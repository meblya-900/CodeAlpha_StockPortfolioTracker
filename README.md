# CodeAlpha Stock Portfolio Tracker

A professional, beginner-friendly, console-based Stock Portfolio Tracker written in Python 3. Build a portfolio by entering stock symbols and quantities, see its total value, and save it automatically to a CSV file.

## Project Overview

This project was built for the **CodeAlpha Python Programming Internship**. The program shows a list of available stocks with hardcoded prices, lets the user add as many stocks as they like, calculates the total investment value, and appends the results to `portfolio.csv` with the current date and time. It uses only Python's standard library, so nothing extra needs to be installed.

## Features

- Displays all available stocks and prices before any input
- Accepts multiple stock symbols (case-insensitive) and a quantity for each
- Type `DONE` to finish entering stocks
- Input validation with friendly error messages for:
  - Invalid stock symbols
  - Empty input
  - Negative numbers
  - Zero
  - Non-numeric quantities (including decimals)
- Adds quantities together if the same stock is entered more than once
- Professional portfolio summary table with the total value
- Automatically appends every portfolio to `portfolio.csv` (never overwrites)
- Records the current date and time using the `datetime` module
- "Create another portfolio? (Y/N)" prompt
- Graceful handling of `Ctrl+C`, EOF and file-saving errors

## Folder Structure

```text
CodeAlpha_StockPortfolioTracker/
├── portfolio.py        # Main application source code
├── README.md           # Project documentation
├── requirements.txt    # Dependency note (none required)
└── portfolio.csv       # Created automatically on the first save
└── screenshots/
    ├── available-stocks.png
    └── portfolio-summary.png
```

## Installation

1. Install **Python 3.8 or newer** from https://www.python.org/downloads/
2. Verify the installation in PowerShell:

```powershell
python --version
```

3. Download or clone this project, then open PowerShell in the project folder:

```powershell
cd CodeAlpha_StockPortfolioTracker
```

No `pip install` is needed because only the standard library is used.

## How to Run

```powershell
python portfolio.py
```

## Example Output

```text
================================================
            STOCK PORTFOLIO TRACKER
================================================

================================================
                Available Stocks
================================================
Stock           Price
------------------------------------------------
AAPL          $180.00
TSLA          $250.00
MSFT          $420.00
NVDA          $950.00
GOOGL         $170.00
AMZN          $190.00
META          $510.00
NFLX          $680.00
================================================

Enter a stock symbol (or DONE to finish): aapl
Enter quantity for AAPL: 5
  Added 5 x AAPL.

Enter a stock symbol (or DONE to finish): xyz
  [!] 'XYZ' is not an available stock.
      Choose from: AAPL, TSLA, MSFT, NVDA, GOOGL, AMZN, META, NFLX

Enter a stock symbol (or DONE to finish): tsla
Enter quantity for TSLA: -3
  [!] Quantity cannot be negative.
Enter quantity for TSLA: 2
  Added 2 x TSLA.

Enter a stock symbol (or DONE to finish): done

================================================
                Portfolio Summary
            Date: 2026-11-03 14:30:00
================================================
Stock          Qty         Price           Value
------------------------------------------------
AAPL             5       $180.00         $900.00
TSLA             2       $250.00         $500.00
------------------------------------------------
Total Portfolio Value:                 $1,400.00
================================================

Portfolio saved to portfolio.csv

Create another portfolio? (Y/N): n

Thank you for using the Stock Portfolio Tracker. Goodbye!
```

### Example `portfolio.csv`

```text
Date,Stock,Quantity,Price,Value
2026-11-03 14:30:00,AAPL,5,180,900
2026-11-03 14:30:00,TSLA,2,250,500
```

## Python Concepts Used

- Functions with docstrings and return values
- Constants and PEP 8 naming conventions
- Dictionaries for stock prices and the portfolio
- `while` loops and conditional logic
- Input validation with `try` / `except`
- String methods and f-string formatting (alignment and padding)
- The `csv` module (appending rows and writing headers)
- The `datetime` module for timestamps
- The `pathlib` module for file paths
- File handling with the `with` statement
- Handling `KeyboardInterrupt` and `EOFError`
- Generator expressions with `sum()`
- The `if __name__ == "__main__"` entry point

## Future Improvements

- Fetch live stock prices from an API
- Allow selling or removing stocks from a portfolio
- View and analyse saved portfolios from the CSV file
- Add profit and loss tracking
- Support portfolio charts
- Load stock prices from an external file
- Add unit tests with `unittest`

## Author

**Meward Bwalya**
CodeAlpha Python Programming Intern
Email: mewardb@gmail.com