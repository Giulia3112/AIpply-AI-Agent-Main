"""
Enhanced scraper service that extracts detailed opportunity information from database websites
"""

import logging
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from startup_opps_api.scraper.enhanced_parser import EnhancedOpportunityParser
from startup_opps_api.scraper.opportunity_sources import OPPORTUNITY_SOURCES, ADDITIONAL_SOURCES

logger = logging.getLogger(__name__)

class EnhancedOpportunityScraper:
    """Enhanced scraper that extracts detailed opportunities from database websites"""
    
    def __init__(self):
        self.parser = EnhancedOpportunityParser()
        self.max_workers = 5  # Limit concurrent requests
        self.timeout = 15  # Timeout for each request
    
    def scrape_detailed_opportunities(self, keyword: str = "", type: str = "", region: str = "") -> List[Dict[str, Any]]:
        """
        Scrape detailed opportunities from database websites based on user criteria
        
        Args:
            keyword: Search keyword
            type: Opportunity type (scholarship, fellowship, accelerator)
            region: Geographic region filter
            
        Returns:
            List of detailed opportunity dictionaries
        """
        all_opportunities = []
        
        # Get relevant sources based on type
        sources = self._get_relevant_sources(type)
        
        # Use ThreadPoolExecutor for concurrent scraping
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit scraping tasks
            future_to_source = {
                executor.submit(self._scrape_single_source, source, keyword, type): source
                for source in sources
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_source, timeout=self.timeout * len(sources)):
                source = future_to_source[future]
                try:
                    opportunities = future.result(timeout=self.timeout)
                    all_opportunities.extend(opportunities)
                    logger.info(f"Scraped {len(opportunities)} opportunities from {source['name']}")
                except Exception as e:
                    logger.error(f"Error scraping {source['name']}: {e}")
                    # Add fallback entry for failed sources
                    all_opportunities.append(self._create_fallback_entry(source))
        
        # Filter and rank results
        filtered_opportunities = self.parser.filter_by_criteria(all_opportunities, keyword, type, region)
        
        # Remove duplicates and rank by relevance
        unique_opportunities = self._remove_duplicates(filtered_opportunities)
        ranked_opportunities = self._rank_by_relevance(unique_opportunities, keyword)
        
        return ranked_opportunities[:20]  # Return top 20 results
    
    def _get_relevant_sources(self, type: str) -> List[Dict[str, Any]]:
        """Get relevant sources based on opportunity type"""
        sources = []
        
        if type and type.lower() in OPPORTUNITY_SOURCES:
            sources.extend(OPPORTUNITY_SOURCES[type.lower()])
        else:
            # If no specific type, use all sources
            for type_sources in OPPORTUNITY_SOURCES.values():
                sources.extend(type_sources)
        
        # Add additional sources
        sources.extend(ADDITIONAL_SOURCES)
        
        # Filter out sources that are likely to block scraping
        reliable_sources = []
        for source in sources:
            domain = source.get('base_url', '').lower()
            # Skip sources that are known to block scraping
            if not any(blocked in domain for blocked in ['techcrunch', 'google', 'ycombinator']):
                reliable_sources.append(source)
        
        return reliable_sources[:10]  # Limit to top 10 most reliable sources
    
    def _scrape_single_source(self, source: Dict[str, Any], keyword: str, type: str) -> List[Dict[str, Any]]:
        """Scrape a single source website"""
        try:
            url = source['search_url']
            
            # Add keyword to search URL if provided
            if keyword:
                if '?' in url:
                    url += f"&q={keyword}"
                else:
                    url += f"?q={keyword}"
            
            # Parse the website
            opportunities = self.parser.parse_database_website(url, keyword, type)
            
            # Add source information to each opportunity
            for opp in opportunities:
                opp['source_url'] = source['search_url']
                opp['source_name'] = source['name']
            
            return opportunities
            
        except Exception as e:
            logger.error(f"Error scraping {source['name']}: {e}")
            return []
    
    def _create_fallback_entry(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """Create a fallback entry for sources that couldn't be scraped"""
        return {
            'title': f"Search {source['name']} for opportunities",
            'organization': source['name'],
            'type': 'opportunity',
            'url': source['search_url'],
            'source': source['name'],
            'description': f"Visit {source['name']} to search for opportunities manually",
            'is_fallback': True
        }
    
    def _remove_duplicates(self, opportunities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate opportunities based on title and URL"""
        seen = set()
        unique_opportunities = []
        
        for opp in opportunities:
            # Create a key based on title and URL
            key = (opp.get('title', '').lower().strip(), opp.get('url', '').lower().strip())
            
            if key not in seen and key[0] and key[1]:  # Ensure both title and URL exist
                seen.add(key)
                unique_opportunities.append(opp)
        
        return unique_opportunities
    
    def _rank_by_relevance(self, opportunities: List[Dict[str, Any]], keyword: str) -> List[Dict[str, Any]]:
        """Rank opportunities by relevance to the keyword"""
        if not keyword:
            return opportunities
        
        keyword_lower = keyword.lower()
        
        def calculate_relevance(opp):
            score = 0
            title = opp.get('title', '').lower()
            description = opp.get('description', '').lower()
            organization = opp.get('organization', '').lower()
            
            # Title matches get highest score
            if keyword_lower in title:
                score += 10
                # Exact title match gets bonus
                if title == keyword_lower:
                    score += 5
            
            # Description matches
            if keyword_lower in description:
                score += 5
            
            # Organization matches
            if keyword_lower in organization:
                score += 3
            
            # Bonus for having detailed information
            if opp.get('amount'):
                score += 2
            if opp.get('deadline'):
                score += 2
            if opp.get('eligibility'):
                score += 2
            if opp.get('location'):
                score += 1
            
            # Penalty for fallback entries
            if opp.get('is_fallback'):
                score -= 10
            
            return score
        
        # Sort by relevance score (highest first)
        return sorted(opportunities, key=calculate_relevance, reverse=True)

def scrape_detailed_opportunities(keyword: str = "", type: str = "", region: str = "") -> List[Dict[str, Any]]:
    """
    Main function to scrape detailed opportunities from database websites
    
    Args:
        keyword: Search keyword
        type: Opportunity type (scholarship, fellowship, accelerator)
        region: Geographic region filter
        
    Returns:
        List of detailed opportunity dictionaries
    """
    scraper = EnhancedOpportunityScraper()
    return scraper.scrape_detailed_opportunities(keyword, type, region)
