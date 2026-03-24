"""
Unit Tests for CLI Module

Tests the command line interface for the Polymarket Trading Bot.

Run with:
    pytest tests/test_cli.py -v
"""

import io
import sys
import pytest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cli import CLI, display_market_summary, parse_arguments


class TestCLI:
    """Tests for CLI class."""

    def test_cli_initialization(self):
        """Test CLI initialization."""
        cli = CLI()
        assert cli.output_stream == sys.stdout

    def test_cli_with_custom_output(self):
        """Test CLI with custom output stream."""
        output = io.StringIO()
        cli = CLI(output_stream=output)
        assert cli.output_stream == output

    def test_write_message(self):
        """Test writing a message."""
        output = io.StringIO()
        cli = CLI(output_stream=output)
        cli.write("Test message")
        assert output.getvalue() == "Test message\n"

    def test_display_header(self):
        """Test displaying a header."""
        output = io.StringIO()
        cli = CLI(output_stream=output)
        cli.display_header("Test Header")

        result = output.getvalue()
        assert "Test Header" in result
        assert "===" in result

    def test_display_market_info_basic(self):
        """Test displaying basic market info."""
        output = io.StringIO()
        cli = CLI(output_stream=output)

        market = {
            "slug": "eth-market",
            "question": "Will ETH go up?",
            "end_date": "2024-01-01T00:00:00Z",
        }

        cli.display_market_info(market)
        result = output.getvalue()

        assert "eth-market" in result
        assert "Will ETH go up?" in result
        assert "2024-01-01T00:00:00Z" in result

    def test_display_market_info_with_prices(self):
        """Test displaying market info with prices."""
        output = io.StringIO()
        cli = CLI(output_stream=output)

        market = {
            "slug": "btc-market",
            "question": "Will BTC go up?",
            "token_ids": {"up": "0x123...", "down": "0x456..."},
            "prices": {"up": 0.65, "down": 0.35},
        }

        cli.display_market_info(market)
        result = output.getvalue()

        assert "UP:" in result
        assert "DOWN:" in result
        assert "65%" in result
        assert "35%" in result

    def test_display_order_result_success(self):
        """Test displaying successful order result."""
        output = io.StringIO()
        cli = CLI(output_stream=output)

        cli.display_order_result(True, "order_123", "Order placed")
        result = output.getvalue()

        assert "✓ Order placed successfully!" in result
        assert "order_123" in result

    def test_display_order_result_failure(self):
        """Test displaying failed order result."""
        output = io.StringIO()
        cli = CLI(output_stream=output)

        cli.display_order_result(False, None, "Insufficient balance")
        result = output.getvalue()

        assert "✗ Order failed" in result
        assert "Insufficient balance" in result

    def test_display_balance(self):
        """Test displaying account balance."""
        output = io.StringIO()
        cli = CLI(output_stream=output)

        cli.display_balance(100.50)
        result = output.getvalue()

        assert "Account Balance" in result
        assert "$100.50" in result

    def test_display_orders_empty(self):
        """Test displaying empty orders list."""
        output = io.StringIO()
        cli = CLI(output_stream=output)

        cli.display_orders([])
        result = output.getvalue()

        assert "No open orders" in result

    def test_display_orders_with_data(self):
        """Test displaying orders with data."""
        output = io.StringIO()
        cli = CLI(output_stream=output)

        orders = [
            {
                "orderId": "0xabcdef123456",
                "side": "BUY",
                "price": 0.65,
                "originalSize": 10,
                "matches": 5,
            }
        ]

        cli.display_orders(orders)
        result = output.getvalue()

        assert "BUY" in result
        assert "65%" in result
        assert "10 shares" in result
        assert "5 shares" in result

    def test_display_error(self):
        """Test displaying error message."""
        output = io.StringIO()
        cli = CLI(output_stream=output)

        cli.display_error("Test error")
        result = output.getvalue()

        assert "✗ Error: Test error" in result

    def test_display_success(self):
        """Test displaying success message."""
        output = io.StringIO()
        cli = CLI(output_stream=output)

        cli.display_success("Test success")
        result = output.getvalue()

        assert "✓ Test success" in result


class TestDisplayMarketSummary:
    """Tests for display_market_summary function."""

    def test_market_summary_basic(self):
        """Test basic market summary."""
        market = {
            "question": "Will BTC go up?",
            "prices": {"up": 0.60, "down": 0.40},
        }

        summary = display_market_summary(market)

        assert "Will BTC go up?" in summary
        assert "60%" in summary
        assert "40%" in summary

    def test_market_summary_no_prices(self):
        """Test market summary without prices."""
        market = {"question": "Test question"}

        summary = display_market_summary(market)

        assert "Test question" in summary
        assert "0%" in summary  # Default prices


class TestParseArguments:
    """Tests for parse_arguments function."""

    def test_parse_no_arguments(self):
        """Test parsing with no arguments."""
        args = parse_arguments(["cli.py"])
        assert args["command"] is None
        assert args["coin"] is None

    def test_parse_command_only(self):
        """Test parsing with command only."""
        args = parse_arguments(["cli.py", "market"])
        assert args["command"] == "market"
        assert args["coin"] is None

    def test_parse_with_coin(self):
        """Test parsing with coin argument."""
        args = parse_arguments(["cli.py", "market", "--coin=BTC"])
        assert args["command"] == "market"
        assert args["coin"] == "BTC"

    def test_parse_with_lowercase_coin(self):
        """Test parsing with lowercase coin (should uppercase)."""
        args = parse_arguments(["cli.py", "market", "--coin=eth"])
        assert args["coin"] == "ETH"

    def test_parse_with_size(self):
        """Test parsing with size argument."""
        args = parse_arguments(["cli.py", "market", "--size=50.0"])
        assert args["size"] == 50.0

    def test_parse_with_price(self):
        """Test parsing with price argument."""
        args = parse_arguments(["cli.py", "market", "--price=0.75"])
        assert args["price"] == 0.75

    def test_parse_with_multiple_options(self):
        """Test parsing with multiple options."""
        args = parse_arguments([
            "cli.py",
            "market",
            "--coin=ETH",
            "--action=BUY",
            "--size=25.0",
            "--price=0.60"
        ])

        assert args["command"] == "market"
        assert args["coin"] == "ETH"
        assert args["action"] == "BUY"
        assert args["size"] == 25.0
        assert args["price"] == 0.60


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
