import json
import yfinance as yf

def get_financial_metrics(ticker: str) -> str:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        metrics = {
            "ticker": ticker.upper(),
            "price_usd": info.get("currentPrice") or info.get("regularMarketPrice"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "market_cap_usd": info.get("marketCap", "N/A"),
        }
        return json.dump(metrics)
    except Exception as e:
        return f"Exception ${e}"