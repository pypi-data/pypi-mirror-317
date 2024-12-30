from .model_utils import *
from .attention_factory import AttentionFactory 
from .embedding_factory import EmbeddingFactory
from .base_model import BaseModel

from typing import List, Union, Callable, Optional, Dict, Any
import torch
import torch.nn.functional as F
from torch import nn, Tensor

class MLP_Backbone(nn.Module):
    """
    A Multi-Layer Perceptron (MLP) model designed for tabular data, based on the architecture
    described in "Revisiting Deep Learning Models for Tabular Data" (Gorishniy et al., 2021).

    Features:
        - Customizable number of layers, sizes, activations, and dropout rates.
        - A modular `Block` class for reusable layer structures.

    References:
        * Gorishniy, Y., Rubachev, I., Khrulkov, V., Babenko, A. "Revisiting Deep Learning Models for Tabular Data", 2021
    """

    class Block(nn.Module):
        """
        A single block in the MLP architecture. Composed of a Linear layer, an activation function,
        and a Dropout layer.
        """

        def __init__(
            self,
            d_in: int,
            d_out: int,
            activation: Union[str, Callable[[], nn.Module]],
            dropout: float,
        ) -> None:
            """
            Args:
                d_in: Input size for the linear layer.
                d_out: Output size for the linear layer.
                activation: Activation function (either a string like "ReLU" or a callable).
                dropout: Dropout rate.
            """
            super().__init__()
            self.linear = nn.Linear(d_in, d_out)
            self.activation = self._get_activation(activation)
            self.dropout = nn.Dropout(dropout)

        def forward(self, x: Tensor) -> Tensor:
            return self.dropout(self.activation(self.linear(x)))

        @staticmethod
        def _get_activation(activation: Union[str, Callable[[], nn.Module]]) -> nn.Module:
            """Helper to resolve the activation function."""
            if isinstance(activation, str):
                return getattr(nn, activation)()
            elif callable(activation):
                return activation()
            else:
                raise ValueError(f"Unsupported activation type: {activation}")

    def __init__(
        self,
        d_in: int,
        d_layers: List[int],
        dropouts: Union[float, List[float]],
        activation: Union[str, Callable[[], nn.Module]],
        d_out: int,
    ) -> None:
        """
        Args:
            d_in: Input size for the MLP.
            d_layers: List of dimensions for each hidden layer.
            dropouts: Either a single dropout rate (applied uniformly) or a list of dropout rates.
            activation: Activation function (either a string like "ReLU" or a callable).
            d_out: Output size for the MLP.
        """
        super().__init__()

        if isinstance(dropouts, float):
            dropouts = [dropouts] * len(d_layers)
        assert len(d_layers) == len(dropouts), (
            "The number of layers (d_layers) and dropouts must match."
        )

        # Create blocks for the hidden layers
        self.blocks = nn.Sequential(
            *[
                MLP_Backbone.Block(
                    d_in=d_layers[i - 1] if i else d_in,
                    d_out=dim,
                    activation=activation,
                    dropout=dropout,
                )
                for i, (dim, dropout) in enumerate(zip(d_layers, dropouts))
            ]
        )

        # Head layer (final output layer)
        self.head = nn.Linear(d_layers[-1] if d_layers else d_in, d_out)

    def forward(self, x: Tensor) -> Tensor:
        """
        Forward pass through the MLP.

        Args:
            x: Input tensor of shape `(batch_size, d_in)`.

        Returns:
            Output tensor of shape `(batch_size, d_out)`.
        """
        x = self.blocks(x)
        return self.head(x)


 


class MLP(BaseModel): 
    def __init__(
        self,
        use_cont_features: bool,
        use_cat_features: bool,
        linear_embedding_type: str,
        cat_features_kwargs: Dict[str, Any],
        cont_features_kwargs: Dict[str, Any],
        dim: int,
        d_in:int,
        d_layers: List[int],
        dropouts: Union[float, List[float]],
        activation: Union[str, Callable[[], nn.Module]],
        d_out: int,
    ) -> None:

        super().__init__(use_cont_features, use_cat_features, linear_embedding_type, cat_features_kwargs, cont_features_kwargs, dim)

        # Validate dimension
        validate_positive(d_in, "d_in")
        validate_positive(d_out, "d_out")

        self.backbone = nn.Sequential(
            nn.Flatten(),
            MLP_Backbone(d_in=d_in*dim, d_layers=d_layers, dropouts=dropouts, activation=activation, d_out=d_out)

        )


    def forward(self, x_cat: Optional[torch.Tensor], x_cont: Optional[torch.Tensor]) -> torch.Tensor:
        if x_cat is None and x_cont is None:
            raise ValueError("At least one of `x_cat` or `x_cont` must be provided.")

        # Validate batch dimensions
        batch_size = self._validate_batch_sizes(x_cat, x_cont)

        x_embeddings = []
    
        if self.cont_embeddings is not None:
            x_embeddings.append(self._process_continuous(x_cont))
        if self.cat_embeddings is not None:
            x_embeddings.append(self._process_categorical(x_cat))
 
        x = torch.cat(x_embeddings, dim=1) 

        return self.backbone(x)
 
