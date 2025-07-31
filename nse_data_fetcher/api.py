from fastapi import FastAPI, HTTPException, Query
from datetime import datetime
from nse_data_fetcher.fetcher import fetch_bulk_deal_data, fetch_block_deal_data, fetch_stock_data, fetch_bulk_deal_summary
from fastapi.responses import JSONResponse
import pandas as pd
import logging
import numpy as np
import json

app = FastAPI(title="NSE Data Fetcher API")

def parse_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

@app.get("/bulk-deals")
async def get_bulk_deals(trade_date: str = Query(..., description="Trade date in YYYY-MM-DD format")):
    date_obj = parse_date(trade_date)
    try:
        data = fetch_bulk_deal_data(date_obj)
        try:
            # Use pandas to_json with default handlers for NaN and infinite values
            json_str = data.to_json(orient="records", date_format="iso", double_precision=6, force_ascii=False, default_handler=str)
            records = json.loads(json_str)
            return JSONResponse(content=records)
        except ValueError as ve:
            logging.warning(f"ValueError during JSON serialization: {ve}")
            raise HTTPException(status_code=500, detail="Data contains non-serializable values")
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/block-deals")
async def get_block_deals(trade_date: str = Query(..., description="Trade date in YYYY-MM-DD format")):
    date_obj = parse_date(trade_date)
    try:
        data = fetch_block_deal_data(date_obj)
        if data.empty:
            logging.warning(f"No block deal data found for date {trade_date}")
            raise HTTPException(status_code=404, detail=f"No block deal data found for date {trade_date}")
        try:
            # Use pandas to_json with default handlers for NaN and infinite values
            json_str = data.to_json(orient="records", date_format="iso", double_precision=6, force_ascii=False, default_handler=str)
            records = json.loads(json_str)
            return JSONResponse(content=records)
        except ValueError as ve:
            logging.warning(f"ValueError during JSON serialization: {ve}")
            raise HTTPException(status_code=500, detail="Data contains non-serializable values")
    except ValueError as ve:
        logging.warning(f"ValueError: {ve}")
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logging.error(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/stock-data")
async def get_stock_data(
    symbol: str = Query(..., description="Stock symbol, e.g. RELIANCE"),
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format")
):
    start_date_obj = parse_date(start_date)
    end_date_obj = parse_date(end_date)
    if end_date_obj < start_date_obj:
        raise HTTPException(status_code=400, detail="end_date must be greater than or equal to start_date")
    try:
        data = fetch_stock_data(symbol, start_date_obj, end_date_obj)
        # Use pandas to_json with default handlers for NaN and infinite values
        json_str = data.to_json(orient="records", date_format="iso", double_precision=6, force_ascii=False, default_handler=str)
        records = json.loads(json_str)
        return JSONResponse(content=records)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/bulk-deals-summary")
async def get_bulk_deals_summary(trade_date: str = Query(..., description="Trade date in YYYY-MM-DD format")):
    date_obj = parse_date(trade_date)
    try:
        summary = fetch_bulk_deal_summary(date_obj)
        # Use pandas to_json with default handlers for NaN and infinite values
        json_str = summary.to_json(orient="records", date_format="iso", double_precision=6, force_ascii=False, default_handler=str)
        records = json.loads(json_str)
        return JSONResponse(content=records)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        import logging
        logging.error(f"Error in get_bulk_deals_summary endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/bulk-deals-columns")
async def get_bulk_deals_columns(trade_date: str = Query(..., description="Trade date in YYYY-MM-DD format")):
    date_obj = parse_date(trade_date)
    try:
        data = fetch_bulk_deal_data(date_obj)
        columns = list(data.columns)
        return JSONResponse(content={"columns": columns})
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
