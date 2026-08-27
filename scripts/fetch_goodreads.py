import json
import os
import time
import urllib.request
import xml.etree.ElementTree as ET

BASE_URL = "https://www.goodreads.com/review/list_rss/28031214-valerio?shelf=read&per_page=100&page="
os.makedirs("_data", exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
books = []
page = 1

while True:
    url = f"{BASE_URL}{page}"
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        items = root.findall(".//item")
        
        # Stop looping if no books remain on the current page
        if not items:
            break

        for item in items:
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

        print(f"Fetched page {page}: {len(items)} books.")
        page += 1
        time.sleep(1)  # Brief pause between requests

    except Exception as e:
        print(f"Error fetching page {page}: {e}")
        break

with open("_data/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, indent=2, ensure_ascii=False)

print(f"Successfully updated _data/books.json with {len(books)} total books.")
