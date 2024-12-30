

def save_predictions(predictions: Dict[str, np.ndarray], save_path: str) -> None:
    """Save predictions to disk."""
    create_directory(save_path)
    for key, value in predictions.items():
        np.save(os.path.join(save_path, f"fft_{key}.npy"), value)
    logging.info("Predictions saved successfully.")


def create_directory(path: str) -> None:
    """Create a directory if it does not exist."""
    os.makedirs(path, exist_ok=True)

def handle_extra_data(train_df: pd.DataFrame, extra_data: pd.DataFrame, logger=None) -> pd.DataFrame:
    """
    Concatenate extra data to the training dataset if provided.
    """
    if extra_data is not None and not extra_data.empty:
        logger.info("Appending extra data to training data...")
        train_df = pd.concat([train_df.reset_index(drop=True), extra_data.reset_index(drop=True)], axis=0)
    return train_df
    
def set_reproducibility(seed: int):
    """
    Set seeds and other configurations for reproducibility.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if Config.with_cuda:
        torch.cuda.manual_seed_all(seed)

    # Configure PyTorch for deterministic behavior
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    os.environ['PYTHONHASHSEED'] = str(seed)

    # Uncomment the following if strict reproducibility is required.
    # torch.use_deterministic_algorithms(True)

def load_data(file_name, logger=None):
    try:
        data = pd.read_csv(file_name)
    except FileNotFoundError as e:
        if logger:
            logger.error(f"File not found: {e}")
        raise
    return data
    
def process_single_validation(
    *,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    extra_data: pd.DataFrame,
    encoder_params: EncoderConfig,
    feature_params: FeatureConfig,
    model_params: ModelConfig,
    bins_params: BinsConfig,
    training_params: TrainingConfig,
    save_preds_path: str,
    logger: logging.Logger,
) -> None:
    """
    Handle single validation split training and prediction.
    """
    logger.info("Starting single validation split...")

    # Split training data into train and validation sets
    seed = training_params.seed
    train_df, val_df = train_test_split(
        train_data,
        test_size=training_params.validation_split,
        stratify=train_data[feature_params.target_label],
        random_state=seed,
    )
    train_df, val_df = train_df.reset_index(drop=True), val_df.reset_index(drop=True)

    # Add extra data
    train_df = handle_extra_data(train_df, extra_data, logger)

    # Process and train the model
    result = process_and_train(
        train_df=train_df.copy(),
        val_df=val_df.copy(),
        test_df=test_data.copy(),
        encoder_params=encoder_params,
        feature_params=feature_params,
        model_params=model_params,
        bins_params=bins_params,
        training_params=training_params,
        fold=None,
        logger=logger,
    )

    # Save predictions
    predictions = {"val": result["val_preds"], "test": result["test_preds"]}
    save_predictions(predictions, save_preds_path)

    logger.info(f"Single validation training completed. Best model saved at {result['best_model_path']}.")


def process_k_fold_validation(
    *,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    extra_data: pd.DataFrame,
    encoder_params: EncoderConfig,
    feature_params: FeatureConfig,
    model_params: ModelConfig,
    bins_params: BinsConfig,
    training_params: TrainingConfig,
    save_preds_path: str,
    logger: logging.Logger,
) -> None:
    """
    Handle k-fold cross-validation training and prediction.
    Ensures folds are independent and do not affect each other.
    """
    logger.info(f"Starting K-Fold Cross-Validation with {training_params.n_splits} folds...")
    seed = training_params.seed
    skf = StratifiedKFold(n_splits=training_params.n_splits, shuffle=True, random_state=seed)

    #train_data = handle_extra_data(train_data, extra_data, logger)
    fold_results = []
    oof_predictions = np.zeros(len(train_data))
    test_predictions = []

    for fold, (train_idx, val_idx) in enumerate(skf.split(train_data, train_data[feature_params.target_label]), 1):
        logger.info(f"Training Fold {fold}/{training_params.n_splits}...")

        # Create independent copies for train and validation data
        fold_train_df = train_data.iloc[train_idx].copy()
        fold_val_df = train_data.iloc[val_idx].copy()

        # Ensure no shared data between folds
        fold_train_df = handle_extra_data(fold_train_df, extra_data, logger)

        # Train the model and get results
        result = process_and_train(
            train_df=fold_train_df,
            val_df=fold_val_df,
            test_df=test_data.copy(),  # Ensure test data remains independent
            encoder_params=encoder_params,
            feature_params=feature_params,
            model_params=model_params,
            bins_params=bins_params,
            training_params=training_params,
            fold=fold,
            logger=logger,
        )

        # Store results
        fold_results.append(result["auc"])
        oof_predictions[val_idx] = result["val_preds"]
        test_predictions.append(result["test_preds"])

        logger.info(f"Fold {fold} completed. AUC: {result['auc']:.4f}")

    # Aggregate test predictions
    aggregated_test_preds = np.mean(test_predictions, axis=0)

    # Save predictions
    logger.info(f"Cross-validation completed. Average AUC: {np.mean(fold_results):.4f}")
    predictions = {"val": oof_predictions, "test": aggregated_test_preds}
    save_predictions(predictions, save_preds_path)



def run_training(validation_type: str, **kwargs):
    """
    Run the training process based on the validation type.

    Args:
        validation_type (str): The type of validation ("single" or "kfold").
        **kwargs: Additional arguments to pass to the specific training process.

    Raises:
        ValueError: If an invalid validation type is provided.
    """
    if validation_type == "single":
        return process_single_validation(**kwargs)
    elif validation_type == "kfold":
        return process_k_fold_validation(**kwargs)
    else:
        raise ValueError(f"Invalid validation type: {validation_type}")




def process_and_train(
    train_df: pd.DataFrame,
    val_df: pd.DataFrame,
    test_df: pd.DataFrame,
    encoder_params: EncoderConfig,
    feature_params: FeatureConfig,
    model_params: ModelConfig,
    bins_params: BinsConfig,
    training_params: TrainingConfig,
    fold: Optional[int] = None,
    logger: Optional[logging.Logger] = None,
) -> Dict[str, Any]:
    """
    Preprocess data, build loaders, and train the model.

    """

    # Create directories
    save_path = os.path.join(
        training_params.model_save_dir,
        f"model_{fold}/best_model.pth" if fold else "best_model.pth"
    )
    create_directory(os.path.dirname(save_path))

    encoders_path = os.path.join(
        training_params.model_save_dir,
        f"model_{fold}" if fold else "encoders"
    )
    create_directory(os.path.dirname(encoders_path))

    # Initialize and fit the encoder
    encoder = Encoder(**vars(encoder_params), logger=logger)
    encoder.fit(train_df, train_df[feature_params.target_label].values)

    # Transform datasets
    train_df = encoder.transform(train_df)
    val_df = encoder.transform(val_df)
    test_df = encoder.transform(test_df)

    # Compute bins if required
    embedding_type = feature_params.linear_embedding_type
    if embedding_type == "piecewise_linear":
        bin_computer = BinComputer(n_bins=bins_params.n_bins, verbose=False)
        X=train_df[feature_params.cont_features_kwargs.cont_features]

        if bins_params.bin_type =="unsupervised":
            bins = bin_computer.compute_unsupervised(X)
        else:
            y=train_df[feature_params.target_label].values
            tree_kwargs = feature_params.cont_features_kwargs.bin_config.tree_kwargs
            regression = feature_params.regression
            bins = bin_computer.compute_supervised(X, y, regression=regression, tree_kwargs=asdict(tree_kwargs))

        feature_params.cont_features_kwargs.embeddings_params.bins = bins

    # Model categories
    #if not feature_params.cat_features_kwargs.embeddings_params.cardinalities:
    cardinalities = [
        train_df[col].nunique() + (1 if col in encoder_params.binning_features else 0)
        for col in feature_params.cat_features_kwargs.cat_features
    ]
    feature_params.cat_features_kwargs.embeddings_params.cardinalities = cardinalities



    # Prepare data loaders
    if training_params.use_sampler:
        labels = train_df[feature_params.target_label].values
        class_counts = [sum(labels == i) for i in range(2)]
        class_weights = 1.0 / torch.tensor(class_counts, dtype=torch.float)
        sample_weights = class_weights[torch.tensor(labels, dtype=torch.long)]
        sampler = WeightedRandomSampler(weights=sample_weights, num_samples=len(train_df), replacement=True)
        shuffle = False
    else:
        sampler, shuffle = None, True

    data_loader_builder = DataLoaderBuilder(
        target_label=feature_params.target_label, logger=logger
    )

    train_loader = data_loader_builder.prepare_data_loader(
        train_df, training_params.batch_size,
        cat_indices=feature_params.cat_features_kwargs.cat_indices,
        numeric_indices=feature_params.cont_features_kwargs.numeric_indices,
        sampler=sampler, shuffle=shuffle
    )
    val_loader = data_loader_builder.prepare_data_loader(
        val_df, training_params.test_batch_size,
        cat_indices=feature_params.cat_features_kwargs.cat_indices,
        numeric_indices=feature_params.cont_features_kwargs.numeric_indices,
        sampler=None, shuffle=False
    )
    test_loader = data_loader_builder.prepare_data_loader(
        test_df, training_params.test_batch_size,
        cat_indices=feature_params.cat_features_kwargs.cat_indices,
        numeric_indices=feature_params.cont_features_kwargs.numeric_indices,
        sampler=None, shuffle=False
    )

    # Build model and trainer
    trainer = build_model_and_trainer(model_params, training_params, feature_params, fold)

    # Train the model with early stopping
    early_stopping = EarlyStopping(
        patience=training_params.patience,
        delta=training_params.delta,
        path=save_path,
        monitor=training_params.monitor,
    )

    trainer.train(
        train_loader=train_loader,
        val_loader=val_loader,
        epochs=training_params.epochs,
        early_stopping=early_stopping,
    )

    # Load the best model and evaluate
    model = trainer.load_best_model(save_path, training_params.monitor)
    _, val_metrics, val_preds = trainer.validate(val_loader)
    test_preds = trainer.predict(test_loader)

    return {
        "encoder": encoder,
        "model": model,
        "trainer": trainer,
        "fold": fold,
        "best_model_path": save_path,
        "auc": val_metrics.get("auc", 0),
        "f1": val_metrics.get("f1", 0),
        "accuracy": val_metrics.get("accuracy", 0),
        "val_preds": val_preds,
        "test_preds": test_preds,
    }

