import json
from datetime import datetime, timezone

from pytrends.request import TrendReq

KEYWORD = "bitcoin"
GEO = ""              # 전세계
TIMEFRAME = "all"     # 2004~현재

def main():
    pytrends = TrendReq(hl="ko-KR", tz=540)  # KST
    pytrends.build_payload([KEYWORD], timeframe=TIMEFRAME, geo=GEO)

    df = pytrends.interest_over_time()
    if df.empty:
        raise RuntimeError("No data returned from Google Trends.")

    if "isPartial" in df.columns:
        df = df.drop(columns=["isPartial"])

    series = df[KEYWORD].reset_index()

    points = [
        {"date": row["date"].strftime("%Y-%m-%d"), "value": int(row[KEYWORD])}
        for _, row in series.iterrows()
    ]

    payload = {
        "keyword": KEYWORD,
        "geo": GEO or "WORLD",
        "timeframe": TIMEFRAME,
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "points": points,
    }

    with open("data/bitcoin_trends.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
