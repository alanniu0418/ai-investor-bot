import yfinance as yf
from openai import OpenAI
from datetime import datetime

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

stocks = ["NVDA", "MSFT", "GOOGL", "AMZN", "META"]

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    current_price = hist["Close"].iloc[-1]
    high_52 = hist["Close"].max()
    low_52 = hist["Close"].min()
    drop_from_high = (high_52 - current_price) / high_52 * 100
    return {
        "ticker": ticker,
        "price": round(current_price, 2),
        "drop": round(drop_from_high, 2)
    }

data = [get_stock_data(s) for s in stocks]

prompt = f"""
You are a long term tech investor.

Today is {datetime.today().strftime('%Y-%m-%d')}.

Here is stock data:
{data}

Write a professional, concise daily investment brief explaining
which stocks are in accumulation zone for long term investors and why.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
)

article = response.choices[0].message.content

with open("daily_report.txt", "w") as f:
    f.write(article)

print("Report generated!")
