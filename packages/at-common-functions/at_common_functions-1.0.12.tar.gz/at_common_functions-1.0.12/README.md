# AT Common Functions

A Python package providing common asynchronous task definitions and utilities for workflow operations.

## Installation
```bash
pip install at_common_functions
```

## Usage
### Database Storage Initialization
```python
from at_common_functions import init_storage

# Initialize storage connection
storage = init_storage(
    host="localhost",
    port=3306,
    user="user",
    password="password",
    database="dbname"
)
```

### Stock Data Operations
```python
from at_common_functions.stock import (
    stock_get_overview,
    stock_get_quotation,
    stock_get_candlesticks,
    stock_get_indicators,
    stock_get_financials
)

async def main():
    # Get stock overview
    overview = await stock_get_overview("AAPL")
    print(overview) # Contains symbol, name, sector, etc.

    # Get current quotation
    quotation = await stock_get_quotation("AAPL")
    print(quotation) # Contains price, volume, timestamp
    
    # Get daily candlesticks
    candlesticks = await stock_get_candlesticks("AAPL", "daily", limit=5)
    print(candlesticks) # List of candlesticks with OHLCV data
    
    # Get technical indicators
    indicators = await stock_get_indicators("AAPL", "daily", limit=5)
    print(indicators) # List of indicators (SMA, RSI, etc.)
    
    # Get financial statements
    financials = await stock_get_financials(
        symbol="AAPL",
        period="annual", # or "quarterly"
        statement="income", # or "balance_sheet", "cash_flow"
        limit=3
    )
    print(financials)
```

## Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment
4. Install development dependencies: `pip install -e ".[dev]"`
5. Run tests: `pytest`

## Dependencies

- Python >= 3.11
- at_common_workflow >= 1.1.15
- SQLAlchemy >= 2.0.36
- at-common-models >= 0.1.3
- aiomysql >= 0.2.0
- greenlet >= 3.0.3

### Development Dependencies
- pytest >= 8.3.4
- pytest-asyncio >= 0.24.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.