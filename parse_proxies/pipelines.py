import time
from typing import Any, Dict, List

from scrapy import Spider

from .utils import get_save_id_proxies_dict, save_execution_time, save_results


class ParseProxiesPipeline:
    def __init__(self, token: str, upstreams: List[str]):
        self.token = token
        self.proxies: List[str] = []
        self.upstreams = upstreams
        self.start_time = time.time()

    @classmethod
    def from_crawler(cls, crawler) -> "ParseProxiesPipeline":
        token = crawler.settings.get("PERSONAL_TOKEN")
        upstreams = crawler.settings.get("UPSTREAMS")
        return cls(token, upstreams)

    def process_item(self, item: Dict[str, Any], spider: Spider) -> Dict[str, Any]:
        proxy = f"{item['ip']}:{item['port']}"
        self.proxies.append(proxy)
        return item

    def close_spider(self, spider: Spider) -> None:
        results = get_save_id_proxies_dict(
            token=self.token,
            proxies=self.proxies,
            upstreams=self.upstreams,
            chunk_size=25,
            max_workers=5,
        )
        save_results(results)
        save_execution_time(self.start_time)
