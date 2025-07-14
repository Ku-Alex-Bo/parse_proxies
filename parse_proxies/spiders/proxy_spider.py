import base64

import scrapy

from parse_proxies.items import ProxyItem
from parse_proxies.settings import MAX_ITEMS


class ProxySpider(scrapy.Spider):
    """
    - Парсит данные по css селекторам
    - Декодирует в utf-8
    """

    name = "proxy_spider"
    allowed_domains = ["advanced.name"]
    start_urls = ["https://advanced.name/freeproxy"]

    def __init__(self, max_items=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collected = 0
        self.max_items = int(max_items) if max_items else MAX_ITEMS

    def parse(self, response):
        rows = response.css("table#table_proxies tbody tr")
        for row in rows:
            if self.collected >= self.max_items:
                return

            ip_encoded = row.css("td[data-ip]::attr(data-ip)").get()
            port_encoded = row.css("td[data-port]::attr(data-port)").get()

            if not ip_encoded or not port_encoded:
                continue

            ip = base64.b64decode(ip_encoded).decode("utf-8")
            port = int(base64.b64decode(port_encoded).decode("utf-8"))
            protocols = [
                a.strip()
                for a in row.css("td:nth-child(4) a::text").getall()
                if a.strip()
            ]

            self.collected += 1
            yield ProxyItem(ip=ip, port=port, protocols=protocols)

        if self.collected < self.max_items:
            next_page = response.css(
                'ul.pagination li a:contains("»")::attr(href)'
            ).get()
            if not next_page:
                page_links = response.css("ul.pagination li a::attr(href)").getall()
                next_page = next((href for href in page_links if "page=" in href), None)
            if next_page:
                yield response.follow(next_page, callback=self.parse)
