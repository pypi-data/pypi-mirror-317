class BinningEncoder:
    def __init__(self, binning_columns, encoder_path="encoders"):
        """
        Initialize the BinningEncoder.

        Parameters:
        - binning_columns: List of columns to apply binning on.
        - encoder_path: Path to save/load bin information.
        """
        self.binning_columns = binning_columns or []
        self.encoder_path = encoder_path
        self.scaling_method = scaling_method.lower().strip()
        self.bins = {}
        self.scalers = {}

    def fit(self, X: pd.DataFrame):
        data = X.copy()

        for col in self.binning_columns:
            if col not in data.columns:
                raise ValueError(f"Column '{col}' not found in the dataset.")
                
            unique_values = sorted(data[col].unique())
            n_bins = len(unique_values) + 1
            bin_edges = [-np.inf] + unique_values + [np.inf]
            self.bins[col] = {
                "edges": bin_edges,
                "labels": list(range(n_bins)),
            }

        self._save_bins()

    def transform(self, X: pd.DataFrame, columns=None) -> pd.DataFrame:
        data = X.copy()
        binning_columns = columns or self.binning_columns

        if not self.bins:
            self._load_bins()

        for col in binning_columns:
            if col not in data.columns:
                raise ValueError(f"Column '{col}' not found in the dataset.")
            if col not in self.bins:
                raise ValueError(f"Bins for column '{col}' not found. Ensure the encoder is fitted.")

            bin_edges = self.bins[col]["edges"]
            labels = self.bins[col]["labels"]
            data[col] = pd.cut(data[col], bins=bin_edges, labels=labels, include_lowest=True).astype(int)

        return data

    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self.fit(X)
        return self.transform(X)

    def _save_bins(self):
        os.makedirs(self.encoder_path, exist_ok=True)
        for col, bin_info in self.bins.items():
            with open(os.path.join(self.encoder_path, f"{col}_bins.pkl"), "wb") as f:
                pickle.dump(bin_info, f)


    def _load_bins(self):
        for col in self.binning_columns:
            bin_path = os.path.join(self.encoder_path, f"{col}_bins.pkl")
            if os.path.exists(bin_path):
                with open(bin_path, "rb") as f:
                    self.bins[col] = pickle.load(f)
            else:
                raise FileNotFoundError(f"Bin file for column '{col}' not found at {bin_path}.")







class Encoder:
    def __init__(
        self,
        scaler_type: str = 'standard',
        smoothing: float = 10.0,
        min_samples: int = 20,
        handle_unknown: str = 'value',
        handle_missing: str = 'value',
        encoder_path: str = "encoders",
        ordinal_features: Optional[List[str]] = None,
        target_encoder_features: Optional[List[str]] = None,
        one_hot_features: Optional[List[str]] = None,
        numerical_features: Optional[List[str]] = None,
        binning_features: Optional[List[str]] = None,
        logger: Optional[logging.Logger] = None,
    ):
        self.ordinal_features = ordinal_features or []
        self.target_encoder_features = target_encoder_features or []
        self.one_hot_features = one_hot_features or []
        self.numerical_features = numerical_features or []
        self.binning_features = binning_features or []

        self.scaler_type = scaler_type
        self.smoothing = smoothing
        self.min_samples = min_samples
        self.handle_unknown = handle_unknown
        self.handle_missing = handle_missing
        self.encoder_path = encoder_path
        self.scaler_path = os.path.join(encoder_path, "scaler.pkl")

        self.logger = logger or logging.getLogger(__name__)
        self.encoders = {}
        self.scaler = self._initialize_scaler(scaler_type)
        self.biner = BinningEncoder(binning_columns=self.binning_features, encoder_path=encoder_path)

        self.target_encoder_params = {
            "smoothing": self.smoothing,
            "min_samples_leaf": self.min_samples,
            "handle_unknown": self.handle_unknown,
            "handle_missing": self.handle_missing,
        }

    @staticmethod
    def _initialize_scaler(scaler_type: str):
        """Initialize the scaler based on the specified type."""
        if isinstance(scaler_type, ScalerType):
            scaler_type = scaler_type.value

        if scaler_type == 'minmax':
            return MinMaxScaler()
        elif scaler_type == 'standard':
            return StandardScaler()
        elif scaler_type in {None, 'none'}:
            return None
        raise ValueError(f"Unsupported scaler type: {scaler_type}. Supported types are: 'minmax', 'standard', or None.")

    @staticmethod
    def _convert_to_categoricals(data: pd.DataFrame, features: List[str]) -> pd.DataFrame:
        """Convert specified columns to categorical dtype."""
        if features:
            for col in features:
                data[col] = data[col].astype("str").astype("category")
        return data

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None):
        """Fit encoders and scalers to the data."""
        if self.ordinal_features:
            self.logger.debug("Fitting ordinal encoder...")
            self.encoders['ordinal'] = OrdinalEncoder()
            self.encoders['ordinal'].fit(X[self.ordinal_features])

        if self.target_encoder_features:
            self.logger.debug("Fitting target encoder...")
            X = self._convert_to_categoricals(X, self.target_encoder_features)
            self.encoders['target'] = TargetEncoder(**self.target_encoder_params)
            self.encoders['target'].fit(X[self.target_encoder_features], y)

        if self.one_hot_features:
            self.logger.debug("Fitting one-hot encoder...")
            self.encoders['one_hot'] = OneHotEncoder(handle_unknown='ignore', sparse=False)
            self.encoders['one_hot'].fit(X[self.one_hot_features])

        if self.numerical_features:
            self.logger.debug("Fitting scaler...")
            self.scaler.fit(X[self.numerical_features])

        if self.binning_features:
            self.logger.debug("Fitting binning encoder...")
            self.biner.fit(X[self.binning_features])

        self.logger.debug("Saving encoders and scaler...")
        self._save_encoders()
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply encoders and scalers to the data."""
        self.logger.debug("Loading encoders and scaler...")
        self._load_encoders()

        if self.ordinal_features:
            self.logger.debug("Applying ordinal encoding...")
            X[self.ordinal_features] = self.encoders['ordinal'].transform(X[self.ordinal_features]).astype(int)

        if self.target_encoder_features:
            X = self._convert_to_categoricals(X, self.target_encoder_features)
            self.logger.debug("Applying target encoding...")
            X[self.target_encoder_features] = self.encoders['target'].transform(X[self.target_encoder_features])

        if self.one_hot_features:
            self.logger.debug("Applying one-hot encoding...")
            one_hot_encoded = self.encoders['one_hot'].transform(X[self.one_hot_features])
            one_hot_df = pd.DataFrame(
                one_hot_encoded,
                columns=self.encoders['one_hot'].get_feature_names_out(self.one_hot_features),
                index=X.index,
            )
            X = pd.concat([X.drop(columns=self.one_hot_features), one_hot_df], axis=1)

        if self.numerical_features:
            self.logger.debug("Applying scaling...")
            X[self.numerical_features] = self.scaler.transform(X[self.numerical_features])

        if self.binning_features:
            self.logger.debug("Applying binning encoding...")
            X[self.binning_features] = self.biner.transform(X[self.binning_features])

        return X

    def _save_encoders(self):
        """Save all encoders and the scaler to the specified path."""
        os.makedirs(self.encoder_path, exist_ok=True)
        for name, encoder in self.encoders.items():
            with open(os.path.join(self.encoder_path, f'{name}_encoder.pkl'), 'wb') as f:
                pickle.dump(encoder, f)
        with open(self.scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)

    def _load_encoders(self):
        """Load encoders and scaler from the specified path."""
        for name, features in [
            ('ordinal', self.ordinal_features),
            ('target', self.target_encoder_features),
            ('one_hot', self.one_hot_features),
        ]:
            if features:  # Only load if there are corresponding features
                path = os.path.join(self.encoder_path, f'{name}_encoder.pkl')
                if os.path.exists(path):
                    with open(path, 'rb') as f:
                        self.encoders[name] = pickle.load(f)

        if self.numerical_features:
            if os.path.exists(self.scaler_path):
                with open(self.scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)

