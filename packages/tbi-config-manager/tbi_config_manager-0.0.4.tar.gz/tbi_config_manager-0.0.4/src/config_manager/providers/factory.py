# Register and initialize providers in this file
from typing import Dict, Type, Optional, TypeVar

from ..utils import logger
from ..providers.env import EnvProvider
from ..providers.gcp import GCPProvider
from ..providers.base import ConfigProvider
from ..typing import Provider

T = TypeVar("T", bound=ConfigProvider)


class ProviderFactory:
    _registry: Dict[Provider, Type[ConfigProvider]] = {}

    @classmethod
    def register(cls, provider_type: Provider, provider_class: Type[T]) -> None:
        cls._registry[provider_type] = provider_class

    @classmethod
    def create(cls, provider_type: Provider, **kwargs) -> Optional[ConfigProvider]:
        if provider_type not in cls._registry:
            logger.warning(f"Provider type {provider_type} not registered")
            return None

        provider_class = cls._registry[provider_type]

        # Filter kwargs based on provider's __init__ parameters
        import inspect

        init_params = inspect.signature(provider_class.__init__).parameters
        filtered_kwargs = {
            key: value for key, value in kwargs.items() if key in init_params
        }

        return provider_class(**filtered_kwargs)


# Register providers here
ProviderFactory.register(Provider.ENV, EnvProvider)
ProviderFactory.register(Provider.GCP, GCPProvider)
