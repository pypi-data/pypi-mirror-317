
def initialize_optimizer(model: nn.Module, optimizer_config: OptimizerConfig) -> torch.optim.Optimizer:
    """
    Initialize the optimizer using the OptimizerConfig.

    Args:
        model (nn.Module): The model whose parameters will be optimized.
        optimizer_config (OptimizerConfig): Configuration for the optimizer.

    Returns:
        torch.optim.Optimizer: Configured optimizer.
    """
    return torch.optim.AdamW(
        model.parameters(),
        lr=optimizer_config.lr,
        weight_decay=optimizer_config.weight_decay,
    )


def initialize_loss(loss_config: LossConfig) -> nn.Module:
    """
    Initialize the loss function using the LossConfig.

    Args:
        loss_config (LossConfig): Configuration for the loss function.

    Returns:
        nn.Module: Configured loss function.
    """
    if loss_config.type == LossType.FOCAL:
        if loss_config.gamma is None or loss_config.alpha is None:
            raise ValueError("Focal loss requires 'gamma' and 'alpha' to be specified in LossConfig.")
        return FocalLoss(
            gamma=loss_config.gamma,
            alpha=loss_config.alpha,
        )
    elif loss_config.type == LossType.BCE:
        return nn.BCEWithLogitsLoss()
    else:
        raise ValueError(f"Unsupported loss type: {loss_config.type}")



def initialize_scheduler(
    optimizer: torch.optim.Optimizer,
    scheduler_config: SchedulerConfig
) -> Optional[torch.optim.lr_scheduler._LRScheduler]:
    """
    Initialize and return a learning rate scheduler using the SchedulerConfig.

    Args:
        optimizer (torch.optim.Optimizer): The optimizer to which the scheduler is applied.
        scheduler_config (SchedulerConfig): Configuration for the learning rate scheduler.

    Returns:
        Optional[torch.optim.lr_scheduler._LRScheduler]: Configured scheduler or None if type is "none".
    """
    if scheduler_config.type == SchedulerType.NONE:
        return None

    if scheduler_config.type == SchedulerType.COSINE:
        if scheduler_config.T_max is None:
            raise ValueError("CosineAnnealingLR requires 'T_max' to be specified in SchedulerConfig.")
        return torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=scheduler_config.T_max,
            eta_min=scheduler_config.eta_min or 0,
        )

    if scheduler_config.type == SchedulerType.REDUCE_ON_PLATEAU:
        return torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode=scheduler_config.monitor_mode,
            factor=scheduler_config.factor,
            patience=scheduler_config.patience,
            threshold=1e-4,  # Optional: Expose threshold to SchedulerConfig
            min_lr=0,        # Optional: Expose min_lr to SchedulerConfig
        )

    if scheduler_config.type == SchedulerType.STEP:
        if scheduler_config.step_size is None or scheduler_config.gamma is None:
            raise ValueError("StepLR requires 'step_size' and 'gamma' to be specified in SchedulerConfig.")
        return torch.optim.lr_scheduler.StepLR(
            optimizer,
            step_size=scheduler_config.step_size,
            gamma=scheduler_config.gamma,
        )

    if scheduler_config.type == SchedulerType.M_STEP:
        if scheduler_config.step_size is None or scheduler_config.gamma is None:
            raise ValueError("MultiStepLR requires 'milestones' and 'gamma' to be specified in SchedulerConfig.")
        return torch.optim.lr_scheduler.MultiStepLR(
            optimizer,
            milestones=scheduler_config.step_size,
            gamma=scheduler_config.gamma,
        )

    if scheduler_config.type == SchedulerType.EXPONENTIAL:
        if scheduler_config.gamma is None:
            raise ValueError("ExponentialLR requires 'gamma' to be specified in SchedulerConfig.")
        return torch.optim.lr_scheduler.ExponentialLR(
            optimizer,
            gamma=scheduler_config.gamma,
        )

    if scheduler_config.type == SchedulerType.CYCLIC:
        if not all([scheduler_config.base_lr, scheduler_config.max_lr, scheduler_config.step_size_up]):
            raise ValueError(
                "CyclicLR requires 'base_lr', 'max_lr', and 'step_size_up' to be specified in SchedulerConfig."
            )
        return torch.optim.lr_scheduler.CyclicLR(
            optimizer,
            base_lr=scheduler_config.base_lr,
            max_lr=scheduler_config.max_lr,
            step_size_up=scheduler_config.step_size_up,
            mode=scheduler_config.mode or "triangular",
        )

    raise ValueError(f"Unsupported scheduler type: {scheduler_config.type}")
