import scrapy
import logging
from urllib.parse import urljoin, urlparse
from startup_opps_api.scraper.opportunity_sources import OPPORTUNITY_SOURCES, ADDITIONAL_SOURCES

class StartupOpportunitiesSpider(scrapy.Spider):
    name = "opps_spider"
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS': 16,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 429],
    }

    def __init__(self, keyword="", region="", type="", **kwargs):
        super().__init__(**kwargs)
        self.keyword = keyword
        self.region = region
        self.type = type
        self.start_urls = self._build_start_urls()
        self.logger.info(f"Starting spider with keyword: {keyword}, type: {type}, region: {region}")

    def _build_start_urls(self):
        """Build start URLs based on opportunity type and keyword"""
        urls = []
        
        # Get sources based on type
        if self.type and self.type.lower() in OPPORTUNITY_SOURCES:
            sources = OPPORTUNITY_SOURCES[self.type.lower()]
        else:
            # If no specific type, use all sources
            sources = []
            for type_sources in OPPORTUNITY_SOURCES.values():
                sources.extend(type_sources)
        
        # Add additional sources
        sources.extend(ADDITIONAL_SOURCES)
        
        for source in sources:
            if self.keyword:
                # Add keyword to search URL
                search_url = source['search_url']
                if '?' in search_url:
                    search_url += f"&q={self.keyword}"
                else:
                    search_url += f"?q={self.keyword}"
                urls.append(search_url)
            else:
                urls.append(source['search_url'])
        
        return urls

    def parse(self, response):
        """Parse response and extract opportunity data"""
        self.logger.info(f"Parsing: {response.url}")
        
        # Determine which source this is based on URL
        source_config = self._get_source_config(response.url)
        if not source_config:
            self.logger.warning(f"No source config found for: {response.url}")
            return
        
        # Extract opportunities using source-specific selectors
        opportunities = response.css(source_config['selectors']['container'])
        
        for opp in opportunities:
            try:
                opportunity_data = self._extract_opportunity_data(opp, source_config, response)
                if opportunity_data and self._is_valid_opportunity(opportunity_data):
                    yield opportunity_data
            except Exception as e:
                self.logger.error(f"Error extracting opportunity: {e}")
                continue

    def _get_source_config(self, url):
        """Get source configuration based on URL"""
        all_sources = []
        for type_sources in OPPORTUNITY_SOURCES.values():
            all_sources.extend(type_sources)
        all_sources.extend(ADDITIONAL_SOURCES)
        
        for source in all_sources:
            if source['base_url'] in url:
                return source
        return None

    def _extract_opportunity_data(self, opp, source_config, response):
        """Extract opportunity data using source-specific selectors"""
        selectors = source_config['selectors']
        
        title = self._safe_extract(opp, selectors.get('title', ''))
        organization = self._safe_extract(opp, selectors.get('organization', ''))
        deadline = self._safe_extract(opp, selectors.get('deadline', ''))
        url = self._safe_extract(opp, selectors.get('url', ''), is_url=True)
        
        if url and not url.startswith('http'):
            url = urljoin(response.url, url)
        
        return {
            "title": title,
            "organization": organization,
            "type": self.type or source_config.get('type', 'opportunity'),
            "deadline": deadline,
            "url": url,
            "source": source_config['name'],
            "region": self.region,
            "keyword": self.keyword
        }

    def _safe_extract(self, element, selector, is_url=False):
        """Safely extract text from element using CSS selector"""
        if not selector:
            return None
        
        try:
            if is_url:
                result = element.css(f"{selector}::attr(href)").get()
            else:
                result = element.css(f"{selector}::text").get()
            
            return result.strip() if result else None
        except Exception as e:
            self.logger.error(f"Error extracting with selector '{selector}': {e}")
            return None

    def _is_valid_opportunity(self, opportunity):
        """Validate that opportunity has required fields"""
        required_fields = ['title', 'url']
        return all(opportunity.get(field) for field in required_fields)
