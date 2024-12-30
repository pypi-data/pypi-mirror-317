from .model_utils import *
from .attention_factory import AttentionFactory 
from .embedding_factory import EmbeddingFactory
from .base_model import BaseModel

from typing import List, Union, Callable, Optional, Dict, Any
import torch
import torch.nn.functional as F
from torch import nn, Tensor

class TransformerBlock(nn.Module):
    """
    A single block of the Transformer.
    """
    def __init__(
        self,
        dim: int,
        n_heads: int,
        attn_type: str = "full",
        attn_dropout: float = 0.1,
        ffn_dropout: float = 0.1,
        mult: float = 4.0,
        norm_method: str = "layer_norm",
        first_block: bool = False,
    ) -> None:
        super().__init__()

        self.dim = dim
        self.n_heads = n_heads

        # Validate inputs
        self._validate_inputs(dim, n_heads, norm_method)

        # Normalization layers
        self.attention_norm = self._get_normalization(norm_method, dim) if not first_block else None
        self.ffn_norm = self._get_normalization(norm_method, dim)

        # Attention and feed-forward layers
        self.attention = AttentionFactory.create(
            attention_type=attn_type,
            dim=dim,
            n_heads=n_heads,
            dropout=attn_dropout,
        )
        self.ffn = FeedForward(dim, mult=mult, dropout=ffn_dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the Transformer block.
        """
        if x.ndim != 3 or x.size(-1) != self.dim:
            raise ValueError(f"Expected input shape [batch_size, seq_len, {self.dim}], got {x.shape}.")

        # Self-attention block
        residual = x
        if self.attention_norm:
            x = self.attention_norm(x)
        x = self.attention(x) + residual

        # Feed-forward block
        residual = x
        x = self.ffn_norm(x)
        x = self.ffn(x) + residual

        # Ensure no NaN values in output
        if torch.isnan(x).any():
            raise ValueError("NaN values detected in TransformerBlock output.")

        return x

    @staticmethod
    def _validate_inputs(dim: int, n_heads: int, norm_method: str) -> None:
        """Validate input arguments."""
        if dim <= 0 or n_heads <= 0:
            raise ValueError(f"Both `dim` and `n_heads` must be positive. Got dim={dim}, n_heads={n_heads}.")
        if dim % n_heads != 0:
            raise ValueError(f"`dim` must be divisible by `n_heads`. Got dim={dim}, n_heads={n_heads}.")
        if norm_method not in {"layer_norm", "rms_norm"}:
            raise ValueError(f"Unsupported normalization method: {norm_method}. Must be 'layer_norm' or 'rms_norm'.")

    @staticmethod
    def _get_normalization(norm_method: str, dim: int) -> nn.Module:
        """Get the normalization layer based on the specified method."""
        if norm_method == "layer_norm":
            return nn.LayerNorm(dim)
        elif norm_method == "rms_norm":
            return RMSNorm(dim)
        else:
            raise ValueError(f"Undefined normalization method: {norm_method}.")
            
            


class FTTransformerBackbone(nn.Module):
    """
    Backbone of the FT-Transformer.
    """
    def __init__(
        self,
        dim: int,
        n_blocks: int,
        n_heads: int,
        attn_type: str = "full",
        attn_dropout: float = 0.1,
        ffn_dropout: float = 0.1,
        mult: float = 4.0,
        norm_method: str = "rms_norm",
        out_dim: Optional[int] = None,
    ):
        super().__init__()

        # Validate inputs
        self._validate_inputs(dim, n_heads, norm_method)

        # Transformer blocks
        self.blocks = nn.ModuleList([
            TransformerBlock(
                dim=dim,
                n_heads=n_heads,
                attn_type=attn_type,
                attn_dropout=attn_dropout,
                ffn_dropout=ffn_dropout,
                mult=mult,
                norm_method=norm_method,
                first_block=(i == 0),
            )
            for i in range(n_blocks)
        ])

        # Final normalization
        self.final_norm = self._get_normalization(norm_method, dim)

        # Optional output head
        self.head = (
            nn.Sequential(
                nn.ReLU(),
                nn.Dropout(ffn_dropout),
                nn.Linear(dim, out_dim),
            )
            if out_dim else None
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the FT-Transformer backbone.
        """
        if x.ndim != 3 or x.size(-1) != self.blocks[0].dim:
            raise ValueError(f"Expected input of shape [batch_size, seq_len, {self.blocks[0].dim}], got {x.shape}.")

        # Pass through Transformer blocks
        for block in self.blocks:
            x = block(x)

        # Extract [CLS] token (first token) for classification tasks
        logits = self.final_norm(x[:, 0])

        # Apply output head if defined
        if self.head:
            logits = self.head(logits)

        # Ensure no NaN values in the output
        if torch.isnan(logits).any():
            raise ValueError("NaN values detected in FTTransformerBackbone output.")

        return logits

    @staticmethod
    def _validate_inputs(dim: int, n_heads: int, norm_method: str) -> None:
        """Validate initialization inputs."""
        if dim <= 0 or n_heads <= 0:
            raise ValueError(f"Both `dim` and `n_heads` must be positive. Got dim={dim}, n_heads={n_heads}.")
        if dim % n_heads != 0:
            raise ValueError(f"`dim` must be divisible by `n_heads`. Got dim={dim}, n_heads={n_heads}.")
        if norm_method not in {"layer_norm", "rms_norm"}:
            raise ValueError(f"Unsupported normalization method: {norm_method}. Must be 'layer_norm' or 'rms_norm'.")

    @staticmethod
    def _get_normalization(norm_method: str, dim: int) -> nn.Module:
        """Get the normalization layer based on the specified method."""
        if norm_method == "layer_norm":
            return nn.LayerNorm(dim)
        elif norm_method == "rms_norm":
            return RMSNorm(dim)
        else:
            raise ValueError(f"Undefined normalization method: {norm_method}.")




class FTTransformer(BaseModel):
    """The FTTransformer model."""
    def __init__(
        self,
        use_cont_features: bool,
        use_cat_features: bool,
        linear_embedding_type: str,
        cat_features_kwargs: Dict[str, Any],
        cont_features_kwargs: Dict[str, Any],
        dim: int,
        n_blocks: int = 6,
        n_heads: int = 8,
        attn_type: str = "full",
        attn_dropout: float = 0.1,
        ffn_dropout: float = 0.1,
        mult: float = 4.0,
        norm_method: str = "rms_norm",
        out_dim: Optional[int] = None,
    ) -> None:

        super().__init__(use_cont_features, use_cat_features, linear_embedding_type, cat_features_kwargs, cont_features_kwargs, dim)

        # Transformer Backbone
        self.backbone = FTTransformerBackbone(dim = dim,
                                              n_blocks = n_blocks,
                                              n_heads = n_heads,
                                              attn_type = attn_type,
                                              attn_dropout = attn_dropout,
                                              ffn_dropout = ffn_dropout,
                                              mult = mult,
                                              norm_method = norm_method,
                                              out_dim = out_dim)

    def forward(self, x_cat: Optional[torch.Tensor], x_cont: Optional[torch.Tensor]) -> torch.Tensor:
        if x_cat is None and x_cont is None:
            raise ValueError("At least one of `x_cat` or `x_cont` must be provided.")

        # Validate batch dimensions
        batch_size = self._validate_batch_sizes(x_cat, x_cont)

        # Add CLS embedding
        x_embeddings = [self.cls_embedding((batch_size,))]
        self._check_for_nan(x_embeddings[0], 'CLS Embedding')

        # Process and append embeddings
        if self.cont_embeddings is not None:
            x_embeddings.append(self._process_continuous(x_cont))
        if self.cat_embeddings is not None:
            x_embeddings.append(self._process_categorical(x_cat))

        # Combine embeddings and pass through the Transformer backbone
        x = torch.cat(x_embeddings, dim=1)
        return self.backbone(x)

