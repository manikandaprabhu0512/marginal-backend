import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import requests


async def search_urls(query: str) -> list[dict]:

    no_of_pages = int(os.environ['SERPER_NUMBER_OF_PAGES'])

    search_data = []

    def fetch_page(query: str, page_number: int):
        payload = {
            "q": query,
            "page": page_number,
        }

        headers = {
            "X-API-KEY": os.getenv("SERPER_API_KEY"),
            "Content-Type": "application/json",
        }

        response = requests.post(
            os.getenv("SERPER_URL"),
            headers=headers,
            json=payload,
            timeout=30,
        )

        response.raise_for_status()

        return response.json().get("organic", [])


    with ThreadPoolExecutor(max_workers=no_of_pages) as executor:
        results = executor.map(
            lambda p: fetch_page(query, p),
            range(1, no_of_pages + 1),
        )

    search_data = []

    for organic in results:
        search_data.extend(organic)
        

    SKIP_DOMAINS = [
        "youtube.com", "youtu.be", "twitter.com", "x.com",
        "instagram.com", "facebook.com", "linkedin.com",
        "reddit.com", "pinterest.com", "tiktok.com"
    ]

    PREFERRED_DOMAINS = [
        "wikipedia.org", "github.com", ".gov", ".edu",
        "docs.", "developer."
    ]
    
    seen_domains = set()
    preferred = []
    others = []

    for r in search_data:
        url = r["link"]
        domain = urlparse(url).netloc

        if any(skip in domain for skip in SKIP_DOMAINS):
            continue

        if domain in seen_domains:
            continue
        seen_domains.add(domain)

        item = {"title": r.get("title", url), "url": url}

        if any(pref in domain for pref in PREFERRED_DOMAINS):
            preferred.append(item)
        else:
            others.append(item)

    return (preferred + others)[:20]