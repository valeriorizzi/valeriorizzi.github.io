import json
import os
import urllib.request
import xml.etree.ElementTree as ET

GOODREADS_RSS = "https://www.goodreads.com/review/list_rss/28031214-valerio?shelf=read"

# Ensure _data directory exists
os.makedirs("_data", exist_ok=True)

req = urllib.request.Request(
    GOODREADS_RSS,
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
)

try:
    with urllib.request.urlopen(req) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    books = []

    for item in root.findall(".//item"):
        def get_text(tag):
            el = item.find(tag)
            return el.text.strip() if el is not None and el.text else ""

        books.append({
            "title": get_text("title"),
            "author": get_text("author_name"),
            "rating": get_text("user_rating"),
            "dateAdded": get_text("user_date_added") or get_text("pubDate"),
            "coverUrl": get_text("book_large_image_url") or get_text("book_image_url")
        })

    with open("_data/books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)

    print(f"Successfully fetched {len(books)} books.")

except Exception as e:
    print(f"Error fetching feed: {e}")
    exit(1)
