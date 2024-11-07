# Scrapy settings for judgement_scrap project

BOT_NAME = "judgement_scrap"
SPIDER_MODULES = ["judgement_scrap.spiders"]
NEWSPIDER_MODULE = "judgement_scrap.spiders"

# Set a custom User-Agent to mimic a common browser
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Disable robots.txt rules (caution: ensure you have permission to scrape the site)
ROBOTSTXT_OBEY = False

# Configure download delay to prevent overloading the server
DOWNLOAD_DELAY = 2  # Set delay in seconds

# Enable AutoThrottle to automatically adjust request rates based on server response
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2  # Initial download delay
AUTOTHROTTLE_MAX_DELAY = 10   # Max delay in case of high latencies
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0  # Number of requests to send in parallel

# Optional: Enable cookies if the site uses them to identify sessions
COOKIES_ENABLED = True

# Additional request headers (if the site needs specific headers)
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}

# Enable or configure HTTP caching to avoid unnecessary re-fetching (optional)
# HTTPCACHE_ENABLED = True
# HTTPCACHE_IGNORE_HTTP_CODES = [403]

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
