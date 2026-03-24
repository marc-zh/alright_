"""
Integration Tests with Test Doubles

Integration tests using Fakes, Stubs, and Mocks to test bot functionality
without real network connections or external dependencies.

Run with:
    pytest tests/test_integration_bot.py -v
"""

import asyncio
import sys
import pytest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.doubles.ConfigFake import ConfigFake
from tests.doubles.ApiClientStub import ApiClientStub
from tests.doubles.WebSocketMock import WebSocketMock
from src.utils import validate_address, format_price, format_usdc


class TestConfigFakeIntegration:
    """Integration tests using ConfigFake."""

    def test_config_fake_initialization(self):
        """Test ConfigFake initialization."""
        # Arrange
        fake_config = ConfigFake(
            safe_address="0xABCDEF1234567890ABCDEF1234567890ABCDEF12"
        )

        # Act
        address = fake_config.safe_address

        # Assert
        assert address == "0xABCDEF1234567890ABCDEF1234567890ABCDEF12"

    def test_config_fake_with_builder_credentials(self):
        """Test ConfigFake with builder credentials."""
        # Arrange
        fake_config = ConfigFake(
            builder_api_key="test_key",
            builder_api_secret="test_secret",
            builder_api_passphrase="test_passphrase",
        )

        # Act
        has_creds = fake_config.has_builder_credentials()

        # Assert
        assert has_creds is True

    def test_config_fake_get_set(self):
        """Test ConfigFake get/set operations."""
        # Arrange
        fake_config = ConfigFake()

        # Act
        fake_config.set("custom_key", "custom_value")
        value = fake_config.get("custom_key")

        # Assert
        assert value == "custom_value"

    def test_config_fake_to_dict(self):
        """Test ConfigFake to_dict conversion."""
        # Arrange
        fake_config = ConfigFake(safe_address="0x123...")

        # Act
        config_dict = fake_config.to_dict()

        # Assert
        assert "safe_address" in config_dict
        assert "builder" in config_dict

    def test_config_fake_from_dict(self):
        """Test creating ConfigFake from dictionary."""
        # Arrange
        config_dict = {
            "safe_address": "0xABC...",
            "builder": {
                "api_key": "key",
                "api_secret": "secret",
                "api_passphrase": "pass",
            },
        }

        # Act
        fake_config = ConfigFake.from_dict(config_dict)

        # Assert
        assert fake_config.safe_address == "0xABC..."
        assert fake_config.has_builder_credentials() is True


class TestApiClientStubIntegration:
    """Integration tests using ApiClientStub."""

    def test_api_stub_get_order_book(self):
        """Test getting order book from stub."""
        # Arrange
        api_stub = ApiClientStub()
        token_id = "test_token_123"

        # Act
        order_book = api_stub.get_order_book(token_id)

        # Assert
        assert "bids" in order_book
        assert "asks" in order_book
        assert order_book["asset_id"] == token_id

    def test_api_stub_place_order(self):
        """Test placing order through stub."""
        # Arrange
        api_stub = ApiClientStub()
        token_id = "test_token_123"

        # Act
        result = api_stub.place_order(
            token_id=token_id,
            price=0.65,
            size=10.0,
            side="BUY"
        )

        # Assert
        assert result["success"] is True
        assert "orderId" in result

    def test_api_stub_call_tracking(self):
        """Test that stub tracks API calls."""
        # Arrange
        api_stub = ApiClientStub()
        token_id = "test_token_123"

        # Act
        api_stub.get_market_price(token_id)
        api_stub.get_market_price(token_id)
        api_stub.get_market_price(token_id)

        # Assert
        assert api_stub.was_called("get_market_price") is True
        assert api_stub.get_call_count("get_market_price") == 3

    def test_api_stub_last_call_args(self):
        """Test getting last call arguments."""
        # Arrange
        api_stub = ApiClientStub()
        token_id = "test_token_123"

        # Act
        api_stub.place_order(token_id, 0.70, 20.0, "SELL")
        last_args = api_stub.get_last_call_args("place_order")

        # Assert
        assert last_args is not None
        assert last_args["token_id"] == token_id
        assert last_args["price"] == 0.70
        assert last_args["size"] == 20.0
        assert last_args["side"] == "SELL"

    def test_api_stub_custom_response(self):
        """Test setting custom response."""
        # Arrange
        api_stub = ApiClientStub()
        custom_response = {
            "success": False,
            "message": "Custom error"
        }

        # Act
        api_stub.set_response("place_order", custom_response)
        result = api_stub.place_order("token", 0.5, 10, "BUY")

        # Assert
        assert result["success"] is False
        assert result["message"] == "Custom error"


class TestWebSocketMockIntegration:
    """Integration tests using WebSocketMock."""

    @pytest.mark.asyncio
    async def test_websocket_mock_connect(self):
        """Test WebSocket mock connection."""
        # Arrange
        ws_mock = WebSocketMock()

        # Act
        await ws_mock.connect()

        # Assert
        assert ws_mock.is_connected is True
        ws_mock.assert_connected()

    @pytest.mark.asyncio
    async def test_websocket_mock_subscribe(self):
        """Test WebSocket mock subscription."""
        # Arrange
        ws_mock = WebSocketMock()
        await ws_mock.connect()

        # Act
        await ws_mock.subscribe(["token_1", "token_2", "token_3"])

        # Assert
        assert ws_mock.get_subscription_count() == 3
        ws_mock.assert_subscribed("token_1")
        ws_mock.assert_subscribed("token_2")
        ws_mock.assert_subscribed("token_3")

    @pytest.mark.asyncio
    async def test_websocket_mock_unsubscribe(self):
        """Test WebSocket mock unsubscription."""
        # Arrange
        ws_mock = WebSocketMock()
        await ws_mock.connect()
        await ws_mock.subscribe(["token_1", "token_2"])

        # Act
        await ws_mock.unsubscribe(["token_1"])

        # Assert
        ws_mock.assert_not_subscribed("token_1")
        ws_mock.assert_subscribed("token_2")

    @pytest.mark.asyncio
    async def test_websocket_mock_message_handling(self):
        """Test WebSocket mock message handling."""
        # Arrange
        ws_mock = WebSocketMock()
        await ws_mock.connect()

        test_message = {
            "event_type": "book",
            "asset_id": "token_123",
            "bids": [{"price": 0.65, "size": 100}],
            "asks": [{"price": 0.66, "size": 100}],
        }

        # Act
        await ws_mock.simulate_message(test_message)

        # Assert
        assert len(ws_mock.get_received_messages()) == 1
        ws_mock.on_book.assert_called_once()

    @pytest.mark.asyncio
    async def test_websocket_mock_callback_tracking(self):
        """Test WebSocket mock callback tracking."""
        # Arrange
        ws_mock = WebSocketMock()
        await ws_mock.connect()
        await ws_mock.subscribe(["token_1"])

        test_message = {
            "event_type": "book",
            "asset_id": "token_1",
        }

        # Act
        await ws_mock.simulate_message(test_message)

        # Assert
        ws_mock.assert_callback_called("on_book")

    @pytest.mark.asyncio
    async def test_websocket_mock_reset(self):
        """Test WebSocket mock reset."""
        # Arrange
        ws_mock = WebSocketMock()
        await ws_mock.connect()
        await ws_mock.subscribe(["token_1", "token_2"])

        # Act
        ws_mock.reset()

        # Assert
        assert ws_mock.is_connected is False
        assert ws_mock.get_subscription_count() == 0


class TestBotIntegrationWithDoubles:
    """Integration tests combining multiple test doubles."""

    def test_bot_initialization_with_fake_config(self):
        """Test bot initialization with fake config."""
        # Arrange
        fake_config = ConfigFake(
            safe_address="0x1234567890123456789012345678901234567890"
        )

        # Act
        is_valid = validate_address(fake_config.safe_address)

        # Assert
        assert is_valid is True

    def test_bot_order_placement_with_stub_api(self):
        """Test order placement with API stub."""
        # Arrange
        api_stub = ApiClientStub()
        token_id = "test_token_123"

        # Act
        order_result = api_stub.place_order(
            token_id=token_id,
            price=0.65,
            size=10.0,
            side="BUY"
        )

        # Assert
        assert order_result["success"] is True
        assert api_stub.was_called("place_order")

    @pytest.mark.asyncio
    async def test_bot_websocket_workflow_with_mock(self):
        """Test complete WebSocket workflow with mock."""
        # Arrange
        ws_mock = WebSocketMock()

        # Act - Simulate connection workflow
        await ws_mock.connect()
        await ws_mock.subscribe(["token_1", "token_2"])

        # Simulate receiving market data
        book_message = {
            "event_type": "book",
            "asset_id": "token_1",
            "bids": [{"price": 0.65, "size": 100}],
            "asks": [{"price": 0.66, "size": 100}],
        }
        await ws_mock.simulate_message(book_message)

        # Assert
        ws_mock.assert_connected()
        ws_mock.assert_subscribed("token_1")
        ws_mock.assert_subscribed("token_2")
        ws_mock.on_book.assert_called_once()

    def test_bot_price_formatting_with_doubles(self):
        """Test price formatting with test doubles."""
        # Arrange
        api_stub = ApiClientStub()
        token_id = "test_token_123"

        # Act
        price = api_stub.get_market_price(token_id)
        formatted = format_price(price)

        # Assert
        assert "%" in formatted
        assert "0.65" in formatted

    def test_bot_usdc_formatting_with_doubles(self):
        """Test USDC formatting with test doubles."""
        # Arrange
        api_stub = ApiClientStub()
        order_size = 50.0

        # Act
        formatted = format_usdc(order_size)

        # Assert
        assert "$" in formatted
        assert "USDC" in formatted
        assert "50.00" in formatted


class TestErrorHandlingWithDoubles:
    """Test error handling scenarios using test doubles."""

    def test_api_stub_error_response(self):
        """Test API stub with error response."""
        # Arrange
        api_stub = ApiClientStub()
        error_response = {
            "success": False,
            "message": "Insufficient balance"
        }
        api_stub.set_response("place_order", error_response)

        # Act
        result = api_stub.place_order("token", 0.5, 1000, "BUY")

        # Assert
        assert result["success"] is False
        assert "Insufficient balance" in result["message"]

    @pytest.mark.asyncio
    async def test_websocket_mock_disconnection_handling(self):
        """Test handling WebSocket disconnection."""
        # Arrange
        ws_mock = WebSocketMock()
        await ws_mock.connect()
        await ws_mock.subscribe(["token_1"])

        # Act
        await ws_mock.disconnect()

        # Assert
        assert ws_mock.is_connected is False
        ws_mock.on_disconnect.assert_called_once()

    def test_config_fake_missing_credentials(self):
        """Test ConfigFake without builder credentials."""
        # Arrange
        fake_config = ConfigFake(
            builder_api_key=None,
            builder_api_secret=None,
            builder_api_passphrase=None,
        )

        # Act
        has_creds = fake_config.has_builder_credentials()

        # Assert
        assert has_creds is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
