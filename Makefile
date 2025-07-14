install:
	pip install -r deps/requirements.txt

setup-env:
	cp .env.example .env

run:
	scrapy crawl proxy_spider -a max_items=$(MAX)