from datetime import date
import pandas as pd
from nselib import capital_market
from datetime import datetime, timedelta
import logging

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

def fetch_bulk_deal_summary(trade_date):
    """
    Fetch bulk deal data for the given trade date and return total buy and sell QuantityTraded
    grouped by Symbol and ClientName where TradePrice or Wght.Avg.Price > 200.

    Args:
        trade_date (str or date): Trade date in 'dd-mm-yyyy' format or date object

    Returns:
        pandas.DataFrame: Aggregated bulk deal summary data

    Raises:
        ValueError: If no data is found or no data matches the criteria
    """
    try:
        data = fetch_bulk_deal_data(trade_date)
        logging.info(f"Bulk deal data columns: {list(data.columns)}")
        # Check if required columns exist
        required_cols = ['TradePrice/Wght.Avg.Price', 'Symbol', 'ClientName', 'QuantityTraded', 'Buy/Sell']
        for col in required_cols:
            if col not in data.columns:
                raise ValueError(f"Required column '{col}' not found in bulk deal data")
        # Convert 'TradePrice/Wght.Avg.Price' to numeric after removing commas
        data['TradePrice/Wght.Avg.Price'] = data['TradePrice/Wght.Avg.Price'].str.replace(',', '').astype(float)
        # Filter rows where TradePrice/Wght.Avg.Price > 200
        filtered = data[data['TradePrice/Wght.Avg.Price'] > 200]
        if filtered.empty:
            raise ValueError(f"No bulk deal data found with TradePrice/Wght.Avg.Price > 200 for trade date {trade_date}")
        # Group by Symbol and ClientName and aggregate total buy and sell QuantityTraded
        # Since Buy/Sell column exists, we need to separate buy and sell quantities
        filtered['QuantityTraded'] = filtered['QuantityTraded'].str.replace(',', '').astype(float)
        buy_data = filtered[filtered['Buy/Sell'].str.upper() == 'BUY']
        sell_data = filtered[filtered['Buy/Sell'].str.upper() == 'SELL']

        buy_summary = buy_data.groupby(['Symbol', 'ClientName']).agg(
            TotalBuyQuantity=('QuantityTraded', 'sum')
        ).reset_index()

        sell_summary = sell_data.groupby(['Symbol', 'ClientName']).agg(
            TotalSellQuantity=('QuantityTraded', 'sum')
        ).reset_index()

        # Merge buy and sell summaries
        summary = buy_summary.merge(sell_summary, on=['Symbol', 'ClientName'], how='outer').fillna(0)
        return summary
    except Exception as e:
        logging.error(f"Error in fetch_bulk_deal_summary: {e}", exc_info=True)
        raise
