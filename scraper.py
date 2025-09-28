import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from typing import Dict, List, Optional
import urllib3

# Suppress SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebScraper:
    def __init__(self, delay: float = 1.0):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.delay = delay
    
    def scrape_url(self, url: str) -> Dict[str, str]:
        """Scrape content from a single URL"""
        try:
            response = self.session.get(url, timeout=10, verify=False)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
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
            
            return {
                'url': url,
                'title': title_text,
                'content': content[:10000],  # Limit content length
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'url': url,
                'title': '',
                'content': '',
                'status': f'error: {str(e)}'
            }
    
    def scrape_multiple_urls(self, urls: List[str]) -> List[Dict[str, str]]:
        """Scrape content from multiple URLs"""
        results = []
        for url in urls:
            result = self.scrape_url(url)
            results.append(result)
            time.sleep(self.delay)  # Be respectful to servers
        return results