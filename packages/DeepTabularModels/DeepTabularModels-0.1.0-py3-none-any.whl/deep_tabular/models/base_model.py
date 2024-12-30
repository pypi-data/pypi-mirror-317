from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, Callable
import torch
import torch.nn as nn

# Abstract Base Class
class BaseModel(nn.Module, ABC):
    def __init__(
        self,
        use_cont_features: bool,
        use_cat_features: bool,
        linear_embedding_type: str,
        cat_features_kwargs: Dict[str, Any],
        cont_features_kwargs: Dict[str, Any],
        dim: int,
    ) -> None:

        super().__init__()

        # Validate dimension
        validate_positive(dim, "dim")

        self.cont_embeddings = (
            EmbeddingFactory.create(embedding_type=linear_embedding_type, d_embedding=dim, **cont_features_kwargs)
            if use_cont_features
            else None
        )
        self.cat_embeddings = (
            EmbeddingFactory.create(embedding_type="categorical", d_embedding=dim, **cat_features_kwargs)
            if use_cat_features
            else None
        )

    @abstractmethod
    def forward(self, x_cat: Optional[torch.Tensor], x_cont: Optional[torch.Tensor]) -> torch.Tensor:
        pass
        

    def _validate_batch_sizes(self, x_cat: Optional[torch.Tensor], x_cont: Optional[torch.Tensor]) -> int:
        """Validate and ensure consistent batch dimensions for inputs."""
        batch_sizes = []
        if x_cat is not None:
            batch_sizes.append(x_cat.size(0))
        if x_cont is not None:
            batch_sizes.append(x_cont.size(0))

        if len(set(batch_sizes)) > 1:
            raise ValueError(f"Inconsistent batch sizes: {batch_sizes}")

        return batch_sizes[0]

    def _process_continuous(self, x_cont: Optional[torch.Tensor]) -> torch.Tensor:
        """Process continuous features through the embedding layer."""
        if x_cont is None:
            raise ValueError("Continuous input `x_cont` is required but not provided.")
        x_cont = self.cont_embeddings(x_cont)
        self._check_for_nan(x_cont, 'Continuous Features')
        return x_cont

    def _process_categorical(self, x_cat: Optional[torch.Tensor]) -> torch.Tensor:
        """Process categorical features through the embedding layer."""
        if x_cat is None:
            raise ValueError("Categorical input `x_cat` is required but not provided.")
        self._validate_categorical_indices(x_cat)
        x_cat = self.cat_embeddings(x_cat)
        self._check_for_nan(x_cat, 'Categorical Features')
        return x_cat

    def _validate_categorical_indices(self, x_cat: torch.Tensor) -> None:
        """Validate indices in categorical embeddings to prevent out-of-range access."""
        if not hasattr(self.cat_embeddings, "cardinalities"):
            return  # No cardinalities defined; skip validation

        for idx, cardinality in enumerate(self.cat_embeddings.cardinalities):
            max_index = x_cat[..., idx].max().item()
            if max_index >= cardinality:
                raise IndexError(
                    f"Index out of range for feature {idx}: max index {max_index} >= cardinality {cardinality}"
                )

    def _check_for_nan(self, tensor: torch.Tensor, embedding_type: str) -> None:
        """Check for NaN values in the tensor."""
        if torch.isnan(tensor).any():
            raise ValueError(f"NaN values detected in the output of {embedding_type}.")

