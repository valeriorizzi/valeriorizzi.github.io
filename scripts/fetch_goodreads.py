import json
import os
import urllib.request
import xml.etree.ElementTree as ET

GOODREADS_RSS = "https://www.goodreads.com/review/list_rss/28031214-valerio?shelf=read"

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

        cover = (
            get_text("book_large_image_url") or
            get_text("book_medium_image_url") or
            get_text("book_image_url")
        )

        books.append({
            "title": get_text("title"),
            "link": get_text("link"),
            "author": get_text("author_name"),
            "published": get_text("book_published"),
            "avgRating": get_text("average_rating"),
            "userRating": get_text("user_rating"),
            "dateAdded": get_text("user_date_added") or get_text("pubDate"),
            "coverUrl": cover
        })

    with open("_data/books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)

    print(f"Successfully updated _data/books.json with {len(books)} books.")

except Exception as e:
    print(f"Error fetching feed: {e}")
    exit(1)
