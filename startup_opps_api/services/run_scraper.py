from scrapy.crawler import CrawlerRunner
from startup_opps_api.scraper.scrapy_spider import StartupOpportunitiesSpider
from twisted.internet import asyncioreactor
from scrapy.utils.project import get_project_settings
import asyncio
from twisted.internet import defer

# Install asyncio reactor
asyncioreactor.install()

def scrape_opportunities(keyword, region=None, type=None):
    results = []

    def collect_data(item):
        results.append(item)

    async def run_spider():
        runner = CrawlerRunner(get_project_settings())
        spider = StartupOpportunitiesSpider
        await runner.crawl(spider, keyword=keyword, region=region, type=type)
        return results

    # Run in a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(run_spider())
    finally:
        loop.close()

    return results
