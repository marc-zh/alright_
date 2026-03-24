"""
ApiClientStub - Test Stub for API Client

A stub implementation of API client for testing purposes.
Provides canned responses to API calls without making real network requests.
"""

from typing import Optional, Dict, Any, List
from unittest.mock import Mock


class ApiClientStub:
    """
    Stub API client for testing.

    Provides pre-programmed responses to API calls.
    Used in tests to avoid making real network requests.
    """

    def __init__(self):
        """Initialize API client stub."""
        self._responses: Dict[str, Any] = {}
        self._calls: List[Dict[str, Any]] = []

        # Set up default responses
        self._setup_default_responses()

    def _setup_default_responses(self) -> None:
        """Set up default canned responses."""
        self._responses = {
            "get_order_book": {
                "asset_id": "test_token_id",
                "bids": [
                    {"price": 0.65, "size": 100},
                    {"price": 0.64, "size": 200},
                ],
                "asks": [
                    {"price": 0.66, "size": 150},
                    {"price": 0.67, "size": 100},
                ],
            },
            "get_market_price": 0.65,
            "get_mid_price": 0.655,
            "place_order": {
                "success": True,
                "orderId": "test_order_123",
                "message": "Order placed successfully",
            },
            "cancel_order": {
                "success": True,
                "orderId": "test_order_123",
                "message": "Order cancelled",
            },
            "get_open_orders": [
                {
                    "orderId": "test_order_123",
                    "side": "BUY",
                    "price": 0.65,
                    "originalSize": 10,
                    "matches": 5,
                }
            ],
        }

    def set_response(self, method: str, response: Any) -> None:
        """
        Set a canned response for a method.

        Args:
            method: Method name
            response: Response to return
        """
        self._responses[method] = response

    def get_call_history(self) -> List[Dict[str, Any]]:
        """
        Get history of API calls.

        Returns:
            List of call dictionaries
        """
        return self._calls.copy()

    def clear_call_history(self) -> None:
        """Clear call history."""
        self._calls.clear()

    def get_order_book(
        self,
        asset_id: str,
        price_limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get order book (stub implementation).

        Args:
            asset_id: Token ID
            price_limit: Optional price limit

        Returns:
            Order book data
        """
        self._calls.append({
            "method": "get_order_book",
            "asset_id": asset_id,
            "price_limit": price_limit,
        })

        response = self._responses.get("get_order_book", {}).copy()
        response["asset_id"] = asset_id
        return response

    def get_market_price(self, token_id: str) -> float:
        """
        Get market price (stub implementation).

        Args:
            token_id: Token ID

        Returns:
            Market price
        """
        self._calls.append({
            "method": "get_market_price",
            "token_id": token_id,
        })

        return self._responses.get("get_market_price", 0.5)

    def get_mid_price(self, token_id: str) -> float:
        """
        Get mid price (stub implementation).

        Args:
            token_id: Token ID

        Returns:
            Mid price
        """
        self._calls.append({
            "method": "get_mid_price",
            "token_id": token_id,
        })

        return self._responses.get("get_mid_price", 0.5)

    def place_order(
        self,
        token_id: str,
        price: float,
        size: float,
        side: str,
    ) -> Dict[str, Any]:
        """
        Place order (stub implementation).

        Args:
            token_id: Token ID
            price: Order price
            size: Order size
            side: Order side (BUY/SELL)

        Returns:
            Order result
        """
        self._calls.append({
            "method": "place_order",
            "token_id": token_id,
            "price": price,
            "size": size,
            "side": side,
        })

        response = self._responses.get("place_order", {}).copy()
        return response

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """
        Cancel order (stub implementation).

        Args:
            order_id: Order ID to cancel

        Returns:
            Cancellation result
        """
        self._calls.append({
            "method": "cancel_order",
            "order_id": order_id,
        })

        response = self._responses.get("cancel_order", {}).copy()
        return response

    def get_open_orders(self, market: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get open orders (stub implementation).

        Args:
            market: Optional market filter

        Returns:
            List of open orders
        """
        self._calls.append({
            "method": "get_open_orders",
            "market": market,
        })

        return self._responses.get("get_open_orders", [])

    def was_called(self, method: str) -> bool:
        """
        Check if a method was called.

        Args:
            method: Method name

        Returns:
            True if method was called
        """
        return any(call["method"] == method for call in self._calls)

    def get_call_count(self, method: str) -> int:
        """
        Get number of times a method was called.

        Args:
            method: Method name

        Returns:
            Number of calls
        """
        return sum(1 for call in self._calls if call["method"] == method)

    def get_last_call_args(self, method: str) -> Optional[Dict[str, Any]]:
        """
        Get arguments from last call to a method.

        Args:
            method: Method name

        Returns:
            Dictionary of arguments or None
        """
        for call in reversed(self._calls):
            if call["method"] == method:
                return {k: v for k, v in call.items() if k != "method"}
        return None
