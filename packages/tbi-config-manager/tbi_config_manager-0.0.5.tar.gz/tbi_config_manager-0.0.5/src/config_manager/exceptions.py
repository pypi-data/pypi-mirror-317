class ConfigError(Exception):
    """Base exception class for configuration errors"""

    pass


class ConfigNotFoundError(ConfigError):
    """Exception for configuration not found"""

    pass


class ProviderError(ConfigError):
    """Error related to provider"""

    pass
