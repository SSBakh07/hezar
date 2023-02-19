from typing import Iterator

from torch import nn, optim

from hezar.utils.logging import get_logger

__all__ = [
    "models_registry",
    "preprocessors_registry",
    "criterions_registry",
    "optimizers_registry",
    "lr_schedulers_registry",
    "build_model",
    "build_preprocessor",
    "build_criterion",
    "build_optimizer",
    "build_scheduler",
    "get_model_config_class",
]

logger = get_logger(__name__)

models_registry = {}
preprocessors_registry = {}
criterions_registry = {
    "bce": nn.BCELoss,
    "nll": nn.NLLLoss,
    "cross_entropy": nn.CrossEntropyLoss,
    "mse": nn.MSELoss,
    "ctc": nn.CTCLoss,
}
optimizers_registry = {"adam": optim.Adam, "adamw": optim.AdamW, "sgd": optim.SGD}
lr_schedulers_registry = {
    "reduce_on_plateau": optim.lr_scheduler.ReduceLROnPlateau,
    "cosine_lr": optim.lr_scheduler.CosineAnnealingLR,
}


def build_model(name: str, config=None, **kwargs):
    """
    Build the model using its registry name. If config is None then the model is built using the default config. Notice
    that this function only builds the model and does not perform any weights loading/initialization unless these
    actions are done in the model's __init__ .

    Args:
        name (str): name of the model in the models' registry
        config (ModelConfig): a ModelConfig instance
        kwargs: extra config parameters that are loaded to the model

    Returns:
        A Model instance
    """

    config = config or models_registry[name]["config_class"]()
    model = models_registry[name]["model_class"](config, **kwargs)
    return model


def build_preprocessor(name: str, config=None, **kwargs):
    """
        Build the preprocessor using its registry name. If config is None then the preprocessor is built using the
        default config.

        Args:
            name (str): name of the preprocessor in the preprocessors' registry
            config (PreprocessorConfig): a PreprocessorConfig instance
            kwargs: extra config parameters that are loaded to the preprocessor

        Returns:
            A Preprocessor instance
        """

    config = config or preprocessors_registry[name]["config_class"]()
    preprocessor = preprocessors_registry[name]["preprocessor_class"](config, **kwargs)
    return preprocessor


def build_criterion(name: str, config=None):
    """
    Build the loss function using its registry name.

    Args:
        name (str): Name of the optimizer in the criterions_registry
        config (CriterionConfig): A CriterionConfig  instance

    Returns:
        An nn.Module instance
    """
    criterion = criterions_registry[name](**config.dict())
    return criterion


def build_optimizer(name: str, params: Iterator[nn.Parameter], config=None):
    """
    Build the optimizer using its registry name.

    Args:
        name (str): Name of the optimizer in the optimizers_registry
        params (Iterator[nn.Parameter]): Model parameters
        config (OptimizerConfig): An OptimizerConfig  instance

    Returns:
        An optim.Optimizer instance
    """
    optimizer = optimizers_registry[name](params, **config.dict())
    return optimizer


def build_scheduler(name: str, optimizer: optim.Optimizer, config=None):
    """
    Build the LR scheduler using its registry name.

    Args:
        name (str): Name of the optimizer in the lr_schedulers_registry
        optimizer (optim.Optimizer): The optimizer
        config (LRSchedulerConfig): An LRSchedulerConfig  instance

    Returns:
        An optim.lr_scheduler._LRScheduler instance
    """
    scheduler = lr_schedulers_registry[name](optimizer, **config.dict())
    return scheduler


def get_model_config_class(name: str):
    """
    Get the config class for a given model based on its registry name.

    Args:
        name (str): model's registry name

    Returns:
        A class of type :class:`hezar.Config`
    """
    config_cls = models_registry[name]["config_class"]
    return config_cls
