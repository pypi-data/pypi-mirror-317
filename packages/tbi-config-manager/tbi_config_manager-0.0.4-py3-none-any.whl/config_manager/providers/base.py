# Abstract base class for configuration providers
from abc import ABC, abstractmethod
from typing import Optional
from ..typing import ConfigValue


class ConfigProvider(ABC):
    """Abstract base class for configuration providers"""

    @abstractmethod
    def reload(self) -> None:
        """Reload the configuration"""
        pass

    @abstractmethod
    def get(self, key: str) -> Optional[ConfigValue]:
        """Get the configuration value"""
        pass

    @abstractmethod
    def has(self, key: str) -> bool:
        """Check if the configuration exists"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name"""
        pass
