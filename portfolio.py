"""
Stock Portfolio Tracker
=======================
A console-based application that lets the user build a stock portfolio
by entering stock symbols and quantities. The portfolio value is
calculated from a hardcoded dictionary of prices, displayed as a summary
table, and appended to a CSV file.

Created for the CodeAlpha Python Programming Internship.
Uses only Python's standard library (no external dependencies).
"""

import csv
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
# Hardcoded stock prices (symbol -> price in US dollars).
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "MSFT": 420,
    "NVDA": 950,
    "GOOGL": 170,
    "AMZN": 190,
    "META": 510,
    "NFLX": 680,
}

# The CSV file is stored next to this script, wherever it is run from.
CSV_FILE_PATH = Path(__file__).resolve().parent / "portfolio.csv"
CSV_HEADERS = ["Date", "Stock", "Quantity", "Price", "Value"]

FINISH_KEYWORD = "DONE"
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SEPARATOR_WIDTH = 48
SEPARATOR_LINE = "=" * SEPARATOR_WIDTH
THIN_LINE = "-" * SEPARATOR_WIDTH

# Column widths used for the tables (they add up to SEPARATOR_WIDTH).
SYMBOL_COLUMN_WIDTH = 10
QUANTITY_COLUMN_WIDTH = 8
PRICE_COLUMN_WIDTH = 14
VALUE_COLUMN_WIDTH = 16


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------
def format_currency(amount):
    """
    Format a number as US dollars with thousands separators.

    Args:
        amount (int or float): The amount of money.

    Returns:
        str: The formatted amount, for example "$1,400.00".
    """
    return f"${amount:,.2f}"


# ---------------------------------------------------------------------------
# Display functions
# ---------------------------------------------------------------------------
def display_available_stocks(stock_prices):
    """
    Show every available stock and its price.

    Args:
        stock_prices (dict): Maps stock symbols to prices.
    """
    print(f"\n{SEPARATOR_LINE}")
    print("Available Stocks".center(SEPARATOR_WIDTH))
    print(SEPARATOR_LINE)
    print(f"{'Stock':<{SYMBOL_COLUMN_WIDTH}}{'Price':>12}")
    print(THIN_LINE)

    for symbol, price in stock_prices.items():
        print(f"{symbol:<{SYMBOL_COLUMN_WIDTH}}{format_currency(price):>12}")

    print(SEPARATOR_LINE)


def display_summary(portfolio, stock_prices, timestamp):
    """
    Print a professional summary table of the portfolio.

    Args:
        portfolio (dict): Maps stock symbols to quantities owned.
        stock_prices (dict): Maps stock symbols to prices.
        timestamp (str): The date and time of the portfolio.
    """
    print(f"\n{SEPARATOR_LINE}")
    print("Portfolio Summary".center(SEPARATOR_WIDTH))
    print(f"Date: {timestamp}".center(SEPARATOR_WIDTH))
    print(SEPARATOR_LINE)
    print(
        f"{'Stock':<{SYMBOL_COLUMN_WIDTH}}"
        f"{'Qty':>{QUANTITY_COLUMN_WIDTH}}"
        f"{'Price':>{PRICE_COLUMN_WIDTH}}"
        f"{'Value':>{VALUE_COLUMN_WIDTH}}"
    )
    print(THIN_LINE)

    for symbol, quantity in portfolio.items():
        price = stock_prices[symbol]
        value = price * quantity
        print(
            f"{symbol:<{SYMBOL_COLUMN_WIDTH}}"
            f"{quantity:>{QUANTITY_COLUMN_WIDTH}}"
            f"{format_currency(price):>{PRICE_COLUMN_WIDTH}}"
            f"{format_currency(value):>{VALUE_COLUMN_WIDTH}}"
        )

    print(THIN_LINE)
    total_value = calculate_total(portfolio, stock_prices)
    label_width = SEPARATOR_WIDTH - VALUE_COLUMN_WIDTH
    print(
        f"{'Total Portfolio Value:':<{label_width}}"
        f"{format_currency(total_value):>{VALUE_COLUMN_WIDTH}}"
    )
    print(SEPARATOR_LINE)


# ---------------------------------------------------------------------------
# Input functions
# ---------------------------------------------------------------------------
def get_stock_symbol(stock_prices):
    """
    Keep asking until the user enters a valid stock symbol or DONE.

    Args:
        stock_prices (dict): Maps stock symbols to prices.

    Returns:
        str or None: The valid symbol in uppercase, or None if the user
        typed DONE to finish.
    """
    while True:
        user_input = input(
            f"\nEnter a stock symbol (or {FINISH_KEYWORD} to finish): "
        ).strip().upper()

        if not user_input:
            print("  [!] Input cannot be empty. Please enter a stock symbol.")
        elif user_input == FINISH_KEYWORD:
            return None
        elif user_input not in stock_prices:
            print(f"  [!] '{user_input}' is not an available stock.")
            print(f"      Choose from: {', '.join(stock_prices)}")
        else:
            return user_input


def get_quantity(symbol):
    """
    Keep asking until the user enters a valid whole-number quantity.

    Rejects empty input, non-numeric text, decimals, zero and
    negative numbers.

    Args:
        symbol (str): The stock symbol the quantity is for.

    Returns:
        int: A positive whole number.
    """
    while True:
        user_input = input(f"Enter quantity for {symbol}: ").strip()

        if not user_input:
            print("  [!] Input cannot be empty. Please enter a quantity.")
            continue

        try:
            quantity = int(user_input)
        except ValueError:
            print("  [!] Please enter a whole number (for example, 5).")
            continue

        if quantity < 0:
            print("  [!] Quantity cannot be negative.")
        elif quantity == 0:
            print("  [!] Quantity must be greater than zero.")
        else:
            return quantity


def ask_create_another():
    """
    Ask the user whether they want to create another portfolio.

    Returns:
        bool: True if the user answers Y, False if the answer is N.
    """
    while True:
        answer = input("\nCreate another portfolio? (Y/N): ").strip().upper()

        if answer == "Y":
            return True
        if answer == "N":
            return False

        print("  [!] Please enter Y for Yes or N for No.")


# ---------------------------------------------------------------------------
# Portfolio logic
# ---------------------------------------------------------------------------
def add_stock(portfolio, symbol, quantity):
    """
    Add a stock to the portfolio.

    If the stock is already in the portfolio, the quantity is added to
    the existing amount instead of replacing it.

    Args:
        portfolio (dict): Maps stock symbols to quantities (modified).
        symbol (str): The stock symbol to add.
        quantity (int): The number of shares to add.
    """
    portfolio[symbol] = portfolio.get(symbol, 0) + quantity


def calculate_total(portfolio, stock_prices):
    """
    Calculate the total value of the portfolio.

    Args:
        portfolio (dict): Maps stock symbols to quantities owned.
        stock_prices (dict): Maps stock symbols to prices.

    Returns:
        int or float: The sum of price x quantity for every stock.
    """
    return sum(
        stock_prices[symbol] * quantity
        for symbol, quantity in portfolio.items()
    )


# ---------------------------------------------------------------------------
# File handling
# ---------------------------------------------------------------------------
def save_to_csv(portfolio, stock_prices, timestamp, file_path=CSV_FILE_PATH):
    """
    Append the portfolio to a CSV file.

    The header row is written only when the file is new or empty, so
    existing entries are never overwritten.

    Args:
        portfolio (dict): Maps stock symbols to quantities owned.
        stock_prices (dict): Maps stock symbols to prices.
        timestamp (str): The date and time of the portfolio.
        file_path (Path): The CSV file to append to.

    Returns:
        bool: True if the file was saved, False if an error occurred.
    """
    needs_header = not file_path.exists() or file_path.stat().st_size == 0

    try:
        with open(file_path, "a", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)

            if needs_header:
                writer.writerow(CSV_HEADERS)

            for symbol, quantity in portfolio.items():
                price = stock_prices[symbol]
                writer.writerow([timestamp, symbol, quantity, price,
                                 price * quantity])
    except OSError as error:
        print(f"\n  [!] Could not save the portfolio: {error}")
        print("      Close the file if it is open in another program.")
        return False

    print(f"\nPortfolio saved to {file_path.name}")
    return True


# ---------------------------------------------------------------------------
# Main workflow
# ---------------------------------------------------------------------------
def create_portfolio(stock_prices):
    """
    Build one portfolio, display its summary and save it to CSV.

    Args:
        stock_prices (dict): Maps stock symbols to prices.
    """
    portfolio = {}
    display_available_stocks(stock_prices)

    while True:
        symbol = get_stock_symbol(stock_prices)
        if symbol is None:
            break

        quantity = get_quantity(symbol)
        add_stock(portfolio, symbol, quantity)
        print(f"  Added {quantity} x {symbol}.")

    if not portfolio:
        print("\nNo stocks were entered, so there is nothing to save.")
        return

    timestamp = datetime.now().strftime(DATE_TIME_FORMAT)
    display_summary(portfolio, stock_prices, timestamp)
    save_to_csv(portfolio, stock_prices, timestamp)


def main():
    """
    Run the Stock Portfolio Tracker and handle repeat portfolios.
    """
    print(SEPARATOR_LINE)
    print("STOCK PORTFOLIO TRACKER".center(SEPARATOR_WIDTH))
    print(SEPARATOR_LINE)

    try:
        keep_going = True
        while keep_going:
            create_portfolio(STOCK_PRICES)
            keep_going = ask_create_another()
    except (KeyboardInterrupt, EOFError):
        # Handles Ctrl+C and EOF (Ctrl+Z then Enter on Windows)
        # without showing a traceback.
        print("\n\nProgram interrupted.")

    print("\nThank you for using the Stock Portfolio Tracker. Goodbye!")


if __name__ == "__main__":
    main()