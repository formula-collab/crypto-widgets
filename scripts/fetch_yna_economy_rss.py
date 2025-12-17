import json
import os
import time
import urllib.request
import xml.etree.ElementTree as ET

RSS_URL = "https://www.yna.co.kr/rss/economy.xml"
OUT_PATH = "data/yna_economy.json"

def text(el, default=""):
    if el is None or el.text is None:
        return default
    return el.text.strip()

def fetch_rss(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; crypto-widgets-bot/1.0)"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()

def main():
    xml_bytes = fetch_rss(RSS_URL)
    root = ET.fromstring(xml_bytes)

    channel = root.find("channel")
    if channel is None:
        raise RuntimeError("RSS channel not found")

    items = []
    for item in channel.findall("item"):
        title = text(item.find("title"))
        link = text(item.find("link"))
        pub_date = text(item.find("pubDate"))

        if not title or not link:
            continue

        items.append({"title": title, "link": link, "pubDate": pub_date})

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    payload = {
        "source": "Yonhap News RSS (Economy)",
        "rss_url": RSS_URL,
        "updated_at_unix": int(time.time()),
        "items": items[:30],
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
