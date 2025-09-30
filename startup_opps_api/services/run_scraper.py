from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from pydispatch import dispatcher
from urllib.parse import urlparse

from startup_opps_api.scraper.scrapy_spider import StartupOpportunitiesSpider
from startup_opps_api.scraper.opportunity_sources import OPPORTUNITY_SOURCES, ADDITIONAL_SOURCES

def _should_use_js(url: str, type: str | None) -> bool:
    try:
        sources = []
        if type and type.lower() in OPPORTUNITY_SOURCES:
            for s in OPPORTUNITY_SOURCES[type.lower()]:
                if s.get("js"):
                    sources.append(s["base_url"]) 
        for s in ADDITIONAL_SOURCES:
            if s.get("js"):
                sources.append(s["base_url"]) 
        return any(base in url for base in sources)
    except Exception:
        return False

def _render_with_playwright(urls: list[str], selectors: dict[str, str], type: str | None):
    # Lazy import to avoid heavy dependency if not used
    from playwright.sync_api import sync_playwright
    items = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        for url in urls:
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                # Wait for container if provided
                container_sel = selectors.get("container")
                if container_sel:
                    try:
                        page.wait_for_selector(container_sel, timeout=8000)
                    except Exception:
                        pass
                # Extract nodes
                nodes = page.query_selector_all(container_sel) if container_sel else []
                for n in nodes:
                    try:
                        title_sel = selectors.get("title")
                        url_sel = selectors.get("url")
                        title = n.inner_text().strip() if title_sel is None else (n.query_selector(title_sel).inner_text().strip() if n.query_selector(title_sel) else None)
                        link = None
                        if url_sel and n.query_selector(url_sel):
                            link = n.query_selector(url_sel).get_attribute("href")
                        if link and not link.startswith("http"):
                            parsed = urlparse(url)
                            base = f"{parsed.scheme}://{parsed.netloc}"
                            link = base + link
                        if title and link:
                            items.append({
                                "title": title,
                                "organization": selectors.get("organization") or urlparse(url).netloc,
                                "type": type or "opportunity",
                                "eligibility": None,
                                "deadline": None,
                                "url": link,
                            })
                    except Exception:
                        continue
            except Exception:
                continue
        context.close()
        browser.close()
    return items


def scrape_opportunities(keyword, region=None, type=None):
    """Run the Scrapy spider synchronously and return collected items.

    This avoids Twisted/asyncio interop issues by using CrawlerProcess,
    which manages the reactor lifecycle internally.
    """
    results = []
    blocked_sources = set()
    visited_bases = set()

    def _item_scraped(item, response, spider):
        results.append(dict(item))

    def _response_received(response, request, spider):
        try:
            status = getattr(response, "status", None)
            url = getattr(response, "url", None)
            if url and status in {401, 403, 429}:  # unauthorized/forbidden/rate-limited
                blocked_sources.add(url)
            # robots.txt denial often shows as fetch to robots.txt or empty results; flag explicitly
            if url and url.endswith("/robots.txt"):
                blocked_sources.add(url)
            # Track visited base domains to provide fallback links when no items extracted
            if url:
                parsed = urlparse(url)
                if parsed.scheme and parsed.netloc:
                    visited_bases.add(f"{parsed.scheme}://{parsed.netloc}")
        except Exception:
            pass

    # Connect signals to collect items and detect blocked sources
    dispatcher.connect(_item_scraped, signal=signals.item_scraped)
    dispatcher.connect(_response_received, signal=signals.response_received)

    try:
        process = CrawlerProcess(get_project_settings())
        process.crawl(StartupOpportunitiesSpider, keyword=keyword, region=region, type=type)
        process.start()  # Blocks until crawling is finished
    finally:
        # Ensure we disconnect signal handlers
        dispatcher.disconnect(_item_scraped, signal=signals.item_scraped)
        dispatcher.disconnect(_response_received, signal=signals.response_received)

    # If Scrapy returned nothing for JS-heavy sources, use Playwright as fallback
    if not results:
        # Build the list of URLs we attempted for this type
        urls = set()
        if type and type.lower() in OPPORTUNITY_SOURCES:
            for s in OPPORTUNITY_SOURCES[type.lower()]:
                urls.add(s["search_url"])
        for s in ADDITIONAL_SOURCES:
            if s.get("type") == (type or s.get("type")):
                urls.add(s["search_url"])
        # Pick JS-enabled sources for fallback
        js_urls = []
        js_selectors = None
        for s in OPPORTUNITY_SOURCES.get(type.lower() if type else "accelerators", []):
            if s.get("js"):
                js_urls.append(s["search_url"])
                js_selectors = s["selectors"]  # use first matching selector set
        if js_urls and js_selectors:
            try:
                results = _render_with_playwright(js_urls[:3], js_selectors, type)
            except Exception:
                pass

    # Append helpful messages for blocked sources
    for src_url in sorted(blocked_sources):
        parsed = urlparse(src_url)
        base = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else src_url
        results.append({
            "title": "Sorry, this opportunity doesn't let me in. You will have to search for data yourself",
            "organization": base,
            "type": type or "accelerator",
            "eligibility": None,
            "deadline": None,
            "url": base,
        })

    # If nothing was scraped at all, provide fallback entries for visited bases
    if not results and visited_bases:
        for base in sorted(visited_bases):
            results.append({
                "title": "Sorry, this opportunity doesn't let me in. You will have to search for data yourself",
                "organization": base,
                "type": type or "accelerator",
                "eligibility": None,
                "deadline": None,
                "url": base,
            })

    return results
