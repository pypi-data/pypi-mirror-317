# Configuration manager that orchestrates multiple providers to retrieve config values
from enum import Enum
from typing import Any, List, Optional, TypeVar, Union, overload
from pathlib import Path

from .providers.factory import ProviderFactory

from .providers.composite import CompositeProvider
from .typing import ConfigValue, PathLike, Provider
from .exceptions import ConfigError, ConfigNotFoundError
from .utils.logger import setup_logger
from .utils.cache import cached_property

logger = setup_logger()
T = TypeVar("T")


class ConfigManager:
    def __init__(
        self,
        providers: List[Provider] = [Provider.ENV],  # renamed from provider_order
        env_file: Optional[PathLike] = None,
        project_id: Optional[str] = None,
        credentials_path: Optional[str] = None,
        secret_prefix: str = "",
        cache_enabled: bool = True,
    ):
        """
        Args:
            providers: List of provider types to use for configuration
            env_file: Path to .env file
            project_id: GCP project ID (only if GCP in providers)
            credentials_path: GCP credentials path
            secret_prefix: Secret prefix for GCP
            cache_enabled: Enable caching
        """
        self.cache_enabled = cache_enabled
        self._setup_providers(
            providers, env_file, project_id, credentials_path, secret_prefix
        )

    def _setup_providers(
        self,
        providers: List[Provider],
        env_file: Optional[PathLike],
        project_id: Optional[str],
        credentials_path: Optional[str],
        secret_prefix: str,
    ) -> None:
        """Setup configuration providers"""
        provider_instances = []

        kwargs = {
            "env_file": env_file,
            "project_id": project_id,
            "credentials_path": credentials_path,
            "secret_prefix": secret_prefix,
        }

        for provider_type in providers:
            provider = ProviderFactory.create(provider_type, **kwargs)
            if provider:
                provider_instances.append(provider)

        if not provider_instances:
            raise ConfigError("No configuration providers available")

        self.provider = CompositeProvider(provider_instances)

    @overload
    def get(self, key: str) -> Optional[ConfigValue]: ...

    @overload
    def get(self, key: str, default: T) -> Union[ConfigValue, T]: ...

    def get(self, key: str, default: Any = None) -> Union[ConfigValue, Any]:
        """
        Get configuration value

        Args:
            key: Configuration key
            default: Default value

        Returns:
            Configuration value
        """
        try:
            # Get value from providers in order until a non-None value is found
            if isinstance(self.provider, CompositeProvider):
                for provider in self.provider.providers:
                    value = provider.get(key)
                    if value is not None:
                        return value
            return default
        except Exception as e:
            logger.error(f"Error getting config {key}: {e}")
            return default

    def __getattr__(self, name: str) -> Any:
        """Support accessing configuration as attributes"""
        return self.get(name)

    def require(self, key: str) -> ConfigValue:
        """
        Get required configuration value; raise exception if not found

        Args:
            key: Configuration key

        Returns:
            Configuration value

        Raises:
            ConfigNotFoundError: If configuration not found
        """
        value = self.get(key)
        if value is None:
            raise ConfigNotFoundError(f"Required config {key} not found")
        return value

    def reload(self) -> None:
        """Reload configurations from all providers"""
        if isinstance(self.provider, CompositeProvider):
            for provider in self.provider.providers:
                try:
                    provider.reload()
                except Exception as e:
                    logger.error(f"Failed to reload provider {provider.name}: {e}")
