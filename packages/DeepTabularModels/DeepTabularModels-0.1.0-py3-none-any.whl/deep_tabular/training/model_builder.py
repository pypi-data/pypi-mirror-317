class ModelBuilder:
    def __init__(self, model_params: ModelConfig, feature_params: FeatureConfig):
        """
        Initialize the ModelBuilder with model configuration.
        """
        self.model_params = model_params
        self.feature_params = feature_params
        self.models = ['ftt', 'mlp']
        self.model_name = model_params.model_name
        self._validate_params()

    def _validate_params(self) -> None:
        if self.model_name not in self.models:
              raise ValueError(f"{self.model_name} is not defined. The deffined models are: {self.models}")

        # Validate that at least one feature type is used
        if not (self.feature_params.use_cont_features or self.feature_params.use_cat_features):
            raise ValueError("At least one of `use_cont_features` or `use_cat_features` must be True.")

    def build_model(self) -> nn.Module:
        if self.model_name == 'ftt':
              return FTTransformer(
                  use_cont_features=self.feature_params.use_cont_features,
                  use_cat_features=self.feature_params.use_cat_features,
                  linear_embedding_type=self.feature_params.linear_embedding_type,
                  cat_features_kwargs=asdict(self.feature_params.cat_features_kwargs.embeddings_params),
                  cont_features_kwargs=asdict(self.feature_params.cont_features_kwargs.embeddings_params),

                  dim=self.model_params.dim,
                  n_blocks=self.model_params.n_blocks,
                  n_heads=self.model_params.n_heads,
                  attn_type=self.model_params.attn_type,
                  attn_dropout=self.model_params.attn_dropout,
                  ffn_dropout=self.model_params.ffn_dropout,
                  mult=self.model_params.mult,
                  out_dim=self.model_params.out_dim,
                  norm_method=self.model_params.norm_method,
              )
        elif self.model_name == 'mlp':
              d_in = len(self.feature_params.cont_features_kwargs.cont_features) + len(self.feature_params.cat_features_kwargs.cat_features)
              return MLP(
                  use_cont_features=self.feature_params.use_cont_features,
                  use_cat_features=self.feature_params.use_cat_features,
                  linear_embedding_type=self.feature_params.linear_embedding_type,
                  cat_features_kwargs=asdict(self.feature_params.cat_features_kwargs.embeddings_params),
                  cont_features_kwargs=asdict(self.feature_params.cont_features_kwargs.embeddings_params),
                  d_in = d_in,
                  dim = self.model_params.dim,
                  d_layers=self.model_params.d_layers,
                  dropouts=self.model_params.dropouts,
                  activation=self.model_params.activation,
                  d_out=self.model_params.d_out,
              )

