"""
ConfigFake - Test Double for Configuration

A fake implementation of Config for testing purposes.
Provides in-memory configuration without needing files or environment variables.
"""

from typing import Optional, Dict, Any


class ConfigFake:
    """
    Fake configuration for testing.

    Provides a simple in-memory configuration that mimics the behavior
    of the real Config class but doesn't require files or env vars.
    """

    def __init__(
        self,
        safe_address: Optional[str] = None,
        builder_api_key: Optional[str] = None,
        builder_api_secret: Optional[str] = None,
        builder_api_passphrase: Optional[str] = None,
    ):
        """
        Initialize fake configuration.

        Args:
            safe_address: Polymarket Safe address
            builder_api_key: Builder API key (optional)
            builder_api_secret: Builder API secret (optional)
            builder_api_passphrase: Builder API passphrase (optional)
        """
        self.safe_address = safe_address or "0x1234567890123456789012345678901234567890"
        self.builder_api_key = builder_api_key or "test_api_key"
        self.builder_api_secret = builder_api_secret or "test_api_secret"
        self.builder_api_passphrase = builder_api_passphrase or "test_passphrase"

        # Internal storage for additional config
        self._config: Dict[str, Any] = {
            "safe_address": self.safe_address,
            "builder": {
                "api_key": self.builder_api_key,
                "api_secret": self.builder_api_secret,
                "api_passphrase": self.builder_api_passphrase,
            },
        }

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        if key == "safe_address":
            return self.safe_address

        if key in self._config:
            return self._config[key]

        # Check nested builder config
        if key in ["builder_api_key", "builder_api_secret", "builder_api_passphrase"]:
            builder_key = key.replace("builder_", "")
            return self._config.get("builder", {}).get(builder_key, default)

        return default

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.

        Args:
            key: Configuration key
            value: Value to set
        """
        if key == "safe_address":
            self.safe_address = value
            self._config["safe_address"] = value
        else:
            self._config[key] = value

    def has_builder_credentials(self) -> bool:
        """
        Check if builder credentials are configured.

        Returns:
            True if builder credentials are set
        """
        return bool(
            self.builder_api_key
            and self.builder_api_secret
            and self.builder_api_passphrase
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.

        Returns:
            Dictionary representation of configuration
        """
        return self._config.copy()

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "ConfigFake":
        """
        Create ConfigFake from dictionary.

        Args:
            config_dict: Configuration dictionary

        Returns:
            ConfigFake instance
        """
        fake = cls()
        fake._config = config_dict.copy()

        # Extract safe_address if present
        if "safe_address" in config_dict:
            fake.safe_address = config_dict["safe_address"]

        # Extract builder credentials if present
        if "builder" in config_dict:
            builder = config_dict["builder"]
            fake.builder_api_key = builder.get("api_key")
            fake.builder_api_secret = builder.get("api_secret")
            fake.builder_api_passphrase = builder.get("api_passphrase")

        return fake
