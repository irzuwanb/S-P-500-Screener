import requests
import pandas as pd
import os
from datetime import datetime, timedelta

API_KEY = os.environ.get("NEWS_API_KEY")

# Your ~20-30 watchlist tickers with company names for better search matching
WATCHLIST = [
    ("NVDA", "NVIDIA"),
    ("AAPL", "Apple"),
    ("MSFT", "Microsoft"),
    ("AMZN", "Amazon"),
    ("GOOGL", "Alphabet"),
    ("META", "Meta Platforms"),
    ("TSLA", "Tesla"),
    ("AMD", "Advanced Micro Devices"),
    ("AVGO", "Broadcom"),
    ("JPM", "JPMorgan Chase"),
    ("V", "Visa"),
    ("MA", "Mastercard"),
    ("LLY", "Eli Lilly"),
    ("UNH", "UnitedHealth"),
    ("XOM", "Exxon Mobil"),
    ("WMT", "Walmart"),
    ("HD", "Home Depot"),
    ("COST", "Costco"),
    ("PG", "Procter Gamble"),
    ("KO", "Coca-Cola"),
    ("NFLX", "Netflix"),
    ("CRM", "Salesforce"),
    ("ORCL", "Oracle"),
    ("ADBE", "Adobe"),
    ("INTU", "Intuit"),
    ("NOW", "ServiceNow"),
    ("PLTR", "Palantir"),
    ("CRWD", "CrowdStrike"),
    ("PANW", "Palo Alto Networks"),
    ("ANET", "Arista Networks"),
]

# Edit the WATCHLIST list above to match your actual 20-30 tickers.

def fetch_news_for_ticker(ticker, company_name):
    url = "https://newsapi.org/v2/everything"
    one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    params = {
        "q": company_name,
        "from": one_week_ago,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 5,
        "apiKey": API_KEY,
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()
        articles = data.get("articles", [])
    except Exception:
        articles = []

    rows = []
    for a in articles:
        rows.append({
            "Ticker": ticker,
            "Company": company_name,
            "Pulled On": datetime.now().strftime("%Y-%m-%d"),
            "Published": a.get("publishedAt", ""),
            "Title": a.get("title", ""),
            "Source": a.get("source", {}).get("name", ""),
            "URL": a.get("url", ""),
        })
    return rows


def main():
    if not API_KEY:
        print("ERROR: NEWS_API_KEY environment variable not set.")
        return

    all_rows = []
    for ticker, name in WATCHLIST:
        rows = fetch_news_for_ticker(ticker, name)
        all_rows.extend(rows)
        print("Fetched", len(rows), "articles for", ticker)

    new_df = pd.DataFrame(all_rows)

    # Append to existing log instead of overwriting, so history builds up over time
    if os.path.exists("news_log.csv"):
        old_df = pd.read_csv("news_log.csv")
        combined = pd.concat([old_df, new_df], ignore_index=True)
        combined = combined.drop_duplicates(subset=["Ticker", "Title", "Published"])
    else:
        combined = new_df

    combined.to_csv("news_log.csv", index=False)
    print("Saved", len(combined), "total articles to news_log.csv")


if __name__ == "__main__":
    main()
