"""
WebSocketMock - Test Mock for WebSocket Client

A mock implementation of WebSocket client for testing purposes.
Simulates WebSocket behavior without real network connections.
"""

import asyncio
from typing import Optional, Dict, Any, List, Callable
from unittest.mock import Mock, AsyncMock


class WebSocketMock:
    """
    Mock WebSocket client for testing.

    Simulates WebSocket connections and messages without real network.
    """

    def __init__(self):
        """Initialize WebSocket mock."""
        self._connected = False
        self._subscribed_assets: set = set()
        self._message_handlers: List[Callable] = []
        self._sent_messages: List[Dict[str, Any]] = []
        self._received_messages: List[Dict[str, Any]] = []

        # Mock callbacks
        self.on_book = Mock()
        self.on_price_change = Mock()
        self.on_trade = Mock()
        self.on_error = Mock()
        self.on_connect = Mock()
        self.on_disconnect = Mock()

    async def connect(self) -> bool:
        """
        Simulate WebSocket connection.

        Returns:
            True (always succeeds in mock)
        """
        self._connected = True
        if self.on_connect:
            self.on_connect()
        return True

    async def disconnect(self) -> None:
        """Simulate WebSocket disconnection."""
        self._connected = False
        if self.on_disconnect:
            self.on_disconnect()

    @property
    def is_connected(self) -> bool:
        """
        Check if WebSocket is connected.

        Returns:
            Connection status
        """
        return self._connected

    async def subscribe(self, asset_ids: List[str], replace: bool = False) -> bool:
        """
        Simulate subscribing to assets.

        Args:
            asset_ids: List of token IDs to subscribe to
            replace: Whether to replace existing subscriptions

        Returns:
            True (always succeeds in mock)
        """
        if replace:
            self._subscribed_assets.clear()

        self._subscribed_assets.update(asset_ids)
        return True

    async def unsubscribe(self, asset_ids: List[str]) -> bool:
        """
        Simulate unsubscribing from assets.

        Args:
            asset_ids: List of token IDs to unsubscribe from

        Returns:
            True (always succeeds in mock)
        """
        self._subscribed_assets.difference_update(asset_ids)
        return True

    def get_subscribed_assets(self) -> set:
        """
        Get subscribed assets.

        Returns:
            Set of subscribed asset IDs
        """
        return self._subscribed_assets.copy()

    async def send(self, message: Dict[str, Any]) -> None:
        """
        Simulate sending a message.

        Args:
            message: Message to send
        """
        self._sent_messages.append(message)

    def get_sent_messages(self) -> List[Dict[str, Any]]:
        """
        Get all sent messages.

        Returns:
            List of sent messages
        """
        return self._sent_messages.copy()

    def clear_sent_messages(self) -> None:
        """Clear sent messages history."""
        self._sent_messages.clear()

    async def simulate_message(self, message: Dict[str, Any]) -> None:
        """
        Simulate receiving a message from the server.

        Args:
            message: Message to receive
        """
        self._received_messages.append(message)

        # Trigger appropriate callback based on message type
        event_type = message.get("event_type", "")

        if event_type == "book" and self.on_book:
            if asyncio.iscoroutinefunction(self.on_book):
                await self.on_book(message)
            else:
                self.on_book(message)

        elif event_type == "price_change" and self.on_price_change:
            if asyncio.iscoroutinefunction(self.on_price_change):
                await self.on_price_change(message)
            else:
                self.on_price_change(message)

        elif event_type == "last_trade_price" and self.on_trade:
            if asyncio.iscoroutinefunction(self.on_trade):
                await self.on_trade(message)
            else:
                self.on_trade(message)

    def get_received_messages(self) -> List[Dict[str, Any]]:
        """
        Get all received messages.

        Returns:
            List of received messages
        """
        return self._received_messages.copy()

    def clear_received_messages(self) -> None:
        """Clear received messages history."""
        self._received_messages.clear()

    def was_subscribed(self, asset_id: str) -> bool:
        """
        Check if an asset was subscribed to.

        Args:
            asset_id: Asset ID to check

        Returns:
            True if asset is subscribed
        """
        return asset_id in self._subscribed_assets

    def get_subscription_count(self) -> int:
        """
        Get number of subscribed assets.

        Returns:
            Number of subscriptions
        """
        return len(self._subscribed_assets)

    def reset(self) -> None:
        """Reset mock to initial state."""
        self._connected = False
        self._subscribed_assets.clear()
        self._sent_messages.clear()
        self._received_messages.clear()
        self.on_book.reset_mock()
        self.on_price_change.reset_mock()
        self.on_trade.reset_mock()
        self.on_error.reset_mock()
        self.on_connect.reset_mock()
        self.on_disconnect.reset_mock()

    def assert_connected(self) -> None:
        """Assert that WebSocket is connected."""
        assert self._connected, "WebSocket is not connected"

    def assert_not_connected(self) -> None:
        """Assert that WebSocket is not connected."""
        assert not self._connected, "WebSocket is connected"

    def assert_subscribed(self, asset_id: str) -> None:
        """
        Assert that an asset is subscribed.

        Args:
            asset_id: Asset ID to check
        """
        assert asset_id in self._subscribed_assets, f"Asset {asset_id} is not subscribed"

    def assert_not_subscribed(self, asset_id: str) -> None:
        """
        Assert that an asset is not subscribed.

        Args:
            asset_id: Asset ID to check
        """
        assert asset_id not in self._subscribed_assets, f"Asset {asset_id} is subscribed"

    def assert_message_sent(self, message_type: Optional[str] = None) -> None:
        """
        Assert that a message was sent.

        Args:
            message_type: Optional message type to check
        """
        assert len(self._sent_messages) > 0, "No messages were sent"

        if message_type:
            found = any(msg.get("type") == message_type for msg in self._sent_messages)
            assert found, f"No message of type {message_type} was sent"

    def assert_callback_called(self, callback_name: str) -> None:
        """
        Assert that a callback was called.

        Args:
            callback_name: Name of the callback (e.g., "on_book")
        """
        callback = getattr(self, callback_name, None)
        assert callback is not None, f"Callback {callback_name} does not exist"
        assert callback.called, f"Callback {callback_name} was not called"
