"""
CLI Module - Command Line Interface for Polymarket Trading Bot

Provides a simple command-line interface for interacting with the bot.
This serves as the "frontend" component for the trading bot.

Example:
    from src.cli import CLI

    cli = CLI()
    cli.display_market_info({"slug": "eth-market", "question": "Will ETH go up?"})
"""

import sys
from typing import Optional, Dict, Any, List
from .utils import format_price, format_usdc, truncate_address


class CLI:
    """
    Command Line Interface for Polymarket Trading Bot.

    Provides methods to display market information, order details,
    and trading results in a user-friendly format.
    """

    def __init__(self, output_stream=None):
        """
        Initialize CLI.

        Args:
            output_stream: Stream to write output to (default: sys.stdout)
        """
        self.output_stream = output_stream or sys.stdout

    def write(self, message: str) -> None:
        """
        Write a message to the output stream.

        Args:
            message: Message to write
        """
        self.output_stream.write(message + "\n")

    def display_header(self, title: str) -> None:
        """
        Display a formatted header.

        Args:
            title: Header title
        """
        self.write("\n" + "=" * 60)
        self.write(f"  {title}")
        self.write("=" * 60 + "\n")

    def display_market_info(self, market: Dict[str, Any]) -> None:
        """
        Display market information in a formatted way.

        Args:
            market: Market data dictionary
        """
        self.display_header("Market Information")

        slug = market.get("slug", "N/A")
        question = market.get("question", "N/A")
        end_date = market.get("end_date", "N/A")
        token_ids = market.get("token_ids", {})
        prices = market.get("prices", {})

        self.write(f"Slug: {slug}")
        self.write(f"Question: {question}")
        self.write(f"End Date: {end_date}")

        if token_ids:
            self.write("\nToken IDs:")
            for side, token_id in token_ids.items():
                truncated = truncate_address(token_id, chars=8)
                self.write(f"  {side.upper()}: {truncated}")

        if prices:
            self.write("\nCurrent Prices:")
            for side, price in prices.items():
                formatted = format_price(price)
                self.write(f"  {side.upper()}: {formatted}")

        self.write("")

    def display_order_result(self, success: bool, order_id: Optional[str], message: str) -> None:
        """
        Display order placement result.

        Args:
            success: Whether the order was successful
            order_id: Order ID (if successful)
            message: Result message
        """
        self.display_header("Order Result")

        if success:
            self.write(f"✓ Order placed successfully!")
            self.write(f"Order ID: {order_id}")
        else:
            self.write(f"✗ Order failed: {message}")

        self.write("")

    def display_balance(self, balance: float) -> None:
        """
        Display account balance.

        Args:
            balance: Balance amount in USDC
        """
        self.display_header("Account Balance")
        formatted = format_usdc(balance)
        self.write(f"Available Balance: {formatted}\n")

    def display_orders(self, orders: List[Dict[str, Any]]) -> None:
        """
        Display list of open orders.

        Args:
            orders: List of order dictionaries
        """
        self.display_header(f"Open Orders ({len(orders)})")

        if not orders:
            self.write("No open orders.\n")
            return

        for i, order in enumerate(orders, 1):
            order_id = order.get("orderId", "N/A")[:12]
            side = order.get("side", "N/A")
            price = order.get("price", 0)
            size = order.get("originalSize", 0)
            filled = order.get("matches", 0)

            self.write(f"\n{i}. Order {order_id}...")
            self.write(f"   Side: {side}")
            self.write(f"   Price: {format_price(price)}")
            self.write(f"   Size: {size} shares")
            self.write(f"   Filled: {filled} shares")

        self.write("")

    def display_error(self, error: str) -> None:
        """
        Display an error message.

        Args:
            error: Error message
        """
        self.write(f"\n✗ Error: {error}\n")

    def display_success(self, message: str) -> None:
        """
        Display a success message.

        Args:
            message: Success message
        """
        self.write(f"\n✓ {message}\n")


def display_market_summary(market: Dict[str, Any]) -> str:
    """
    Get a formatted market summary string.

    Args:
        market: Market data dictionary

    Returns:
        Formatted market summary string
    """
    question = market.get("question", "N/A")
    prices = market.get("prices", {})
    up_price = prices.get("up", 0)
    down_price = prices.get("down", 0)

    summary = f"{question}\n"
    summary += f"  UP: {format_price(up_price)} | DOWN: {format_price(down_price)}"

    return summary


def parse_arguments(args: List[str]) -> Dict[str, Any]:
    """
    Parse command line arguments.

    Args:
        args: List of command line arguments

    Returns:
        Dictionary of parsed arguments
    """
    parsed = {
        "command": None,
        "coin": None,
        "action": None,
        "size": 10.0,
        "price": None,
    }

    if len(args) < 2:
        return parsed

    parsed["command"] = args[1]

    for i, arg in enumerate(args[2:], 2):
        if arg.startswith("--coin="):
            parsed["coin"] = arg.split("=")[1].upper()
        elif arg.startswith("--action="):
            parsed["action"] = arg.split("=")[1].upper()
        elif arg.startswith("--size="):
            parsed["size"] = float(arg.split("=")[1])
        elif arg.startswith("--price="):
            parsed["price"] = float(arg.split("=")[1])

    return parsed


def main() -> int:
    """
    Main CLI entry point.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    args = parse_arguments(sys.argv)
    cli = CLI()

    if not args["command"]:
        cli.display_header("Polymarket Trading Bot CLI")
        cli.write("Usage: python -m src.cli <command> [options]")
        cli.write("\nCommands:")
        cli.write("  market   --coin=BTC|ETH|SOL|XRP  Display current market info")
        cli.write("  balance                              Display account balance")
        cli.write("  orders                               Display open orders")
        cli.write("\nOptions:")
        cli.write("  --coin=BTC|ETH|SOL|XRP  Coin symbol")
        cli.write("  --action=BUY|SELL       Order side")
        cli.write("  --size=<amount>         Order size in USDC")
        cli.write("  --price=<price>         Order price (0-1)")
        return 0

    if args["command"] == "market":
        if not args["coin"]:
            cli.display_error("Please specify a coin with --coin=BTC|ETH|SOL|XRP")
            return 1

        cli.display_success(f"Fetching market info for {args['coin']}...")
        # In real implementation, would fetch actual market data
        # For now, just display a placeholder
        cli.write("Market data fetching not implemented in this example")

    elif args["command"] == "balance":
        cli.display_success("Fetching account balance...")
        cli.write("Balance fetching not implemented in this example")

    elif args["command"] == "orders":
        cli.display_success("Fetching open orders...")
        cli.write("Order fetching not implemented in this example")

    else:
        cli.display_error(f"Unknown command: {args['command']}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
