import httpx
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

async def fetch_crypto_news(pair: str):
    query = pair[:3]  # e.g., SOL from SOLUSDT
    url = f"https://newsdata.io/api/1/news"
    params = {
        "apikey": "pub_cbedbf6c1fbb4fc9b5f36b5c157d73f4",  # 🔐 Replace this
        "q": query,
        "language": "en",
        "category": "business"
    }

    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(url, params=params)
            res.raise_for_status()
            articles = res.json().get("results", [])
    except:
        return "News sentiment: Unable to fetch news."

    # Combine top 3 headlines
    headlines = [a["title"] for a in articles[:3] if "title" in a]
    joined = ". ".join(headlines)

    sentiment = analyzer.polarity_scores(joined)
    compound = sentiment["compound"]

    if compound >= 0.2:
        return f"News sentiment: Positive — {headlines[0]}"
    elif compound <= -0.2:
        return f"News sentiment: Negative — {headlines[0]}"
    else:
        return f"News sentiment: Neutral — {headlines[0]}" if headlines else "No news found"
