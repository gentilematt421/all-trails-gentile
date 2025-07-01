"""
AllTrails Web Scraper Module

This module contains the core scraping functionality for extracting hike data
from AllTrails pages. It follows single responsibility principle by focusing
only on data extraction logic.
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import random
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class HikeData:
    """Data class representing hike information extracted from AllTrails."""
    name: str = ""
    location: str = ""
    difficulty: str = ""
    length: str = ""
    elevation_gain: str = ""
    route_type: str = ""
    rating: str = ""
    reviews_count: str = ""
    description: str = ""
    features: List[str] = None
    
    def __post_init__(self):
        if self.features is None:
            self.features = []


class AllTrailsScraper:
    """Handles scraping of AllTrails hike pages."""
    
    def __init__(self):
        # Create a session for better connection management
        self.session = requests.Session()
        
        # More realistic browser headers to avoid detection
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"'
        }
        
        # Apply headers to session
        self.session.headers.update(self.headers)
    
    def scrape_hike(self, url: str) -> Optional[HikeData]:
        """
        Scrape hike information from an AllTrails page.
        
        Args:
            url: The AllTrails hike URL to scrape
            
        Returns:
            HikeData object containing extracted information, or None if scraping fails
        """
        max_retries = 5  # Increased retries
        for attempt in range(max_retries):
            try:
                response = self._make_request(url)
                soup = self._parse_html(response.content)
                return self._extract_hike_data(soup)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    if attempt < max_retries - 1:
                        # Wait longer before retrying with different headers
                        wait_time = random.uniform(5, 15)  # Longer wait
                        time.sleep(wait_time)
                        self._rotate_user_agent()
                        continue
                    else:
                        raise ScrapingError("Access denied (403). AllTrails may be blocking automated requests. Try again later or use a different URL.")
                else:
                    raise ScrapingError(f"HTTP Error {e.response.status_code}: {str(e)}")
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(2, 5))
                    continue
                else:
                    raise ScrapingError(f"Failed to scrape hike data: {str(e)}")
    
    def _rotate_user_agent(self):
        """Rotate to a different user agent to avoid detection."""
        user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
        ]
        new_agent = random.choice(user_agents)
        self.session.headers.update({'User-Agent': new_agent})
    
    def _make_request(self, url: str) -> requests.Response:
        """Make HTTP request to the given URL."""
        # Add a longer delay to be more human-like
        time.sleep(random.uniform(3, 8))
        
        # Use session for better connection management
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response
    
    def _parse_html(self, content: bytes) -> BeautifulSoup:
        """Parse HTML content using BeautifulSoup."""
        return BeautifulSoup(content, 'html.parser')
    
    def _extract_hike_data(self, soup: BeautifulSoup) -> HikeData:
        """Extract hike information from parsed HTML."""
        hike_data = HikeData()
        
        hike_data.name = self._extract_name(soup)
        hike_data.location = self._extract_location(soup)
        hike_data.difficulty, hike_data.length, hike_data.elevation_gain = self._extract_stats(soup)
        hike_data.rating = self._extract_rating(soup)
        hike_data.reviews_count = self._extract_reviews_count(soup)
        hike_data.description = self._extract_description(soup)
        hike_data.features = self._extract_features(soup)
        
        return hike_data
    
    def _extract_name(self, soup: BeautifulSoup) -> str:
        """Extract hike name from the page."""
        # Try multiple selectors for the name
        name_selectors = [
            'h1',
            '[data-testid="trail-title"]',
            '.styles-module__title___2JX0j',
            'h1[class*="title"]'
        ]
        
        for selector in name_selectors:
            name_elem = soup.select_one(selector)
            if name_elem:
                return name_elem.get_text(strip=True)
        
        return ""
    
    def _extract_location(self, soup: BeautifulSoup) -> str:
        """Extract location from the page."""
        location_selectors = [
            'div[class*="location"]',
            '[data-testid="location"]',
            '.styles-module__location___2X7Xl',
            'p[class*="location"]'
        ]
        
        for selector in location_selectors:
            location_elem = soup.select_one(selector)
            if location_elem:
                return location_elem.get_text(strip=True)
        
        return ""
    
    def _extract_stats(self, soup: BeautifulSoup) -> tuple[str, str, str]:
        """Extract difficulty, length, and elevation gain from stats section."""
        difficulty = length = elevation_gain = ""
        
        # Try multiple selectors for stats
        stats_selectors = [
            'div[class*="trailStats"]',
            'div[class*="stat"]',
            '[data-testid="trail-stats"]',
            '.styles-module__trailStats___2JX0j'
        ]
        
        for selector in stats_selectors:
            stats_container = soup.select_one(selector)
            if stats_container:
                stats = stats_container.find_all(['div', 'span'], class_=re.compile(r'.*stat.*'))
                for stat in stats:
                    stat_text = stat.get_text(strip=True)
                    if 'difficulty' in stat_text.lower():
                        difficulty = stat_text
                    elif 'mi' in stat_text.lower() or 'km' in stat_text.lower():
                        length = stat_text
                    elif 'ft' in stat_text.lower() or 'm' in stat_text.lower():
                        elevation_gain = stat_text
                break
        
        return difficulty, length, elevation_gain
    
    def _extract_rating(self, soup: BeautifulSoup) -> str:
        """Extract rating from the page."""
        rating_selectors = [
            'span[class*="rating"]',
            '[data-testid="rating"]',
            '.styles-module__rating___1WBrE',
            'span[class*="star"]'
        ]
        
        for selector in rating_selectors:
            rating_elem = soup.select_one(selector)
            if rating_elem:
                return rating_elem.get_text(strip=True)
        
        return ""
    
    def _extract_reviews_count(self, soup: BeautifulSoup) -> str:
        """Extract reviews count from the page."""
        reviews_elem = soup.find('span', string=re.compile(r'\d+ reviews'))
        if reviews_elem:
            return reviews_elem.get_text(strip=True)
        
        # Try alternative patterns
        reviews_elem = soup.find('span', string=re.compile(r'\d+.*review'))
        if reviews_elem:
            return reviews_elem.get_text(strip=True)
        
        return ""
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract description from the page."""
        desc_selectors = [
            'div[class*="description"]',
            '[data-testid="description"]',
            '.styles-module__description___2X7Xl',
            'p[class*="description"]'
        ]
        
        for selector in desc_selectors:
            desc_elem = soup.select_one(selector)
            if desc_elem:
                return desc_elem.get_text(strip=True)
        
        return ""
    
    def _extract_features(self, soup: BeautifulSoup) -> List[str]:
        """Extract features/tags from the page."""
        features = set()  # Use a set to avoid duplicates
        features_selectors = [
            'div[class*="tags"]',
            '[data-testid="tags"]',
            '.styles-module__tags___3J6Xj',
            'div[class*="features"]'
        ]
        
        for selector in features_selectors:
            features_container = soup.select_one(selector)
            if features_container:
                # Find direct child elements that are likely to be feature tags
                feature_elements = features_container.find_all(['span', 'div', 'a'], recursive=False)
                for feature in feature_elements:
                    feature_text = feature.get_text(strip=True)
                    if feature_text and len(feature_text) > 1:  # Filter out empty or single-character text
                        features.add(feature_text)
                break
        
        return list(features)  # Convert set back to list


class ScrapingError(Exception):
    """Custom exception for scraping-related errors."""
    pass 