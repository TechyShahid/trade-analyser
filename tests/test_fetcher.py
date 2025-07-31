import pytest
from datetime import date
import pandas as pd
import sys
import os

# Add the project root directory to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nse_data_fetcher.fetcher import fetch_bulk_deal_summary

def test_fetch_bulk_deal_summary_valid(monkeypatch):
    # Sample data to mock fetch_bulk_deal_data
    sample_data = pd.DataFrame({
        'TradePrice/Wght.Avg.Price': ['250', '300', '150'],
        'Symbol': ['AAA', 'BBB', 'CCC'],
        'ClientName': ['Client1', 'Client2', 'Client3'],
        'QuantityTraded': ['1,000', '2,000', '3,000'],
        'Buy/Sell': ['BUY', 'SELL', 'BUY']
    })

    def mock_fetch_bulk_deal_data(trade_date):
        return sample_data

    monkeypatch.setattr('nse_data_fetcher.fetcher.fetch_bulk_deal_data', mock_fetch_bulk_deal_data)

    trade_date = date(2023, 1, 1)
    summary = fetch_bulk_deal_summary(trade_date)

    # Check that only rows with price > 200 are included
    assert 'CCC' not in summary['Symbol'].values  # 150 price filtered out
    # Check that quantities are summed correctly
    buy_qty = summary.loc[summary['ClientName'] == 'Client1', 'TotalBuyQuantity'].values[0]
    sell_qty = summary.loc[summary['ClientName'] == 'Client2', 'TotalSellQuantity'].values[0]
    assert buy_qty == 1000.0
    assert sell_qty == 2000.0

def test_fetch_bulk_deal_summary_no_data(monkeypatch):
    def mock_fetch_bulk_deal_data(trade_date):
        return pd.DataFrame(columns=['TradePrice/Wght.Avg.Price', 'Symbol', 'ClientName', 'QuantityTraded', 'Buy/Sell'])

    monkeypatch.setattr('nse_data_fetcher.fetcher.fetch_bulk_deal_data', mock_fetch_bulk_deal_data)

    trade_date = date(2023, 1, 1)
    with pytest.raises(ValueError):
        fetch_bulk_deal_summary(trade_date)

def test_fetch_bulk_deal_summary_missing_columns(monkeypatch):
    sample_data = pd.DataFrame({
        'Symbol': ['AAA'],
        'ClientName': ['Client1'],
        'QuantityTraded': ['1000'],
        'Buy/Sell': ['BUY']
    })

    def mock_fetch_bulk_deal_data(trade_date):
        return sample_data

    monkeypatch.setattr('nse_data_fetcher.fetcher.fetch_bulk_deal_data', mock_fetch_bulk_deal_data)

    trade_date = date(2023, 1, 1)
    with pytest.raises(ValueError):
        fetch_bulk_deal_summary(trade_date)
