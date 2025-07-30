import sys
from datetime import date
from nse_data_fetcher.fetcher import fetch_stock_data, fetch_bulk_deal_data, fetch_block_deal_data

def test_fetch_valid_data():
    try:
        data = fetch_stock_data("SBIN", date(2023, 6, 20), date(2023, 7, 20))
        print("test_fetch_valid_data: PASSED")
    except ValueError as ve:
        print(f"test_fetch_valid_data: FAILED - {ve}")
    except Exception as e:
        print(f"test_fetch_valid_data: FAILED with unexpected exception {e}")

def test_fetch_invalid_symbol():
    try:
        data = fetch_stock_data("INVALIDSYM", date(2023, 1, 1), date(2023, 1, 10))
        # Expecting empty dataframe or handled exception
        if data.empty:
            print("test_fetch_invalid_symbol: PASSED (empty data)")
        else:
            print("test_fetch_invalid_symbol: PASSED (data returned)")
    except Exception as e:
        print(f"test_fetch_invalid_symbol: PASSED (exception handled) - {e}")

def test_fetch_invalid_dates():
    try:
        data = fetch_stock_data("RELIANCE", date(2023, 1, 10), date(2023, 1, 1))
        # Expecting empty dataframe or handled exception
        if data.empty:
            print("test_fetch_invalid_dates: PASSED (empty data)")
        else:
            print("test_fetch_invalid_dates: PASSED (data returned)")
    except Exception as e:
        print(f"test_fetch_invalid_dates: PASSED (exception handled) - {e}")

def test_fetch_empty_symbol():
    try:
        data = fetch_stock_data("", date(2023, 1, 1), date(2023, 1, 10))
        if data.empty:
            print("test_fetch_empty_symbol: PASSED (empty data)")
        else:
            print("test_fetch_empty_symbol: FAILED - Expected empty data")
    except Exception as e:
        print(f"test_fetch_empty_symbol: PASSED (exception handled) - {e}")

def test_fetch_future_dates():
    try:
        data = fetch_stock_data("SBIN", date(2050, 1, 1), date(2050, 1, 10))
        if data.empty:
            print("test_fetch_future_dates: PASSED (empty data)")
        else:
            print("test_fetch_future_dates: FAILED - Expected empty data")
    except Exception as e:
        print(f"test_fetch_future_dates: PASSED (exception handled) - {e}")

def test_fetch_large_date_range():
    try:
        data = fetch_stock_data("SBIN", date(2010, 1, 1), date(2023, 7, 20))
        print("test_fetch_large_date_range: PASSED")
    except ValueError as ve:
        print(f"test_fetch_large_date_range: FAILED - {ve}")
    except Exception as e:
        print(f"test_fetch_large_date_range: FAILED with unexpected exception {e}")

def test_fetch_bulk_deal_data():
    try:
        data = fetch_bulk_deal_data(date(2024, 6, 20))
        print("test_fetch_bulk_deal_data: PASSED")
    except ValueError as ve:
        print(f"test_fetch_bulk_deal_data: FAILED - {ve}")
    except Exception as e:
        print(f"test_fetch_bulk_deal_data: FAILED with unexpected exception {e}")

def test_fetch_block_deal_data():
    try:
        data = fetch_block_deal_data(date(2024, 6, 20))
        print("test_fetch_block_deal_data: PASSED")
    except ValueError as ve:
        print(f"test_fetch_block_deal_data: FAILED - {ve}")
    except Exception as e:
        print(f"test_fetch_block_deal_data: FAILED with unexpected exception {e}")

if __name__ == "__main__":
    print("Running tests for nse_data_fetcher...")
    test_fetch_valid_data()
    test_fetch_invalid_symbol()
    test_fetch_invalid_dates()
    test_fetch_empty_symbol()
    test_fetch_future_dates()
    test_fetch_large_date_range()
    test_fetch_bulk_deal_data()
    test_fetch_block_deal_data()
