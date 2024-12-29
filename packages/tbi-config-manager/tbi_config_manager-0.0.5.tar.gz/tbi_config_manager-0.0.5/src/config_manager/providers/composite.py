# Implements composite pattern to aggregate multiple config providers in priority order
from typing import List, Optional

from ..utils import logger
from .base import ConfigProvider
from ..typing import ConfigValue


class CompositeProvider(ConfigProvider):
    """Combine multiple configuration providers"""

    def __init__(self, providers: List[ConfigProvider]):
        """
        Initialize the composite provider

        Args:
            providers: List of providers, ordered by priority
        """
        self.providers = providers

    def get(self, key: str) -> Optional[ConfigValue]:
        for provider in self.providers:
            if provider.has(key):
                return provider.get(key)
        return None

    def has(self, key: str) -> bool:
        return any(provider.has(key) for provider in self.providers)

    @property
    def name(self) -> str:
        provider_names = ", ".join(p.name for p in self.providers)
        return f"Composite({provider_names})"

    def reload(self) -> None:
        """Reload the configurations of all child providers"""
        for provider in self.providers:
            try:
                provider.reload()
            except Exception as e:
                # If a provider fails to reload, continue with other providers
                logger.warning(f"Failed to reload provider {provider.name}: {e}")
