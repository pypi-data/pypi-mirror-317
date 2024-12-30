from typing import Tuple, Literal

import torch
import torch.nn.functional as F
from torch import nn, Tensor

class BaseAttention(nn.Module):
    """Base class for multihead attention mechanisms."""

    def __init__(
        self,
        dim: int,
        n_heads: int,
        dropout: float = 0.1,
        initialization: str = "xavier",
        use_relative_positional_encoding: bool = False,
        scale_logits_dynamically: bool = True,
    ):
        super().__init__()

        # Validate input
        assert dim % n_heads == 0, "Embedding size must be divisible by the number of heads."

        # Parameters
        self.dim = dim
        self.n_heads = n_heads
        self.d_head = dim // n_heads
        self.scale_logits_dynamically = scale_logits_dynamically
        self.dropout = nn.Dropout(dropout)

        # Learnable projections
        self.W_q = nn.Linear(dim, dim)
        self.W_k = nn.Linear(dim, dim)
        self.W_v = nn.Linear(dim, dim)
        self.W_out = nn.Linear(dim, dim)

        # Positional encoding (optional)
        self.use_relative_positional_encoding = use_relative_positional_encoding
        if self.use_relative_positional_encoding:
            self.relative_position_bias = nn.Parameter(
                torch.zeros((2 * 512 - 1, self.n_heads))  # Supports up to 512 tokens
            )

        # Initialize weights
        self._initialize_weights(initialization)

    def _initialize_weights(self, initialization: str):
        """Initialize weights with the specified strategy."""
        for layer in [self.W_q, self.W_k, self.W_v, self.W_out]:
            if initialization == "xavier":
                nn.init.xavier_uniform_(layer.weight, gain=1 / 2**0.5)
            elif initialization == "kaiming":
                nn.init.kaiming_uniform_(layer.weight, nonlinearity="relu")
            nn.init.zeros_(layer.bias)

    def _reshape(self, x: torch.Tensor, batch_size: int, n_tokens: int) -> torch.Tensor:
        """Splits embeddings into multiple heads."""
        return x.view(batch_size, n_tokens, self.n_heads, self.d_head).permute(0, 2, 1, 3)

    def _combine_heads(self, x: torch.Tensor, batch_size: int, n_tokens: int) -> torch.Tensor:
        """Combines multiple heads back into a single tensor."""
        return x.permute(0, 2, 1, 3).reshape(batch_size, n_tokens, -1)

    def _apply_relative_positional_encoding(self, attention_logits: torch.Tensor, n_tokens: int) -> torch.Tensor:
        """Add relative positional bias to attention logits."""
        if not self.use_relative_positional_encoding:
            return attention_logits

        position_bias = self.relative_position_bias
        indices = torch.arange(n_tokens).unsqueeze(1) - torch.arange(n_tokens).unsqueeze(0)
        indices = indices + 512 - 1  # Offset for zero-based indexing
        relative_bias = position_bias[indices]  # Shape: (n_tokens, n_tokens, n_heads)
        return attention_logits + relative_bias.permute(2, 0, 1).unsqueeze(0)

    def forward(self, x: torch.Tensor):
        raise NotImplementedError("BaseAttention is an abstract class.")


class FullAttention(BaseAttention):
    """Standard full multihead attention."""

    def forward(self, x: torch.Tensor):
        batch_size, n_tokens, _ = x.size()

        # Compute query, key, and value projections
        q = self._reshape(self.W_q(x), batch_size, n_tokens)
        k = self._reshape(self.W_k(x), batch_size, n_tokens)
        v = self._reshape(self.W_v(x), batch_size, n_tokens)

        # Compute scaled dot-product attention
        attention_logits = torch.matmul(q, k.transpose(-1, -2))

        # Dynamic scaling of logits
        if self.scale_logits_dynamically:
            scaling_factor = torch.tensor(self.d_head, dtype=q.dtype, device=q.device).sqrt()
            attention_logits /= scaling_factor

        # Apply relative positional encodings if enabled
        attention_logits = self._apply_relative_positional_encoding(attention_logits, n_tokens)

        # Compute attention probabilities
        attention_probs = F.softmax(attention_logits, dim=-1)
        attention_probs = self.dropout(attention_probs)

        # Weighted sum of values
        attention_output = torch.matmul(attention_probs, v)
        attention_output = self._combine_heads(attention_output, batch_size, n_tokens)

        # Output projection
        return self.W_out(attention_output)


class SparseAttention(BaseAttention):
    """Sparse multihead attention, useful for irrelevant features."""

    def forward(self, x: torch.Tensor):
        batch_size, n_tokens, _ = x.size()

        # Compute query, key, and value projections
        q = self._reshape(self.W_q(x), batch_size, n_tokens)
        k = self._reshape(self.W_k(x), batch_size, n_tokens)
        v = self._reshape(self.W_v(x), batch_size, n_tokens)

        # Compute scaled dot-product attention
        attention_logits = torch.matmul(q, k.transpose(-1, -2))

        # Sparse masking: Retain only top-k attention logits
        top_k = int(0.1 * n_tokens)  # Keep top 10% attention scores
        _, indices = torch.topk(attention_logits, k=top_k, dim=-1)
        mask = torch.zeros_like(attention_logits).scatter_(-1, indices, 1)
        attention_logits = attention_logits * mask

        # Scale logits
        if self.scale_logits_dynamically:
            attention_logits /= torch.tensor(self.d_head, dtype=q.dtype, device=q.device).sqrt()

        # Compute attention probabilities
        attention_probs = F.softmax(attention_logits, dim=-1)
        attention_probs = self.dropout(attention_probs)

        # Weighted sum of values
        attention_output = torch.matmul(attention_probs, v)
        attention_output = self._combine_heads(attention_output, batch_size, n_tokens)

        # Output projection
        return self.W_out(attention_output)


class LinearAttention(BaseAttention):
    """Linear attention for computational efficiency."""

    def forward(self, x: torch.Tensor):
        batch_size, n_tokens, _ = x.size()

        # Compute query, key, and value projections
        q = self._reshape(self.W_q(x), batch_size, n_tokens)
        k = self._reshape(self.W_k(x), batch_size, n_tokens)
        v = self._reshape(self.W_v(x), batch_size, n_tokens)

        # Linear attention approximation (q @ (k^T @ v))
        k_v = torch.matmul(k.transpose(-1, -2), v)
        attention_output = torch.matmul(q, k_v)

        attention_output = self._combine_heads(attention_output, batch_size, n_tokens)

        # Output projection
        return self.W_out(attention_output)


class AttentionFactory:
    """Factory to create attention modules dynamically."""

    _attention_classes = {
        "full": FullAttention,
        "sparse": SparseAttention,
        "linear": LinearAttention,
    }

    @staticmethod
    def create(
        attention_type: Literal["full", "sparse", "linear"],
        **kwargs,
    ) -> BaseAttention:
        if attention_type not in AttentionFactory._attention_classes:
            raise ValueError(
                f"Unsupported attention type '{attention_type}'. "
                f"Supported types are: {list(AttentionFactory._attention_classes.keys())}"
            )
        return AttentionFactory._attention_classes[attention_type](**kwargs)


def test_attention_factory():
    """
    Test the AttentionFactory by creating instances of different attention mechanisms
    and validating their outputs.
    """
    def check_for_nan(tensor, attention_type):
        if torch.isnan(tensor).any():
            raise ValueError(f"NaN values detected in the output of {attention_type} attention.")

    def run_test(attention_type, **kwargs):
        print(f"Testing {attention_type} Attention...")
        attention_module = AttentionFactory.create(attention_type=attention_type, **kwargs)
        assert isinstance(attention_module, BaseAttention), f"Failed to create {attention_type} Attention"

        # Input tensor: batch_size=4, n_tokens=8, dim=kwargs['dim']
        x = torch.randn(4, 8, kwargs["dim"])

        # Forward pass
        output = attention_module(x)
        assert output.shape == (4, 8, kwargs["dim"]), f"Incorrect output shape for {attention_type} Attention"
        check_for_nan(output, attention_type)
        print(f"{attention_type.capitalize()} Attention passed all checks.")

    # Test parameters
    dim = 64
    n_heads = 8
    kwargs = {
        "dim": dim,
        "n_heads": n_heads,
        "dropout": 0.1,
        "use_relative_positional_encoding": True,
        "scale_logits_dynamically": True,
    }

    # Test FullAttention
    run_test("full", **kwargs)

    # Test SparseAttention
    run_test("sparse", **kwargs)

    # Test LinearAttention
    run_test("linear", **kwargs)

    print("All tests passed!")


#if __name__ == "__main__":
#    try:
#        test_attention_factory()
#    except ValueError as e:
#        print(f"Test failed: {e}")
#    except AssertionError as e:
#        print(f"Assertion failed: {e}")

