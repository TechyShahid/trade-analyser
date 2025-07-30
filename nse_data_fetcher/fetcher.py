from datetime import date
from datetime import date
import pandas as pd
from nselib import capital_market

def fetch_stock_data(symbol, start_date, end_date):
    """
    Fetch historical stock data from NSE for the given symbol and date range using nselib capital_market module.
    
    Args:
        symbol (str): Stock symbol (e.g. 'RELIANCE')
        start_date (date): Start date for fetching data
        end_date (date): End date for fetching data
    
    Returns:
        pandas.DataFrame: Historical stock data
    
    Raises:
        ValueError: If no data is found for the given parameters
    """
    from_date = start_date.strftime('%d-%m-%Y')
    to_date = end_date.strftime('%d-%m-%Y')
    data = capital_market.price_volume_and_deliverable_position_data(symbol=symbol, from_date=from_date, to_date=to_date)
    if data.empty:
        raise ValueError(f"No data found for symbol {symbol} between {start_date} and {end_date}")
    return data

from datetime import datetime, timedelta

def fetch_bulk_deal_data(trade_date):
    """
    Fetch bulk deal data for the given trade date.
    
    Args:
        trade_date (str or date): Trade date in 'dd-mm-yyyy' format or date object
    
    Returns:
        pandas.DataFrame: Bulk deal data
    
    Raises:
        ValueError: If no data is found for the given date
    """
    if hasattr(trade_date, 'strftime'):
        trade_date_str = trade_date.strftime('%d-%m-%Y')
        from_date = datetime.strptime(trade_date_str, '%d-%m-%Y')
    else:
        trade_date_str = trade_date
        from_date = datetime.strptime(trade_date_str, '%d-%m-%Y')
    to_date = from_date + timedelta(days=1)
    to_date_str = to_date.strftime('%d-%m-%Y')
    data = capital_market.bulk_deal_data(from_date=trade_date_str, to_date=to_date_str)
    if data.empty:
        raise ValueError(f"No bulk deal data found for trade date {trade_date_str}")
    return data

def fetch_block_deal_data(trade_date):
    """
    Fetch block deal data for the given trade date.
    
    Args:
        trade_date (str or date): Trade date in 'dd-mm-yyyy' format or date object
    
    Returns:
        pandas.DataFrame: Block deal data
    
    Raises:
        ValueError: If no data is found for the given date
    """
    if hasattr(trade_date, 'strftime'):
        trade_date_str = trade_date.strftime('%d-%m-%Y')
        from_date = datetime.strptime(trade_date_str, '%d-%m-%Y')
    else:
        trade_date_str = trade_date
        from_date = datetime.strptime(trade_date_str, '%d-%m-%Y')
    to_date = from_date + timedelta(days=1)
    to_date_str = to_date.strftime('%d-%m-%Y')
    data = capital_market.block_deals_data(from_date=trade_date_str, to_date=to_date_str)
    if data.empty:
        raise ValueError(f"No block deal data found for trade date {trade_date_str}")
    return data

if __name__ == "__main__":
    # Example usage
    symbol = "RELIANCE"
    start_date = date(2023, 1, 1)
    end_date = date(2023, 12, 31)
    data = fetch_stock_data(symbol, start_date, end_date)
    print(data)
