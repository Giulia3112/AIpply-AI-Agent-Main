"""
Enhanced parser for detailed opportunity extraction from database websites
"""

import re
import logging
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class EnhancedOpportunityParser:
    """Enhanced parser for extracting detailed opportunity information"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def parse_database_website(self, url: str, keyword: str = "", type: str = "") -> List[Dict[str, Any]]:
        """
        Parse a database website and extract detailed opportunities that match the criteria
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Determine the website type and use appropriate parsing strategy
            domain = urlparse(url).netloc.lower()
            
            if 'wemakescholars' in domain:
                return self._parse_wemakescholars(soup, keyword, type)
            elif 'partiuintercambio' in domain:
                return self._parse_partiu_intercambio(soup, keyword, type)
            elif 'profellow' in domain:
                return self._parse_profellow(soup, keyword, type)
            elif 'opportunitydesk' in domain:
                return self._parse_opportunity_desk(soup, keyword, type)
            elif 'f6s' in domain:
                return self._parse_f6s(soup, keyword, type)
            elif 'idealist' in domain:
                return self._parse_idealist(soup, keyword, type)
            else:
                return self._parse_generic_database(soup, url, keyword, type)
                
        except Exception as e:
            logger.error(f"Error parsing {url}: {e}")
            return []
    
    def _parse_wemakescholars(self, soup: BeautifulSoup, keyword: str, type: str) -> List[Dict[str, Any]]:
        """Parse WeMakeScholars website"""
        opportunities = []
        
        # Look for scholarship cards/items
        scholarship_items = soup.find_all(['div', 'article'], class_=re.compile(r'scholarship|card|item'))
        
        for item in scholarship_items:
            try:
                # Extract title
                title_elem = item.find(['h1', 'h2', 'h3', 'h4'], class_=re.compile(r'title|name'))
                if not title_elem:
                    title_elem = item.find('a', class_=re.compile(r'title|name'))
                title = title_elem.get_text(strip=True) if title_elem else None
                
                # Extract organization
                org_elem = item.find(['span', 'div'], class_=re.compile(r'organization|university|provider'))
                organization = org_elem.get_text(strip=True) if org_elem else "WeMakeScholars"
                
                # Extract amount
                amount_elem = item.find(['span', 'div'], class_=re.compile(r'amount|value|money'))
                amount = amount_elem.get_text(strip=True) if amount_elem else None
                
                # Extract deadline
                deadline_elem = item.find(['span', 'div'], class_=re.compile(r'deadline|date|due'))
                deadline = deadline_elem.get_text(strip=True) if deadline_elem else None
                
                # Extract URL
                link_elem = item.find('a', href=True)
                url = link_elem['href'] if link_elem else None
                if url and not url.startswith('http'):
                    url = f"https://www.wemakescholars.com{url}"
                
                # Extract description
                desc_elem = item.find(['p', 'div'], class_=re.compile(r'description|summary|details'))
                description = desc_elem.get_text(strip=True) if desc_elem else None
                
                # Filter by keyword if provided
                if keyword and title and keyword.lower() not in title.lower():
                    continue
                
                if title and url:
                    opportunities.append({
                        'title': title,
                        'organization': organization,
                        'type': 'scholarship',
                        'amount': amount,
                        'deadline': deadline,
                        'description': description,
                        'url': url,
                        'source': 'WeMakeScholars',
                        'eligibility': self._extract_eligibility(item)
                    })
                    
            except Exception as e:
                logger.error(f"Error parsing WeMakeScholars item: {e}")
                continue
        
        return opportunities[:10]  # Limit to top 10 results
    
    def _parse_partiu_intercambio(self, soup: BeautifulSoup, keyword: str, type: str) -> List[Dict[str, Any]]:
        """Parse Partiu Intercambio website"""
        opportunities = []
        
        # Look for scholarship items
        items = soup.find_all(['div', 'article'], class_=re.compile(r'bolsa|scholarship|item'))
        
        for item in items:
            try:
                title_elem = item.find(['h1', 'h2', 'h3', 'h4'])
                title = title_elem.get_text(strip=True) if title_elem else None
                
                # Extract organization (often in Portuguese)
                org_elem = item.find(['span', 'div'], class_=re.compile(r'instituicao|organization'))
                organization = org_elem.get_text(strip=True) if org_elem else "Partiu Intercambio"
                
                # Extract amount/value
                amount_elem = item.find(['span', 'div'], class_=re.compile(r'valor|amount'))
                amount = amount_elem.get_text(strip=True) if amount_elem else None
                
                # Extract deadline
                deadline_elem = item.find(['span', 'div'], class_=re.compile(r'prazo|deadline'))
                deadline = deadline_elem.get_text(strip=True) if deadline_elem else None
                
                # Extract URL
                link_elem = item.find('a', href=True)
                url = link_elem['href'] if link_elem else None
                if url and not url.startswith('http'):
                    url = f"https://partiuintercambio.org{url}"
                
                # Filter by keyword
                if keyword and title and keyword.lower() not in title.lower():
                    continue
                
                if title and url:
                    opportunities.append({
                        'title': title,
                        'organization': organization,
                        'type': 'scholarship',
                        'amount': amount,
                        'deadline': deadline,
                        'url': url,
                        'source': 'Partiu Intercambio',
                        'eligibility': self._extract_eligibility(item)
                    })
                    
            except Exception as e:
                logger.error(f"Error parsing Partiu Intercambio item: {e}")
                continue
        
        return opportunities[:10]
    
    def _parse_profellow(self, soup: BeautifulSoup, keyword: str, type: str) -> List[Dict[str, Any]]:
        """Parse ProFellow website"""
        opportunities = []
        
        # Look for fellowship items
        items = soup.find_all(['div', 'article'], class_=re.compile(r'fellowship|opportunity|item'))
        
        for item in items:
            try:
                title_elem = item.find(['h1', 'h2', 'h3', 'h4'])
                title = title_elem.get_text(strip=True) if title_elem else None
                
                # Extract organization
                org_elem = item.find(['span', 'div'], class_=re.compile(r'organization|provider'))
                organization = org_elem.get_text(strip=True) if org_elem else "ProFellow"
                
                # Extract location
                location_elem = item.find(['span', 'div'], class_=re.compile(r'location|region'))
                location = location_elem.get_text(strip=True) if location_elem else None
                
                # Extract deadline
                deadline_elem = item.find(['span', 'div'], class_=re.compile(r'deadline|date'))
                deadline = deadline_elem.get_text(strip=True) if deadline_elem else None
                
                # Extract URL
                link_elem = item.find('a', href=True)
                url = link_elem['href'] if link_elem else None
                if url and not url.startswith('http'):
                    url = f"https://www.profellow.com{url}"
                
                # Filter by keyword
                if keyword and title and keyword.lower() not in title.lower():
                    continue
                
                if title and url:
                    opportunities.append({
                        'title': title,
                        'organization': organization,
                        'type': 'fellowship',
                        'location': location,
                        'deadline': deadline,
                        'url': url,
                        'source': 'ProFellow',
                        'eligibility': self._extract_eligibility(item)
                    })
                    
            except Exception as e:
                logger.error(f"Error parsing ProFellow item: {e}")
                continue
        
        return opportunities[:10]
    
    def _parse_opportunity_desk(self, soup: BeautifulSoup, keyword: str, type: str) -> List[Dict[str, Any]]:
        """Parse OpportunityDesk website"""
        opportunities = []
        
        # Look for opportunity items
        items = soup.find_all(['div', 'article'], class_=re.compile(r'opportunity|item|card'))
        
        for item in items:
            try:
                title_elem = item.find(['h1', 'h2', 'h3', 'h4'])
                title = title_elem.get_text(strip=True) if title_elem else None
                
                # Extract organization
                org_elem = item.find(['span', 'div'], class_=re.compile(r'organization|provider'))
                organization = org_elem.get_text(strip=True) if org_elem else "OpportunityDesk"
                
                # Extract deadline
                deadline_elem = item.find(['span', 'div'], class_=re.compile(r'deadline|date'))
                deadline = deadline_elem.get_text(strip=True) if deadline_elem else None
                
                # Extract URL
                link_elem = item.find('a', href=True)
                url = link_elem['href'] if link_elem else None
                if url and not url.startswith('http'):
                    url = f"https://opportunitydesk.org{url}"
                
                # Filter by keyword
                if keyword and title and keyword.lower() not in title.lower():
                    continue
                
                if title and url:
                    opportunities.append({
                        'title': title,
                        'organization': organization,
                        'type': type or 'opportunity',
                        'deadline': deadline,
                        'url': url,
                        'source': 'OpportunityDesk',
                        'eligibility': self._extract_eligibility(item)
                    })
                    
            except Exception as e:
                logger.error(f"Error parsing OpportunityDesk item: {e}")
                continue
        
        return opportunities[:10]
    
    def _parse_f6s(self, soup: BeautifulSoup, keyword: str, type: str) -> List[Dict[str, Any]]:
        """Parse F6S programs website"""
        opportunities = []
        
        # Look for program items
        items = soup.find_all(['div', 'article'], class_=re.compile(r'program|item|card'))
        
        for item in items:
            try:
                title_elem = item.find(['h1', 'h2', 'h3', 'h4'])
                title = title_elem.get_text(strip=True) if title_elem else None
                
                # Extract organization
                org_elem = item.find(['span', 'div'], class_=re.compile(r'organization|company'))
                organization = org_elem.get_text(strip=True) if org_elem else "F6S"
                
                # Extract location
                location_elem = item.find(['span', 'div'], class_=re.compile(r'location|region'))
                location = location_elem.get_text(strip=True) if location_elem else None
                
                # Extract deadline
                deadline_elem = item.find(['span', 'div'], class_=re.compile(r'deadline|date'))
                deadline = deadline_elem.get_text(strip=True) if deadline_elem else None
                
                # Extract URL
                link_elem = item.find('a', href=True)
                url = link_elem['href'] if link_elem else None
                if url and not url.startswith('http'):
                    url = f"https://www.f6s.com{url}"
                
                # Filter by keyword
                if keyword and title and keyword.lower() not in title.lower():
                    continue
                
                if title and url:
                    opportunities.append({
                        'title': title,
                        'organization': organization,
                        'type': 'accelerator',
                        'location': location,
                        'deadline': deadline,
                        'url': url,
                        'source': 'F6S',
                        'eligibility': self._extract_eligibility(item)
                    })
                    
            except Exception as e:
                logger.error(f"Error parsing F6S item: {e}")
                continue
        
        return opportunities[:10]
    
    def _parse_idealist(self, soup: BeautifulSoup, keyword: str, type: str) -> List[Dict[str, Any]]:
        """Parse Idealist website"""
        opportunities = []
        
        # Look for opportunity cards
        items = soup.find_all(['div', 'article'], class_=re.compile(r'opportunity|card|item'))
        
        for item in items:
            try:
                title_elem = item.find(['h1', 'h2', 'h3', 'h4'], class_=re.compile(r'title'))
                title = title_elem.get_text(strip=True) if title_elem else None
                
                # Extract organization
                org_elem = item.find(['span', 'div'], class_=re.compile(r'organization'))
                organization = org_elem.get_text(strip=True) if org_elem else "Idealist"
                
                # Extract location
                location_elem = item.find(['span', 'div'], class_=re.compile(r'location'))
                location = location_elem.get_text(strip=True) if location_elem else None
                
                # Extract deadline
                deadline_elem = item.find(['span', 'div'], class_=re.compile(r'deadline'))
                deadline = deadline_elem.get_text(strip=True) if deadline_elem else None
                
                # Extract URL
                link_elem = item.find('a', href=True)
                url = link_elem['href'] if link_elem else None
                if url and not url.startswith('http'):
                    url = f"https://www.idealist.org{url}"
                
                # Filter by keyword
                if keyword and title and keyword.lower() not in title.lower():
                    continue
                
                if title and url:
                    opportunities.append({
                        'title': title,
                        'organization': organization,
                        'type': 'fellowship',
                        'location': location,
                        'deadline': deadline,
                        'url': url,
                        'source': 'Idealist',
                        'eligibility': self._extract_eligibility(item)
                    })
                    
            except Exception as e:
                logger.error(f"Error parsing Idealist item: {e}")
                continue
        
        return opportunities[:10]
    
    def _parse_generic_database(self, soup: BeautifulSoup, url: str, keyword: str, type: str) -> List[Dict[str, Any]]:
        """Generic parser for unknown database websites"""
        opportunities = []
        
        # Try to find common patterns
        possible_containers = [
            soup.find_all(['div', 'article'], class_=re.compile(r'item|card|entry|post')),
            soup.find_all(['div', 'article'], class_=re.compile(r'opportunity|scholarship|fellowship|program')),
            soup.find_all(['li'], class_=re.compile(r'item|entry')),
            soup.find_all(['div'], class_=re.compile(r'listing|result'))
        ]
        
        items = []
        for container_list in possible_containers:
            if container_list:
                items = container_list
                break
        
        for item in items[:20]:  # Limit to first 20 items
            try:
                # Try to find title in various ways
                title = None
                for tag in ['h1', 'h2', 'h3', 'h4', 'h5']:
                    title_elem = item.find(tag)
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        break
                
                if not title:
                    # Try finding title in links
                    link_elem = item.find('a')
                    if link_elem:
                        title = link_elem.get_text(strip=True)
                
                # Extract URL
                link_elem = item.find('a', href=True)
                url_link = link_elem['href'] if link_elem else None
                if url_link and not url_link.startswith('http'):
                    base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
                    url_link = urljoin(base_url, url_link)
                
                # Filter by keyword
                if keyword and title and keyword.lower() not in title.lower():
                    continue
                
                if title and url_link:
                    opportunities.append({
                        'title': title,
                        'organization': urlparse(url).netloc,
                        'type': type or 'opportunity',
                        'url': url_link,
                        'source': urlparse(url).netloc,
                        'eligibility': self._extract_eligibility(item)
                    })
                    
            except Exception as e:
                logger.error(f"Error parsing generic item: {e}")
                continue
        
        return opportunities[:10]
    
    def _extract_eligibility(self, item) -> Optional[str]:
        """Extract eligibility requirements from an item"""
        try:
            # Look for common eligibility patterns
            eligibility_patterns = [
                r'eligibility|eligible|requirements?|criteria',
                r'age|years? old',
                r'degree|education|university|college',
                r'citizen|nationality|country',
                r'experience|work|professional'
            ]
            
            for pattern in eligibility_patterns:
                elem = item.find(text=re.compile(pattern, re.IGNORECASE))
                if elem:
                    # Get the parent element and extract text
                    parent = elem.parent
                    if parent:
                        return parent.get_text(strip=True)[:200]  # Limit length
            
            return None
        except Exception:
            return None
    
    def filter_by_criteria(self, opportunities: List[Dict[str, Any]], keyword: str = "", type: str = "", region: str = "") -> List[Dict[str, Any]]:
        """Filter opportunities based on user criteria"""
        filtered = opportunities
        
        if keyword:
            keyword_lower = keyword.lower()
            filtered = [opp for opp in filtered if 
                       keyword_lower in (opp.get('title') or '').lower() or
                       keyword_lower in (opp.get('description') or '').lower() or
                       keyword_lower in (opp.get('eligibility') or '').lower()]
        
        if type:
            type_lower = type.lower()
            filtered = [opp for opp in filtered if type_lower in opp.get('type', '').lower()]
        
        if region:
            region_lower = region.lower()
            filtered = [opp for opp in filtered if 
                       region_lower in (opp.get('location') or '').lower() or
                       region_lower in (opp.get('organization') or '').lower()]
        
        return filtered
