import warnings
from typing import Tuple, List

import torch
from torch import nn, Tensor



def validate_positive(value: int, name: str) -> None:
    """Validate that a value is positive."""
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")


def validate_dim(tensor: torch.Tensor, ndim: int) -> None:
    """Validate the number of dimensions in a tensor."""
    if tensor.ndim != ndim:
        raise ValueError(f"Expected tensor with {ndim} dimensions, got {tensor.ndim}")


def validate_shape(tensor: torch.Tensor, shape: Tuple[int, ...], name: str) -> None:
    """Validate the shape of a tensor."""
    if tensor.shape[1:] != shape[1:]:
        raise ValueError(f"{name} tensor shape mismatch: expected {shape}, got {tensor.shape}")



def _check_bins(bins: list[Tensor]) -> None:
    if not bins:
        raise ValueError('The list of bins must not be empty')
    for i, feature_bins in enumerate(bins):
        if not isinstance(feature_bins, Tensor):
            raise ValueError(
                'bins must be a list of PyTorch tensors. '
                f'However, for {i=}: {type(bins[i])=}'
            )
        if feature_bins.ndim != 1:
            raise ValueError(
                'Each item of the bin list must have exactly one dimension.'
                f' However, for {i=}: {bins[i].ndim=}'
            )
        if len(feature_bins) < 2:
            raise ValueError(
                'All features must have at least two bin edges.'
                f' However, for {i=}: {len(bins[i])=}'
            )
        if not feature_bins.isfinite().all():
            raise ValueError(
                'Bin edges must not contain nan/inf/-inf.'
                f' However, this is not true for the {i}-th feature'
            )
        if (feature_bins[:-1] >= feature_bins[1:]).any():
            raise ValueError(
                'Bin edges must be sorted.'
                f' However, the for the {i}-th feature, the bin edges are not sorted'
            )
        if len(feature_bins) == 2:
            warnings.warn(
                f'The {i}-th feature has just two bin edges, which means only one bin.'
                ' Strictly speaking, using a single bin for the'
                ' piecewise-linear encoding should not break anything,'
                ' but it is the same as using sklearn.preprocessing.MinMaxScaler'
            )



def _check_input_shape(x: Tensor, expected_n_features: int) -> None:
    if x.ndim < 1:
        raise ValueError(
            f'The input must have at least one dimension, however: {x.ndim=}'
        )
    if x.shape[-1] != expected_n_features:
        raise ValueError(
            'The last dimension of the input was expected to be'
            f' {expected_n_features}, however, {x.shape[-1]=}'
        )



class _NLinear(nn.Module):
    """N *separate* linear layers for N feature embeddings.

    In other words,
    each feature embedding is transformed by its own dedicated linear layer.
    """

    def __init__(
        self, n: int, in_features: int, out_features: int, bias: bool = True
    ) -> None:
        super().__init__()
        self.weight = nn.Parameter(torch.empty(n, in_features, out_features))
        self.bias = nn.Parameter(torch.empty(n, out_features)) if bias else None
        self.reset_parameters()

    def reset_parameters(self):
        """Reset the parameters."""
        d_in_rsqrt = self.weight.shape[-2] ** -0.5
        nn.init.uniform_(self.weight, -d_in_rsqrt, d_in_rsqrt)
        if self.bias is not None:
            nn.init.uniform_(self.bias, -d_in_rsqrt, d_in_rsqrt)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Do the forward pass."""
        if x.ndim != 3:
            raise ValueError(
                '_NLinear supports only inputs with exactly one batch dimension,'
                ' so `x` must have a shape like (BATCH_SIZE, N_FEATURES, D_EMBEDDING).'
            )
        assert x.shape[-(self.weight.ndim - 1) :] == self.weight.shape[:-1]

        x = x.transpose(0, 1)
        x = x @ self.weight
        x = x.transpose(0, 1)
        if self.bias is not None:
            x = x + self.bias
        return x



def initialize_weights(
    module: nn.Module,
    method: str = "scaled_uniform",
    gain: float = 1.0,
    mode: str = "fan_in",
    nonlinearity: str = "leaky_relu",
    mean: float = 0.0,
    std: float = 1.0,
    a: float = 0.01,
) -> None:
    """
    Initializes the weights of the given module using the specified method.
    """
    if hasattr(module, 'weight') and module.weight is not None:
        if method == "uniform":
            fan = nn.init._calculate_correct_fan(module.weight, mode)
            bound = gain * (1.0 / fan) ** 0.5
            nn.init.uniform_(module.weight, -bound, bound)
        elif method == "normal":
            nn.init.normal_(module.weight, mean, std)
        elif method == "xavier_uniform":
            nn.init.xavier_uniform_(module.weight, gain=gain)
        elif method == "xavier_normal":
            nn.init.xavier_normal_(module.weight, gain=gain)
        elif method == "kaiming_uniform":
            nn.init.kaiming_uniform_(module.weight, a=a, mode=mode, nonlinearity=nonlinearity)
        elif method == "kaiming_normal":
            nn.init.kaiming_normal_(module.weight, a=a, mode=mode, nonlinearity=nonlinearity)
        elif method == "scaled_uniform":
            d_rqsrt = module.weight.shape[1] ** -0.5
            nn.init.uniform_(module.weight, -d_rqsrt, d_rqsrt)
            if hasattr(module, 'bias') and module.bias is not None:
                  nn.init.uniform_(module.bias, -d_rqsrt, d_rqsrt)
        else:
            raise ValueError(f"Unknown initialization method: {method}")

    if hasattr(module, 'bias') and module.bias is not None and method != "scaled_uniform":
        nn.init.constant_(module.bias, 0)

    # Special case for BatchNorm layers
    if isinstance(module, (nn.BatchNorm1d, nn.BatchNorm2d, nn.BatchNorm3d)):
        nn.init.constant_(module.weight, 1)
        nn.init.constant_(module.bias, 0)


