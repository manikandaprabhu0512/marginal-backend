from crawl4ai import AsyncWebCrawler, BrowserConfig

browser_cfg = BrowserConfig(
    browser_type="chromium",
    headless=True,
    verbose=True
)

crawler = AsyncWebCrawler(config=browser_cfg)
print("Crawler Loaded....")
