class CreateDataset(Dataset):
    def __init__(self, X, y=None, cat_indices=None, numeric_indices=None):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32) if y is not None else None
        self.cat_indices = cat_indices
        self.numeric_indices = numeric_indices

        if y is not None and len(self.X) != len(self.y):
            raise ValueError("Features and target must have the same length.")

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        X = self.X[idx]

        X_categ = (
            X[self.cat_indices].long() if self.cat_indices else None
        )
        X_numer = (
            X[self.numeric_indices] if self.numeric_indices else None
        )

        if self.y is not None:
            y = self.y[idx]
            return X_categ, X_numer, y

        return X_categ, X_numer



class DataLoaderBuilder:
    def __init__(self, target_label, logger=None):
        self.logger = logger
        self.target_label = target_label
        self.dataset = None

    def prepare_data_loader(
        self, X, batch_size, cat_indices=None, numeric_indices=None, sampler=None, shuffle=False
    ):
        """
        Prepares a DataLoader for a given dataset.
        """
        if not self.target_label:
            if self.logger:
                self.logger.error("target_label must be provided in params.")
            raise ValueError("target_label must be provided in params.")

        validate_positive(batch_size, 'batch_size')

        if self.target_label in X.columns:
            y = X[self.target_label].values
            X = X.drop(self.target_label, axis=1).values
        else:
            y = None
            X = X.values

        self.dataset = CreateDataset(
            X, y, cat_indices=cat_indices, numeric_indices=numeric_indices
        )

        data_loader = DataLoader(
            self.dataset, batch_size=batch_size, sampler=sampler, shuffle=shuffle
        )

        return data_loader

