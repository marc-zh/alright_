"""
Integration Unit Tests for Utils Module

Tests integration between utils and other modules using Arrange-Act-Assert pattern.

Run with:
    pytest tests/test_integration_utils.py -v
"""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import (
    validate_address,
    validate_private_key,
    format_price,
    format_usdc,
    truncate_address,
    truncate_token_id,
)
from src.config import Config


class TestValidateAddressIntegration:
    """Integration tests for address validation."""

    def test_validate_address_with_config(self):
        """Test address validation with Config integration."""
        # Arrange
        config = Config(safe_address="0x1234567890123456789012345678901234567890")
        test_address = config.safe_address

        # Act
        result = validate_address(test_address)

        # Assert
        assert result is True

    def test_validate_invalid_address_from_config(self):
        """Test that invalid address from config fails validation."""
        # Arrange
        config = Config(safe_address="invalid_address")
        test_address = config.safe_address

        # Act
        result = validate_address(test_address)

        # Assert
        assert result is False

    def test_validate_address_case_insensitive(self):
        """Test that address validation is case-insensitive."""
        # Arrange
        lowercase = "0x1234567890123456789012345678901234567890"
        uppercase = "0xABCDEF1234567890ABCDEF1234567890ABCDEF12"
        mixed = "0xAbCdEf1234567890AbCdEf1234567890AbCdEf12"

        # Act
        result_lower = validate_address(lowercase)
        result_upper = validate_address(uppercase)
        result_mixed = validate_address(mixed)

        # Assert
        assert result_lower is True
        assert result_upper is True
        assert result_mixed is True


class TestValidatePrivateKeyIntegration:
    """Integration tests for private key validation."""

    def test_validate_key_normalization(self):
        """Test that keys are normalized with 0x prefix."""
        # Arrange
        key_without_prefix = "a" * 64

        # Act
        is_valid, result = validate_private_key(key_without_prefix)

        # Assert
        assert is_valid is True
        assert result.startswith("0x")
        assert len(result) == 66

    def test_validate_key_with_prefix_preserved(self):
        """Test that keys with 0x prefix are handled correctly."""
        # Arrange
        key_with_prefix = "0x" + "a" * 64

        # Act
        is_valid, result = validate_private_key(key_with_prefix)

        # Assert
        assert is_valid is True
        assert result == key_with_prefix

    def test_validate_key_uppercase_conversion(self):
        """Test that uppercase keys are converted to lowercase."""
        # Arrange
        uppercase_key = "A" * 64

        # Act
        is_valid, result = validate_private_key(uppercase_key)

        # Assert
        assert is_valid is True
        assert result.islower()
        assert result == "0x" + "a" * 64


class TestFormatPriceIntegration:
    """Integration tests for price formatting."""

    def test_format_price_with_market_data(self):
        """Test formatting price with market-like data."""
        # Arrange
        market_data = {
            "price": 0.65,
            "side": "BUY",
        }

        # Act
        formatted = format_price(market_data["price"])

        # Assert
        assert "0.65" in formatted
        assert "65%" in formatted

    def test_format_price_edge_cases(self):
        """Test formatting edge case prices."""
        # Arrange
        edge_prices = [0.0, 0.01, 0.99, 1.0]

        # Act & Assert
        for price in edge_prices:
            formatted = format_price(price)
            assert "%" in formatted
            assert str(price) in formatted or str(int(price * 100)) in formatted

    def test_format_price_custom_decimals(self):
        """Test formatting with custom decimal places."""
        # Arrange
        price = 0.654321
        decimals = 4

        # Act
        formatted = format_price(price, decimals=decimals)

        # Assert
        assert "0.6543" in formatted

    def test_format_price_negative(self):
        """Test formatting negative price (should handle gracefully)."""
        # Arrange
        price = -0.10

        # Act
        formatted = format_price(price)

        # Assert
        assert "%" in formatted  # Should still format, even if negative


class TestFormatUsdcIntegration:
    """Integration tests for USDC formatting."""

    def test_format_usdc_with_order_size(self):
        """Test formatting USDC with order sizes."""
        # Arrange
        order_sizes = [1.0, 10.5, 100.0, 1000.0]

        # Act & Assert
        for size in order_sizes:
            formatted = format_usdc(size)
            assert "$" in formatted
            assert "USDC" in formatted
            assert str(size) in formatted or str(int(size)) in formatted

    def test_format_usdc_zero(self):
        """Test formatting zero USDC."""
        # Arrange
        amount = 0.0

        # Act
        formatted = format_usdc(amount)

        # Assert
        assert "$0.00" in formatted

    def test_format_usdc_small_amounts(self):
        """Test formatting small USDC amounts."""
        # Arrange
        small_amounts = [0.01, 0.001, 0.0001]

        # Act & Assert
        for amount in small_amounts:
            formatted = format_usdc(amount)
            assert "$" in formatted
            assert "USDC" in formatted


class TestTruncateAddressIntegration:
    """Integration tests for address truncation."""

    def test_truncate_with_config_address(self):
        """Test truncating address from config."""
        # Arrange
        config = Config(safe_address="0x1234567890123456789012345678901234567890")
        full_address = config.safe_address

        # Act
        truncated = truncate_address(full_address)

        # Assert
        assert "..." in truncated
        assert len(truncated) < len(full_address)

    def test_truncate_custom_chars(self):
        """Test truncating with custom character count."""
        # Arrange
        address = "0x1234567890123456789012345678901234567890"
        chars = 4

        # Act
        truncated = truncate_address(address, chars=chars)

        # Assert
        assert truncated == "0x1234...7890"

    def test_truncate_short_address(self):
        """Test that short addresses are not truncated."""
        # Arrange
        short_address = "0x1234"

        # Act
        truncated = truncate_address(short_address)

        # Assert
        assert truncated == short_address

    def test_truncate_empty_address(self):
        """Test truncating empty address."""
        # Arrange
        empty_address = ""

        # Act
        truncated = truncate_address(empty_address)

        # Assert
        assert truncated == ""


class TestTruncateTokenIdIntegration:
    """Integration tests for token ID truncation."""

    def test_truncate_token_id_with_market_data(self):
        """Test truncating token ID from market data."""
        # Arrange
        market = {
            "token_ids": {
                "up": "1234567890123456789012345678901234567890123456789012345678901234",
                "down": "9876543210987654321098765432109876543210987654321098765432109876",
            }
        }

        # Act
        truncated_up = truncate_token_id(market["token_ids"]["up"])
        truncated_down = truncate_token_id(market["token_ids"]["down"])

        # Assert
        assert "..." in truncated_up
        assert "..." in truncated_down
        assert len(truncated_up) < len(market["token_ids"]["up"])

    def test_truncate_token_id_custom_chars(self):
        """Test truncating token ID with custom character count."""
        # Arrange
        token_id = "123456789012345678901234567890"
        chars = 4

        # Act
        truncated = truncate_token_id(token_id, chars=chars)

        # Assert
        assert truncated == "1234..."

    def test_truncate_short_token_id(self):
        """Test that short token IDs are not truncated."""
        # Arrange
        short_token = "12345"

        # Act
        truncated = truncate_token_id(short_token)

        # Assert
        assert truncated == short_token


class TestUtilsErrorHandling:
    """Tests for error handling in utils."""

    def test_validate_address_none_input(self):
        """Test that None input is handled gracefully."""
        # Arrange
        address = None

        # Act
        result = validate_address(address)

        # Assert
        assert result is False

    def test_validate_private_key_empty_input(self):
        """Test that empty key is rejected."""
        # Arrange
        empty_key = ""

        # Act
        is_valid, result = validate_private_key(empty_key)

        # Assert
        assert is_valid is False
        assert "empty" in result.lower()

    def test_validate_private_key_invalid_characters(self):
        """Test that key with invalid characters is rejected."""
        # Arrange
        invalid_key = "0x" + "g" * 64  # 'g' is not valid hex

        # Act
        is_valid, result = validate_private_key(invalid_key)

        # Assert
        assert is_valid is False
        assert "invalid" in result.lower()

    def test_format_price_invalid_type(self):
        """Test formatting with invalid input type."""
        # Arrange
        invalid_price = "not_a_number"

        # Act & Assert
        with pytest.raises((TypeError, ValueError)):
            format_price(invalid_price)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
