# from crawl4ai import AsyncWebCrawler, BrowserConfig

# browser_cfg = BrowserConfig(
#     browser_type="chromium",
#     headless=True,
#     verbose=True
# )

# crawler = AsyncWebCrawler(config=browser_cfg)
# print("Crawler Loaded....")

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

markdown_generator = DefaultMarkdownGenerator(
    content_filter=PruningContentFilter(
        threshold=0.5,
        threshold_type="dynamic",
        min_word_threshold=50,
    ),
    options={
        "ignore_links": True,
        "ignore_images": True,
    },
)

run_config = CrawlerRunConfig(
    word_count_threshold=10,
    markdown_generator=markdown_generator,
    exclude_external_images=True,
    exclude_external_links=True,
    page_timeout=15000,
    excluded_tags=[
        "script",
        "style",
        "nav",
        "footer",
        "header",
    ]
)

crawler = AsyncWebCrawler()
print("Crawler Loaded....")
