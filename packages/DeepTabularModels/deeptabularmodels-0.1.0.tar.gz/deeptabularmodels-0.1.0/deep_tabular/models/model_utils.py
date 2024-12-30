from typing import Tuple, Literal

import torch
import torch.nn.functional as F
from torch import nn, Tensor

class RMSNorm(nn.Module):
    def __init__(self, normalized_shape, eps=1e-6, elementwise_affine=True):
        super().__init__()
        if isinstance(normalized_shape, int):
            normalized_shape = (normalized_shape,)
        self.normalized_shape = normalized_shape
        self.eps = eps
        self.elementwise_affine = elementwise_affine
        if self.elementwise_affine:
            self.weight = nn.Parameter(torch.ones(self.normalized_shape))
        else:
            self.register_parameter("weight", None)

    def forward(self, x):
        return F.rms_norm(x, self.normalized_shape, self.weight, self.eps)


class GEGLU(nn.Module):
    def forward(self, x: Tensor) -> Tensor:
        x, gates = x.chunk(2, dim=-1)
        return x * F.gelu(gates)

class SiLU(nn.Module):
    """
    Implements the SiLU (Swish) activation function.
    """
    def forward(self, x: Tensor) -> Tensor:
        return x * torch.sigmoid(x)

class ReGLU(nn.Module):
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Split the input into two halves
        x, gates = x.chunk(2, dim=-1)
        # Apply gating and a linear operation
        return x * torch.sigmoid(gates)
        
class FeedForward(nn.Module):
    def __init__(self, dim: int, mult: float = 4.0, dropout: float = 0.1, activation_type: str = 'GEGLU'):
        super().__init__()
        self.activation_type = activation_type
        
        # Determine the activation module based on the type
        if activation_type == 'GEGLU':
            activation = GEGLU()
        elif activation_type == 'SiLU':
            activation = SiLU()
        elif activation_type == 'ReGLU':
            activation = ReGLU()
        elif activation_type == 'ReLU':
            activation = nn.ReLU()
        else:
            raise ValueError(f"Unsupported activation type: {activation_type}")
        
        self.net = nn.Sequential(
            nn.Linear(dim, int(dim * mult * 2)),
            activation,
            nn.Dropout(dropout),
            nn.Linear(int(dim * mult), dim)
        )

    def forward(self, x: Tensor) -> Tensor:
        return self.net(x)

