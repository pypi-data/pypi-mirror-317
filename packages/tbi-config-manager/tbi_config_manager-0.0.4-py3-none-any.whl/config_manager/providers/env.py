# Local environment configuration for the `.env` provider
import os
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

from .base import ConfigProvider
from ..typing import ConfigValue, PathLike
from ..exceptions import ConfigError


class EnvProvider(ConfigProvider):
    """Environment variable configuration provider"""

    def __init__(self, env_file: Optional[PathLike] = None):
        """
        Initialize the environment variable provider

        Args:
            env_file: Path to the .env file
        """
        self.env_file = Path(env_file) if env_file else None
        if self.env_file and self.env_file.exists():
            load_dotenv(self.env_file)

    def reload(self) -> None:
        """Reload the environment variables"""
        if self.env_file and self.env_file.exists():
            print(f"Reloading environment variables from {self.env_file}")
            load_dotenv(self.env_file, override=True)
        else:
            print("No .env file specified, using existing environment variables")

    def get(self, key: str) -> Optional[ConfigValue]:
        return os.getenv(key)

    def has(self, key: str) -> bool:
        return key in os.environ

    @property
    def name(self) -> str:
        return "Environment"
