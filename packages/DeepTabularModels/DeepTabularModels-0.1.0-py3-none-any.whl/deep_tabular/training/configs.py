
from enum import Enum

# Enums for fixed choices
class LossType(Enum):
    BCE = "bce"
    FOCAL = "focal"


class SchedulerType(Enum):
    NONE = "none"
    COSINE = "cosine_annealing"
    STEP = "step_lr"
    M_STEP = "multi_step_lr"
    REDUCE_ON_PLATEAU = "reduce_on_plateau"
    CYCLIC = "cyclic"
    EXPONENTIAL = "exponential"


class ScalerType(Enum):
    STANDARD = "standard"
    MINMAX = "minmax"
    ROBUST = "robust"


# Configurations
@dataclass
class LossConfig:
    """Configuration for loss function."""
    type: LossType = LossType.BCE
    gamma: Optional[float] = None
    alpha: Optional[float] = None

    def validate(self):
        if self.type == LossType.FOCAL and (self.gamma is None or self.alpha is None):
            raise ValueError("Focal loss requires 'gamma' and 'alpha' to be specified.")


@dataclass
class OptimizerConfig:
    """Configuration for optimizer."""
    lr: float = 1e-4
    weight_decay: float = 1e-5


@dataclass
class SchedulerConfig:
    """Configuration for learning rate scheduler."""
    type: SchedulerType = SchedulerType.NONE
    T_max: Optional[int] = None
    eta_min: float = 0.0
    monitor_mode: Optional[str] = "min"
    factor: Optional[float] = 0.1
    patience: Optional[int] = 10
    step_size: Optional[int] = None
    gamma: Optional[float] = None
    base_lr: Optional[float] = None
    max_lr: Optional[float] = None
    step_size_up: Optional[int] = None
    mode: Optional[str] = None

    def validate(self):
        if self.type == SchedulerType.COSINE and self.T_max is None:
            raise ValueError("CosineAnnealingLR requires 'T_max' to be specified.")


@dataclass
class TreeConfig:
    """Configuration for tree-based binning."""
    min_samples_leaf: int = 64
    min_impurity_decrease: float = 1e-4


@dataclass
class BinsConfig:
    """Configuration for binning."""
    n_bins: int = 48
    bin_type: str = "unsupervised"
    tree_kwargs: Optional[TreeConfig] = None


@dataclass
class EmbeddingConfig:
    """Base class for embedding configurations."""


@dataclass
class LinearEmbeddingConfig(EmbeddingConfig):
    """Configuration for linear embeddings."""
    n_cont_features: int
    activation: bool = False


@dataclass
class PiecewiseEmbeddingConfig(EmbeddingConfig):
    """Configuration for piecewise linear embeddings."""
    bins: List[int] = field(default_factory=list)
    version: str = 'A'
    activation: bool = False


@dataclass
class ContFeaturesKwargs:
    """Configuration for continuous feature processing."""
    bin_config: Optional[BinsConfig] = None
    embeddings_params: Optional[EmbeddingConfig] = None
    cont_features: List[str] = field(default_factory=list)
    numeric_indices: Optional[List[int]] = None


@dataclass
class CatEmbeddingConfig:
    """Configuration for categorical embeddings."""
    cardinalities: List[int] = field(default_factory=list)
    bias: bool = True


@dataclass
class CatFeaturesKwargs:
    """Configuration for categorical feature processing."""
    cat_features: List[str] = field(default_factory=list)
    cat_indices: Optional[List[int]] = None
    embeddings_params: Optional[CatEmbeddingConfig] = None


@dataclass
class FeatureConfig:
    """Configuration for feature processing."""
    target_label: str
    linear_embedding_type: str
    use_cont_features: bool
    use_cat_features: bool
    cat_features_kwargs: CatFeaturesKwargs = field(default_factory=CatFeaturesKwargs)
    cont_features_kwargs: ContFeaturesKwargs = field(default_factory=ContFeaturesKwargs)
    regression: bool = False

    def validate(self):
        if not self.target_label:
            raise ValueError("Target label must be specified.")


@dataclass
class ModelConfig:
    """Base configuration for models."""
    dim: int
    model_name: str



@dataclass
class FTTConfig(ModelConfig):
    """Configuration for Fully Tokenized Transformer models."""
    model_name: str = "ftt"
    n_blocks: int = 6
    n_heads: int = 8
    attn_type: str = "full"
    attn_dropout: float = 0.1
    ffn_dropout: float = 0.1
    mult: int = 4
    out_dim: Optional[int] = None
    norm_method: str = "rms_norm"


@dataclass
class MLPConfig(ModelConfig):
    """Configuration for Multi-Layer Perceptron models."""
    model_name: str = "mlp"
    d_layers: List[int] = field(default_factory=lambda: [64, 32])
    dropouts: Union[float, List[float]] = 0.3
    activation: Union[str, Callable[[], Any]] = "relu"
    d_out: int = 1


@dataclass
class TrainingConfig:
    """Configuration for training."""
    validation_type: str
    validation_split: float = 0.2
    n_splits: int = 5
    max_norm: float = 1.0
    batch_size: int = 32
    test_batch_size: int = 32
    epochs: int = 50
    log_dir: str = "./logs"
    model_save_dir: str = "./models"
    monitor: str = "loss"
    patience: int = 10
    delta: float = 0.01
    seed: int = 42
    use_sampler: bool = False
    loss_config: LossConfig = field(default_factory=LossConfig)
    optimizer_config: OptimizerConfig = field(default_factory=OptimizerConfig)
    scheduler_config: SchedulerConfig = field(default_factory=SchedulerConfig)


@dataclass
class EncoderConfig:
    """Configuration for data encoders."""
    ordinal_features: List[str] = field(default_factory=list)
    target_encoder_features: List[str] = field(default_factory=list)
    binning_features: List[str] = field(default_factory=list)
    one_hot_features: List[str] = field(default_factory=list)
    numerical_features: List[str] = field(default_factory=list)
    scaler_type: ScalerType = ScalerType.STANDARD
    smoothing: int = 10
    min_samples: int = 20
    handle_unknown: str = "ignore"
    handle_missing: str = "mean"
    encoder_path: str = "./encoders"


@dataclass
class Config:
    """Main configuration."""
    train_file: str = "art_train_file.csv"
    org_train_file: str = "org_train_file.csv"
    test_file: str = "test_file.csv"
    submission_file: str = "sample_submission.csv"
    with_cuda: bool = torch.cuda.is_available()
    seed: int = 42

