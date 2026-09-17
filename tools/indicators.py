import json
import yfinance as yf

def calculate_sma(ticker: str, period: str) -> str:
    try: 
        stock = yf.Ticker(ticker)
        history = stock.history(period=f"{period + 15}d")
        if history.empty:
            return "Cannot find data"

        sma_val = history['Close'].tail(period).mean()
        latest_price = history['Close'].iloc[-1]

        return json.dumps({
            "ticker": ticker.upper(),
            "period": period,
            "sma_price": round(sma_val, 2),
            "latest_close": round(latest_price, 2),
            "signal": "BULLISH" if latest_price > sma_val else "BEARISH"
        })
                
    except Exception as e:
        return f"Exception {e}"