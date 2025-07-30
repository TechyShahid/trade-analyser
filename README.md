# NSE Data Fetcher

This Python project fetches historical stock data and deal data from the National Stock Exchange (NSE) of India, suitable for swing trading and investment analysis.

## Setup

1. Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Fetching Data Programmatically

The main module is `nse_data_fetcher/fetcher.py`. You can fetch historical stock data, bulk deals, and block deals by calling the respective functions:

- `fetch_stock_data(symbol, start_date, end_date)`
- `fetch_bulk_deal_data(trade_date)`
- `fetch_block_deal_data(trade_date)`

Example:

```python
from datetime import date
from nse_data_fetcher.fetcher import fetch_stock_data

symbol = "RELIANCE"
start_date = date(2023, 1, 1)
end_date = date(2023, 12, 31)

data = fetch_stock_data(symbol, start_date, end_date)
print(data)
```

## REST API

A FastAPI-based REST API is provided to expose the data fetching functionality via HTTP endpoints.

### Running the API Server

Run the API server with:

```bash
uvicorn nse_data_fetcher.api:app --reload
```

### API Endpoints

- **GET /stock-data**

  Fetch historical stock data.

  Query parameters:
  - `symbol` (string): Stock symbol, e.g. RELIANCE
  - `start_date` (string): Start date in YYYY-MM-DD format
  - `end_date` (string): End date in YYYY-MM-DD format

  Example:

  ```
  http://127.0.0.1:8000/stock-data?symbol=RELIANCE&start_date=2023-01-01&end_date=2023-01-31
  ```

- **GET /bulk-deals**

  Fetch bulk deal data for a specific trade date.

  Query parameters:
  - `trade_date` (string): Trade date in YYYY-MM-DD format

  Example:

  ```
  http://127.0.0.1:8000/bulk-deals?trade_date=2023-07-22
  ```

- **GET /block-deals**

  Fetch block deal data for a specific trade date.

  Query parameters:
  - `trade_date` (string): Trade date in YYYY-MM-DD format

  Example:

  ```
  http://127.0.0.1:8000/block-deals?trade_date=2023-07-22
  ```

### Notes

- The API handles JSON serialization of special float values like NaN and infinite by converting them appropriately using pandas' built-in JSON serialization.
- Proper error handling is implemented for invalid inputs and missing data.
- The API returns HTTP 404 if no data is found for the requested parameters.

## Testing

- Core data fetching functions have unit tests covering valid and invalid inputs.
- API endpoints have been manually tested for JSON serialization and error handling.
- Further thorough testing can be performed as needed.

## Dependencies

- `nsepy` or `nselib` for NSE data fetching
- `fastapi` and `uvicorn` for the REST API
- `pandas` for data manipulation

Install all dependencies via:

```bash
pip install -r requirements.txt
```

## License

MIT License
