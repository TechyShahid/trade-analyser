# NSE Data Fetcher

This Python project fetches historical stock data from the National Stock Exchange (NSE) of India, suitable for swing trading and investment analysis.

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

The main module is `nse_data_fetcher/fetcher.py`. You can fetch historical stock data by calling the `fetch_stock_data` function.

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

### REST API

You can also run the REST API server to access the data via HTTP endpoints.

1. Install dependencies (if not done):

```bash
pip install -r requirements.txt
```

2. Run the API server:

```bash
uvicorn nse_data_fetcher.api:app --reload
```

3. API Endpoints:

- `GET /bulk-deals?trade_date=YYYY-MM-DD`  
  Fetch bulk deal data for the given trade date.

- `GET /block-deals?trade_date=YYYY-MM-DD`  
  Fetch block deal data for the given trade date.

- `GET /stock-data?symbol=SYMBOL&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`  
  Fetch historical stock data for the given symbol and date range.

Example:

```bash
curl "http://127.0.0.1:8000/stock-data?symbol=RELIANCE&start_date=2023-01-01&end_date=2023-01-31"
curl "http://127.0.0.1:8000/bulk-deals?trade_date=2025-07-30"
curl "http://127.0.0.1:8000/block-deals?trade_date=2025-07-25"
```

## Notes

- The project uses the `nsepy` library to fetch data.
- You can modify the date range and stock symbol as needed.
- Extend the project to add more features for swing trading and investment analysis.
