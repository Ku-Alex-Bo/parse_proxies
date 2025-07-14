import os

from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "parse_proxies"
SPIDER_MODULES = ["parse_proxies.spiders"]
NEWSPIDER_MODULE = "parse_proxies.spiders"

FEEDS = {
    "proxies.json": {
        "format": "json",
        "encoding": "utf8",
        "indent": 2,
        "overwrite": True,
    }
}

ITEM_PIPELINES = {
    "parse_proxies.pipelines.ParseProxiesPipeline": 300,
}

PERSONAL_TOKEN = os.getenv("PERSONAL_TOKEN")
MAX_ITEMS = int(os.getenv("MAX_PROXIES", 150))

CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 0.5
FEED_EXPORT_ENCODING = "utf-8"
UPSTREAMS = [
    "http://dav51tRB:SJ3irbuaRg@104.219.171.245:50100",
    "http://hA2EzKTl:McVvTeq6ND@203.27.70.107:50100",
    "http://OIzEHjcM:Zoyw0F2kEN@200.239.219.241:50100",
]
