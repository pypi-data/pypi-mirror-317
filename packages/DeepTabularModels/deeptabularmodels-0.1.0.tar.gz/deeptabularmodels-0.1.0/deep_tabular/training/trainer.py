class EarlyStopping:
    def __init__(self, patience=5, delta=0, path="best_model.pth", monitor="loss"):
        """
        Args:
            patience (int): How many epochs to wait after last improvement.
            delta (float): Minimum change to qualify as an improvement.
            path (str): Path to save the best model.
            monitor (str): Metric to monitor ("loss", "auc", "accuracy", "f1", etc.).
        """
        self.patience = patience
        self.delta = delta
        self.path = path
        self.monitor = monitor

        # Determine mode based on the metric
        self.mode = "min" if self.monitor == "loss" else "max"
        self.best_score = None
        self.counter = 0
        self.early_stop = False

    def __call__(self, metric_value, model, optimizer):
        """
        Args:
            metric_value (float): The value of the monitored metric for the current epoch.
            model (torch.nn.Module): The model to save.
            optimizer (torch.optim.Optimizer): The optimizer to save.
        """

        # Adjust the score for comparison based on mode
        score = metric_value if self.mode == "max" else -metric_value

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(metric_value, model, optimizer)
        elif score < self.best_score + self.delta:
            self.counter += 1
            if self.counter >= self.patience:
                print("Early stopping triggered.")
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(metric_value, model, optimizer)
            self.counter = 0

    def save_checkpoint(self, metric_value, model, optimizer):
        """Save model and optimizer when the monitored metric improves."""
        checkpoint = {
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            self.monitor: metric_value,
        }
        torch.save(checkpoint, self.path)
        print(f"Validation {self.monitor}: {metric_value:.6f}, Best {self.monitor} so far: {self.best_score:.6f}")
        print(f'Validation {self.monitor} improved. Saving model...')



class BaseTrainer(ABC):
    def __init__(self, model, device, criterion, optimizer, scheduler=None, max_norm=1.0, writer_path='runs'):
        if max_norm <= 0:
            raise ValueError("max_norm must be greater than 0.")

        self.model = model.to(device)
        self.device = device
        self.criterion = criterion
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.max_norm = max_norm
        self.scaler = GradScaler()
        self.writer = SummaryWriter(log_dir=writer_path)

    @abstractmethod
    def compute_metrics(self, labels, preds):
        """Compute task-specific metrics."""
        pass

    def train_epoch(self, train_loader):
        self.model.train()
        running_loss = 0.0
        rolling_loss = []
        all_labels, all_preds = [], []

        train_loader_tqdm = tqdm(train_loader, desc="Training", leave=False)
        for *inputs, y in train_loader_tqdm:
            inputs = [self._process(tensor) for tensor in inputs]
            y = self._process(y)

            with autocast():
                outputs = self.model(*inputs).squeeze(-1)
                loss = self.criterion(outputs, y)

            if not torch.isfinite(loss):
                print(f"Warning: Non-finite loss detected!")
                break

            self.optimizer.zero_grad()
            self.scaler.scale(loss).backward()
            self.scaler.unscale_(self.optimizer)
            clip_grad_norm_(self.model.parameters(), self.max_norm)
            self.scaler.step(self.optimizer)
            self.scaler.update()

            running_loss += loss.item()
            rolling_loss.append(loss.item())
            if len(rolling_loss) > 10:
                rolling_loss.pop(0)
            avg_loss = np.mean(rolling_loss)
            train_loader_tqdm.set_postfix({"Rolling Loss": f"{avg_loss:.4f}"})

            all_labels.extend(y.cpu())
            all_preds.extend(outputs.cpu())

        train_loss = running_loss / len(train_loader)
        train_metrics = self.compute_metrics(torch.stack(all_labels), torch.stack(all_preds))
        return train_loss, train_metrics

    def validate(self, val_loader, epoch=None):
        self.model.eval()
        running_loss = 0.0
        all_labels, all_preds = [], []

        val_loader_tqdm = tqdm(val_loader, desc="Validating", leave=False)
        with torch.no_grad():
            for *inputs, y in val_loader_tqdm:
                inputs = [self._process(tensor) for tensor in inputs]
                y = self._process(y)
                outputs = self.model(*inputs).squeeze(-1)
                loss = self.criterion(outputs, y)
                running_loss += loss.item()

                all_labels.extend(y.cpu())
                all_preds.extend(outputs.cpu())

        val_loss = running_loss / len(val_loader) if len(val_loader) > 0 else float('inf')
        val_metrics = self.compute_metrics(torch.stack(all_labels), torch.stack(all_preds))

        if self.writer and epoch is not None:
            self.writer.add_histogram("Validation/Predictions", torch.stack(all_preds).numpy(), epoch)

        return val_loss, val_metrics, torch.stack(all_preds)

    def predict(self, test_loader):
        self.model.eval()
        all_preds = []

        test_loader_tqdm = tqdm(test_loader, desc="Predicting", leave=False)
        with torch.no_grad():
            for inputs in test_loader_tqdm:
                inputs = [self._process(tensor) for tensor in inputs]
                outputs = self.model(*inputs).squeeze(-1)
                all_preds.extend(outputs.cpu())

        return torch.stack(all_preds).numpy()

    def train(self, train_loader, val_loader, epochs, early_stopping):
        for epoch in range(epochs):
            print(f"\nEpoch {epoch + 1}/{epochs}")
            train_loss, train_metrics = self.train_epoch(train_loader)
            val_loss, val_metrics, _ = self.validate(val_loader, epoch)

            print(f"Train Loss: {train_loss:.4f}, Train Metrics: {train_metrics}")
            print(f"Val Loss: {val_loss:.4f}, Val Metrics: {val_metrics}")

            self._log_metrics(train_loss, train_metrics, val_loss, val_metrics, epoch)

            if self.scheduler:
                if isinstance(self.scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
                    self.scheduler.step(val_loss)
                else:
                    self.scheduler.step()

            early_stopping(val_loss, model=self.model, optimizer=self.optimizer)
            if early_stopping.early_stop:
                print("Early stopping triggered.")
                break

        self.writer.close()

    def _log_metrics(self, train_loss, train_metrics, val_loss, val_metrics, epoch):
        self.writer.add_scalar('Train/Loss', train_loss, epoch)
        for key, value in train_metrics.items():
            self.writer.add_scalar(f'Train/{key.upper()}', value, epoch)

        self.writer.add_scalar('Validation/Loss', val_loss, epoch)
        for key, value in val_metrics.items():
            self.writer.add_scalar(f'Validation/{key.upper()}', value, epoch)

    def _process(self, tensor):
        return tensor.to(self.device) if tensor is not None and tensor.numel() > 0 else None


