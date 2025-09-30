import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse, parse_qsl, urlencode
import time
from typing import Dict, List, Optional, Set
import urllib3

# Suppress SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebScraper:
    def __init__(self, delay: float = 1.0, max_depth: int = 1, max_pages: int = 10):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.delay = delay
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.visited_urls: Set[str] = set()
        self.scraped_count = 0
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URLs for consistent comparison and storage.
        - Lowercase scheme and host
        - Remove fragment
        - Remove default ports
        - Strip common tracking query params
        - Remove trailing slash (except root)
        """
        try:
            parsed = urlparse(url)
            scheme = parsed.scheme.lower()
            hostname = (parsed.hostname or '').lower()
            # Drop leading www. for same-site comparisons
            hostname = hostname.lstrip('www.')
            port = parsed.port
            # Remove default ports
            netloc = hostname
            if port and not ((scheme == 'http' and port == 80) or (scheme == 'https' and port == 443)):
                netloc = f"{hostname}:{port}"

            # Clean query: drop tracking params
            query_pairs = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True)]
            drop_keys = {'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid'}
            cleaned_pairs = [(k, v) for k, v in query_pairs if k.lower() not in drop_keys]
            # Keep original order
            query = urlencode(cleaned_pairs)

            # Remove fragment
            fragment = ''

            # Normalize path: remove trailing slash except root
            path = parsed.path or '/'
            if len(path) > 1 and path.endswith('/'):
                path = path.rstrip('/')

            normalized = urlunparse((scheme, netloc, path, '', query, fragment))
            return normalized
        except Exception:
            return url

    def _is_same_site(self, url: str, base_url: str) -> bool:
        """Heuristic same-site check tolerant of www and subdomains."""
        a = urlparse(url)
        b = urlparse(base_url)
        host_a = (a.hostname or '').lower().lstrip('www.')
        host_b = (b.hostname or '').lower().lstrip('www.')
        return host_a == host_b
    
    def scrape_url(self, url: str, extract_links: bool = False) -> Dict[str, str]:
        """Scrape content from a single URL"""
        try:
            normalized_url = self._normalize_url(url)
            response = self.session.get(normalized_url, timeout=10, verify=False)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract links if requested
            links = []
            if extract_links:
                links = self._extract_links(soup, url)
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "No title"
            
            # Extract main content
            content = soup.get_text()
            # Clean up whitespace
            lines = (line.strip() for line in content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            content = ' '.join(chunk for chunk in chunks if chunk)
            
            result = {
                'url': normalized_url,
                'title': title_text,
                'content': content[:10000],  # Limit content length
                'status': 'success'
            }
            
            if extract_links:
                result['links'] = links
            
            return result
            
        except Exception as e:
            return {
                'url': self._normalize_url(url),
                'title': '',
                'content': '',
                'status': f'error: {str(e)}',
                'links': [] if extract_links else None
            }
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract and normalize links from a page"""
        links = []
        base_domain = urlparse(base_url).hostname or ''
        base_domain = base_domain.lower().lstrip('www.')
        
        # Extract from various link sources
        link_selectors = [
            'a[href]',  # Standard links
            'area[href]',  # Image map areas
            'link[href]',  # Link elements
        ]
        
        for selector in link_selectors:
            for element in soup.select(selector):
                href = element.get('href')
                if not href:
                    continue
                    
                # Convert relative URLs to absolute and normalize
                candidate = self._normalize_url(urljoin(base_url, href))
                parsed_url = urlparse(candidate)
                
                # Only include HTTP/HTTPS links from the same site
                if (parsed_url.scheme in ['http', 'https'] and 
                    self._is_same_site(candidate, base_url) and
                    candidate not in self.visited_urls and
                    self._is_valid_link(candidate)):
                    links.append(candidate)
        
        # Also look for links in navigation menus, content areas
        nav_links = soup.select('nav a[href], .menu a[href], .navigation a[href], .nav a[href]')
        content_links = soup.select('main a[href], .content a[href], article a[href], section a[href]')
        
        for link_set in [nav_links, content_links]:
            for link in link_set:
                href = link.get('href')
                if href:
                    candidate = self._normalize_url(urljoin(base_url, href))
                    parsed_url = urlparse(candidate)
                    
                    if (parsed_url.scheme in ['http', 'https'] and 
                        self._is_same_site(candidate, base_url) and
                        candidate not in self.visited_urls and
                        self._is_valid_link(candidate)):
                        links.append(candidate)
        
        return list(set(links))  # Remove duplicates
    
    def _is_valid_link(self, url: str) -> bool:
        """Check if a link should be followed"""
        # Skip common file extensions and fragments
        skip_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.doc', '.docx', 
                          '.mp4', '.mp3', '.avi', '.mov', '.wmv', '.css', '.js', '.xml', '.rss']
        parsed = urlparse(url)
        
        # Skip if it's a file download
        if any(parsed.path.lower().endswith(ext) for ext in skip_extensions):
            return False
        
        # Skip mailto, tel, javascript links
        if parsed.scheme in ['mailto', 'tel', 'javascript', 'ftp']:
            return False
        
        # Skip common non-content paths (keep this conservative)
        skip_paths = ['/login', '/register', '/cart', '/checkout', '/admin', '/wp-admin', 
                     '/feed', '/rss']
        if any(skip_path in parsed.path.lower() for skip_path in skip_paths):
            return False
        
        # Skip URLs with query parameters that suggest dynamic content
        # Allow common pagination/sorting to enable multi-level traversal
        q = parsed.query.lower()
        if q and (('search=' in q) or ('q=' in q) or ('filter=' in q)):
            return False
            
        return True
    
    def scrape_multiple_urls(self, urls: List[str]) -> List[Dict[str, str]]:
        """Scrape content from multiple URLs (single level only)"""
        results = []
        for url in urls:
            result = self.scrape_url(url, extract_links=False)
            results.append(result)
            time.sleep(self.delay)  # Be respectful to servers
        return results
    
    def scrape_with_depth(self, start_urls: List[str], depth: int = 2) -> List[Dict[str, str]]:
        """Scrape URLs with specified depth level"""
        self.max_depth = depth
        self.visited_urls.clear()
        self.scraped_count = 0
        
        results = []
        # Seed queue with normalized URLs
        urls_to_process = [(self._normalize_url(url), 0) for url in start_urls]  # (url, current_depth)
        
        while urls_to_process and self.scraped_count < self.max_pages:
            current_url, current_depth = urls_to_process.pop(0)
            
            # Skip if already visited
            if current_url in self.visited_urls:
                continue
                
            # Mark as visited
            self.visited_urls.add(current_url)
            
            print(f"Scraping (depth {current_depth}): {current_url}")
            
            # Scrape the current URL
            extract_links = current_depth < self.max_depth
            result = self.scrape_url(current_url, extract_links=extract_links)
            result['depth'] = current_depth
            results.append(result)
            
            self.scraped_count += 1
            
            # If successful and not at max depth, add found links to queue
            if (result['status'] == 'success' and 
                current_depth < self.max_depth and 
                'links' in result and 
                result['links']):
                
                # Prioritize different types of links
                nav_links = [self._normalize_url(link) for link in result['links'] if any(word in link.lower() for word in ['about', 'service', 'product', 'contact'])]
                content_links = [self._normalize_url(link) for link in result['links'] if self._normalize_url(link) not in nav_links]
                
                # Add navigation links first (higher priority)
                for link in nav_links[:3]:
                    if link not in self.visited_urls:
                        urls_to_process.append((link, current_depth + 1))
                
                # Then add content links
                for link in content_links[:7]:  # Increased from 5 to 7
                    if link not in self.visited_urls:
                        urls_to_process.append((link, current_depth + 1))
            
            # Respectful delay
            time.sleep(self.delay)
        
        return results
    
    def get_scraping_stats(self) -> Dict[str, int]:
        """Get statistics about the scraping session"""
        return {
            'total_pages_scraped': self.scraped_count,
            'total_urls_visited': len(self.visited_urls),
            'max_depth_configured': self.max_depth,
            'max_pages_configured': self.max_pages
        }