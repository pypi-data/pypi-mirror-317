import warnings
from typing import Union, Optional, List, Any, Tuple, Dict, Literal
from .embedding_utils import * 
import torch
from torch import nn, Tensor
from torch.nn import functional as F
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from tqdm import tqdm


class BinComputer:
    """
    A class to compute bin boundaries for PiecewiseLinearEncoding and PiecewiseLinearEmbeddings.

    Supports both supervised (using a target `y`) and unsupervised approaches.
    """
    def __init__(self, n_bins: int, verbose: bool = False):
        if n_bins <= 1:
            raise ValueError("n_bins must be greater than 1.")

        self.n_bins = n_bins
        self.verbose = verbose

    @staticmethod
    def _validate_inputs(X: Union[Tensor, pd.DataFrame], y: Optional[Union[Tensor, pd.Series]] = None):
        # Convert X and y to PyTorch tensors if they are pandas DataFrame/Series
        if isinstance(X, pd.DataFrame):
            X = torch.tensor(X.values, dtype=torch.float32)
        if isinstance(y, pd.Series):
            y = torch.tensor(y.values, dtype=torch.float32)

        # Validate X
        if not isinstance(X, Tensor):
            raise ValueError(f'X must be a PyTorch tensor, however: {type(X)=}')
        if X.ndim != 2:
            raise ValueError(f'X must have exactly two dimensions, however: {X.ndim=}')
        if X.shape[0] < 2:
            raise ValueError(f'X must have at least two rows, however: {X.shape[0]=}')
        if X.shape[1] < 1:
            raise ValueError(f'X must have at least one column, however: {X.shape[1]=}')
        if not X.isfinite().all():
            raise ValueError('X must not contain nan/inf/-inf.')
        if (X == X[0]).all(dim=0).any():
            raise ValueError(
                'All columns of X must have at least two distinct values.'
                ' However, X contains columns with just one distinct value.'
            )
        return X, y


    def compute_unsupervised(self, X: Union[Tensor, pd.DataFrame]) -> list[Tensor]:
        X, _ = self._validate_inputs(X)

        _upper = 2**24  # 16_777_216
        if len(X) > _upper:
            warnings.warn(
                f'Computing quantile-based bins for more than {_upper} million objects'
                ' may not be possible due to the limitation of PyTorch.'
            )
        bins = [
            q.unique()
            for q in torch.quantile(
                X, torch.linspace(0.0, 1.0, self.n_bins + 1).to(X), dim=0
            ).T
        ]
        self._check_bins(bins)
        return bins

    def compute_supervised(
        self,
        X: Union[Tensor, pd.DataFrame],
        y: Union[Tensor, pd.Series],
        regression: bool,
        tree_kwargs: Optional[dict[str, Any]] = None,
    ) -> list[Tensor]:
        X, y = self._validate_inputs(X, y)

        if y.ndim != 1:
            raise ValueError(f'y must have exactly one dimension, however: {y.ndim=}')
        if len(y) != len(X):
            raise ValueError(
                f'len(y) must be equal to len(X), however: {len(y)=}, {len(X)=}'
            )
        if tree_kwargs is None:
            tree_kwargs = {}
        if 'max_leaf_nodes' in tree_kwargs:
            raise ValueError(
                'tree_kwargs must not contain the key "max_leaf_nodes"'
                ' (it will be set to n_bins automatically).'
            )

        bins = []
        tqdm_ = tqdm if self.verbose else lambda x: x

        for column in tqdm_(X.T):
            feature_bin_edges = [float(column.min()), float(column.max())]
            tree = (
                DecisionTreeRegressor if regression else DecisionTreeClassifier
            )(max_leaf_nodes=self.n_bins, **tree_kwargs).fit(column.reshape(-1, 1), y)

            for node_id in range(tree.tree_.node_count):
                if tree.tree_.children_left[node_id] != tree.tree_.children_right[node_id]:
                    feature_bin_edges.append(float(tree.tree_.threshold[node_id]))
            bins.append(torch.as_tensor(feature_bin_edges).unique())
        self._check_bins(bins)
        return [x.to(device=X.device, dtype=X.dtype) for x in bins]

    @staticmethod
    def _check_bins(bins: list[Tensor]):
        for b in bins:
            if len(b) < 2:
                raise ValueError("Each feature must have at least two bin edges.")




class BaseEmbedding(nn.Module):
    """Base class for all embedding modules."""

    def __init__(self, d_embedding: int) -> None:
        """
        Args:
            d_embedding (int): The embedding size.
        """
        super().__init__()
        validate_positive(d_embedding, "d_embedding")
        self.d_embedding = d_embedding

    def initialize_weights(self, module: nn.Module, **kwargs) -> None:
        """Initialize weights of the module."""
        initialize_weights(module, **kwargs)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Abstract method for forward pass."""
        raise NotImplementedError("BaseEmbedding is an abstract class and cannot be used directly.")



class LinearEmbeddings(nn.Module):
    """Linear embeddings for continuous features."""

    def __init__(self, d_embedding: int, n_cont_features: int, activation: bool = False) -> None:
        """
        Args:
            d_embedding (int): The embedding size.
            n_cont_features (int): Number of continuous features.
            activation (bool): Whether to apply ReLU activation after embeddings.
        """
        super().__init__()
        self.d_embedding = d_embedding
        self.n_cont_features = n_cont_features
        self.weight = nn.Parameter(torch.empty(n_cont_features, d_embedding))
        self.bias = nn.Parameter(torch.empty(n_cont_features, d_embedding))
        self.activation = nn.ReLU() if activation else None
        self.reset_parameters()

    def reset_parameters(self) -> None:
        d_rqsrt = self.weight.shape[1] ** -0.5
        nn.init.uniform_(self.weight, -d_rqsrt, d_rqsrt)
        nn.init.uniform_(self.bias, -d_rqsrt, d_rqsrt)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for continuous feature embeddings.

        Args:
            x (torch.Tensor): Input tensor of shape [batch_size, n_cont_features].

        Returns:
            torch.Tensor: Output tensor of shape [batch_size, n_cont_features, d_embedding].
        """
        if torch.isnan(x).any() or torch.isinf(x).any():
            raise ValueError("Input contains NaN or Inf values.")

        if x.shape[1] != self.weight.shape[0]:
            raise ValueError(
                f"Expected input shape [batch_size, {self.weight.shape[0]}], got {x.shape}."
            )

        # Compute embeddings
        x = torch.addcmul(self.bias, self.weight, x[..., None])  # Linear transformation

        # Apply activation if defined
        if self.activation:
            x = self.activation(x)

        return x



class PiecewiseLinearEmbeddings(BaseEmbedding):
    """Piecewise-linear embeddings."""

    def __init__(
        self,
        d_embedding: int,
        bins: List[torch.Tensor],
        activation: bool = True,
        version: Literal[None, "A", "B"] = None,
    ) -> None:
        super().__init__(d_embedding)
        _check_bins(bins)
        if version is None:
            warnings.warn("No version provided. Defaulting to 'A' for backward compatibility.")
            version = "A"

        n_features = len(bins)
        self.linear0 = LinearEmbeddings(d_embedding, n_features) if version == "B" else None
        self.impl = _PiecewiseLinearEncodingImpl(bins)
        self.linear = _NLinear(n_features, self.impl.get_max_n_bins(), d_embedding, bias=version != "B")
        self.activation = nn.ReLU() if activation else None

        if version == "B":
            nn.init.zeros_(self.linear.weight)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        validate_dim(x, 2)
        x_linear = None if self.linear0 is None else self.linear0(x)
        x_ple = self.impl(x)
        x_ple = self.linear(x_ple)
        if self.activation:
            x_ple = self.activation(x_ple)
        return x_ple if x_linear is None else x_linear + x_ple


class CategoricalEmbeddings(BaseEmbedding):
    """Embedding for categorical features."""

    def __init__(self, cardinalities: List[int], d_embedding: int, bias: bool = True) -> None:
        super().__init__(d_embedding)
        if not cardinalities:
            raise ValueError("No categorical features provided.")
        self.cardinalities = cardinalities
        self.embeddings = nn.ModuleList([nn.Embedding(c, d_embedding) for c in cardinalities])
        self.bias = nn.Parameter(torch.zeros(len(cardinalities), d_embedding)) if bias else None
        self.reset_parameters()

    def reset_parameters(self) -> None:
        d_rsqrt = self.embeddings[0].embedding_dim ** -0.5
        for m in self.embeddings:
            nn.init.uniform_(m.weight, -d_rsqrt, d_rsqrt)
        if self.bias is not None:
            nn.init.uniform_(self.bias, -d_rsqrt, d_rsqrt)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.ndim != 2:
            raise ValueError(f"Expected input of shape [batch_size, n_features], got {x.shape}.")
        if x.shape[1] != len(self.embeddings):
            raise ValueError(f"Expected input with {len(self.embeddings)} features, got {x.shape[1]}.")

        # Validate indices
        for idx, cardinality in enumerate(self.cardinalities):
            if x[..., idx].max().item() >= cardinality:
                raise IndexError(
                    f"Index out of range for feature {idx}: max index {x[..., idx].max().item()} >= cardinality {cardinality}."
                )

        # Compute embeddings
        embeddings = torch.stack([embed(x[..., i]) for i, embed in enumerate(self.embeddings)], dim=-2)

        # Add bias
        if self.bias is not None:
            embeddings += self.bias

        return embeddings


class _CLSEmbedding(BaseEmbedding):
    """CLS token embedding."""

    def __init__(self, d_embedding: int) -> None:
        super().__init__(d_embedding)
        self.weight = nn.Parameter(torch.empty(d_embedding))
        self.reset_parameters()

    def reset_parameters(self) -> None:
        d_rsqrt = self.weight.shape[-1] ** -0.5
        nn.init.uniform_(self.weight, -d_rsqrt, d_rsqrt)

    def forward(self, batch_dims: Tuple[int]) -> torch.Tensor:
        if not batch_dims:
            raise ValueError("Batch dimensions cannot be empty.")
        return self.weight.expand(*batch_dims, 1, -1)




class EmbeddingFactory:
    """
    Factory to create embedding modules dynamically based on the specified type.

    Supports the following embedding types:
    - LinearEmbeddings
    - PiecewiseLinearEmbeddings
    - CategoricalEmbeddings
    - _CLSEmbedding
    """

    _embedding_classes = {
        "linear": LinearEmbeddings,
        "piecewise_linear": PiecewiseLinearEmbeddings,
        "categorical": CategoricalEmbeddings,
        "cls": _CLSEmbedding,
    }

    @staticmethod
    def create(
        embedding_type: str,
        d_embedding: int,
        **kwargs: Any,
    ) -> nn.Module:
        """
        Create an embedding module dynamically.

        Args:
            embedding_type (str): The type of embedding to create. Must be one of:
                                  "linear", "piecewise_linear", "categorical", "cls".
            d_embedding (int): The embedding dimension for the module.
            **kwargs: Additional parameters specific to the embedding type.

        Returns:
            nn.Module: The created embedding module.

        Raises:
            ValueError: If the embedding_type is not supported or if required parameters are missing.
        """
        if embedding_type not in EmbeddingFactory._embedding_classes:
            raise ValueError(
                f"Unsupported embedding type '{embedding_type}'. "
                f"Supported types are: {list(EmbeddingFactory._embedding_classes.keys())}"
            )

        # Fetch the embedding class
        embedding_class = EmbeddingFactory._embedding_classes[embedding_type]

        # Ensure required parameters for each embedding type are provided
        if embedding_type == "linear":
            required_params = ["n_cont_features"]
            self._validate_params(required_params, kwargs)
            return embedding_class(d_embedding=d_embedding, **kwargs)

        if embedding_type == "piecewise_linear":
            required_params = ["bins"]
            self._validate_params(required_params, kwargs)
            return embedding_class(d_embedding=d_embedding, **kwargs)

        if embedding_type == "categorical":
            required_params = ["cardinalities"]
            self._validate_params(required_params, kwargs)
            return embedding_class(d_embedding=d_embedding, **kwargs)

        if embedding_type == "cls":
            return embedding_class(d_embedding=d_embedding)

        raise ValueError(f"Unhandled embedding type: {embedding_type}")


    def _validate_params(self, required_params: List[str], provided_params: Dict[str, Any]) -> None:
        """
        Validate that the required parameters are present in the provided parameters.
        """
        missing_params = [param for param in required_params if param not in provided_params]
        if missing_params:
            raise ValueError(f"Missing required parameters: {missing_params}")



def combined_test():
    """Run all tests for LinearEmbeddings, CategoricalEmbeddings, and EmbeddingFactory."""
    def check_output(tensor, expected_shape, description):
        assert tensor.shape == expected_shape, f"{description} failed: Expected shape {expected_shape}, got {tensor.shape}."
        if torch.isnan(tensor).any():
            raise ValueError(f"{description} failed: Output contains NaN values.")
        if torch.isinf(tensor).any():
            raise ValueError(f"{description} failed: Output contains Inf values.")

    # ---- LinearEmbeddings Tests ----
    def test_linear_embeddings():
        print("Testing LinearEmbeddings...")
        batch_size = 16
        n_cont_features = 5
        d_embedding = 8
        x = torch.randn(batch_size, n_cont_features)

        embedding_layer = LinearEmbeddings(d_embedding=d_embedding, n_cont_features=n_cont_features, activation=True)
        output = embedding_layer(x)
        check_output(output, (batch_size, n_cont_features, d_embedding), "LinearEmbeddings standard functionality")

        # NaN Input Test
        x_nan = x.clone()
        x_nan[0, 0] = float('nan')
        try:
            embedding_layer(x_nan)
        except ValueError as e:
            print(f"Correctly caught NaN in LinearEmbeddings input: {e}")

        # Inf Input Test
        x_inf = x.clone()
        x_inf[0, 0] = float('inf')
        try:
            embedding_layer(x_inf)
        except ValueError as e:
            print(f"Correctly caught Inf in LinearEmbeddings input: {e}")

        # Empty Input Test
        x_empty = torch.empty(0, n_cont_features)
        try:
            embedding_layer(x_empty)
        except ValueError as e:
            print(f"Correctly caught empty input in LinearEmbeddings: {e}")

    # ---- CategoricalEmbeddings Tests ----
    def test_categorical_embeddings():
        print("Testing CategoricalEmbeddings...")
        cardinalities = [5, 10, 20]
        d_embedding = 8
        batch_size = 4
        x = torch.randint(0, 5, (batch_size, len(cardinalities)))

        categorical_embeddings = CategoricalEmbeddings(cardinalities=cardinalities, d_embedding=d_embedding)
        output = categorical_embeddings(x)
        expected_shape = (batch_size, len(cardinalities), d_embedding)
        check_output(output, expected_shape, "CategoricalEmbeddings standard functionality")

        # No Bias Test
        categorical_embeddings_no_bias = CategoricalEmbeddings(cardinalities=cardinalities, d_embedding=d_embedding, bias=False)
        output_no_bias = categorical_embeddings_no_bias(x)
        check_output(output_no_bias, expected_shape, "CategoricalEmbeddings without bias")

        # Different Batch Sizes
        for batch_size in [1, 10, 50]:
            x = torch.randint(0, 5, (batch_size, len(cardinalities)))
            output = categorical_embeddings(x)
            check_output(output, (batch_size, len(cardinalities), d_embedding), f"CategoricalEmbeddings batch size {batch_size}")

        # Empty Cardinalities
        try:
            CategoricalEmbeddings(cardinalities=[], d_embedding=d_embedding)
        except ValueError as e:
            print(f"Correctly caught empty cardinalities in CategoricalEmbeddings: {e}")

        # Invalid Indices
        x_invalid = torch.tensor([[0, 9, 21]])
        try:
            categorical_embeddings(x_invalid)
        except IndexError as e:
            print(f"Correctly caught invalid indices in CategoricalEmbeddings: {e}")

        # NaN Propagation
        x_nan = torch.tensor([[0, 1, 2], [float('nan'), 0, 1]]).to(torch.int64)
        try:
            categorical_embeddings(x_nan)
        except Exception as e:
            print(f"Correctly handled NaN input in CategoricalEmbeddings: {e}")

    # ---- EmbeddingFactory Tests ----
    def test_embedding_factory():
        print("Testing EmbeddingFactory...")
        d_embedding = 8

        # LinearEmbeddings Creation
        linear_emb = EmbeddingFactory.create("linear", d_embedding, n_cont_features=5)
        assert isinstance(linear_emb, LinearEmbeddings), "Failed to create LinearEmbeddings."

        # CategoricalEmbeddings Creation
        cat_emb = EmbeddingFactory.create("categorical", d_embedding, cardinalities=[5, 10, 20])
        assert isinstance(cat_emb, CategoricalEmbeddings), "Failed to create CategoricalEmbeddings."

        # Unsupported Type
        try:
            EmbeddingFactory.create("unsupported", d_embedding)
        except ValueError as e:
            print(f"Correctly caught unsupported embedding type: {e}")

        # Missing Parameters
        try:
            EmbeddingFactory.create("linear", d_embedding)
        except ValueError as e:
            print(f"Correctly caught missing parameters for LinearEmbeddings: {e}")

    # Run all tests
    test_linear_embeddings()
    test_categorical_embeddings()
    test_embedding_factory()
    print("All combined tests passed!")

#if __name__ == "__main__":
#    try:
#        combined_test()
#    except AssertionError as e:
#        print(f"Test failed: {e}")
#    except ValueError as e:
#        print(f"Value error: {e}")
#    except IndexError as e:
#        print(f"Index error: {e}")
#    except Exception as e:
#        print(f"Unexpected error: {e}")


