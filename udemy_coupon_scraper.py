"""
Udemy Coupon Scraper Module

This module fetches coupon-based Udemy courses from multiple sources:
- Real Discount (real.discount)
- Discudemy (discudemy.com)

Author: AI Assistant
Date: July 3, 2025
"""

import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
import logging
from typing import List, Dict, Optional
from urllib.parse import urlparse, parse_qs
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class UdemyCouponScraper:
    """
    A scraper class to fetch coupon-based Udemy courses from multiple sources.
    """
    
    def __init__(self):
        """Initialize the scraper with default headers to avoid detection."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'DNT': '1'
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def _make_request(self, url: str, timeout: int = 30) -> Optional[requests.Response]:
        """
        Make a safe HTTP request with error handling.
        
        Args:
            url (str): The URL to request
            timeout (int): Request timeout in seconds
            
        Returns:
            Optional[requests.Response]: Response object or None if failed
        """
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
    
    def _extract_udemy_url(self, url: str) -> Optional[str]:
        """
        Extract and validate Udemy URL from a redirect or affiliate link.
        
        Args:
            url (str): The URL to extract from
            
        Returns:
            Optional[str]: Clean Udemy URL or None if invalid
        """
        try:
            # If it's already a udemy.com URL, return it
            if 'udemy.com' in url:
                return url
            
            # Follow redirects to get the final URL
            response = self._make_request(url)
            if response:
                final_url = response.url
                if 'udemy.com' in final_url:
                    return final_url
                    
        except Exception as e:
            logger.error(f"Failed to extract Udemy URL from {url}: {e}")
            
        return None
    
    def scrape_real_discount(self) -> List[Dict[str, str]]:
        """
        Scrape courses from Real Discount website.
        
        Returns:
            List[Dict[str, str]]: List of course dictionaries
        """
        courses = []
        
        try:
            # Real Discount API endpoint
            api_url = "https://cdn.real.discount/api/courses"
            params = {
                'page': 1,
                'limit': 500,
                'sortBy': 'sale_start',
                'store': 'Udemy',
                'freeOnly': 'true'
            }
            
            # Custom headers for Real Discount API
            api_headers = self.headers.copy()
            api_headers.update({
                'Host': 'cdn.real.discount',
                'Referer': 'https://www.real.discount/',
                'Accept': 'application/json, text/plain, */*'
            })
            
            logger.info("Fetching courses from Real Discount...")
            response = requests.get(api_url, params=params, headers=api_headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            items = data.get('items', [])
            
            logger.info(f"Found {len(items)} courses from Real Discount")
            
            for item in items:
                if item.get('store') == 'Sponsored':
                    continue
                    
                title = item.get('name', '').strip()
                url = item.get('url', '').strip()
                
                if title and url:
                    # Extract clean Udemy URL
                    udemy_url = self._extract_udemy_url(url)
                    if udemy_url:
                        courses.append({
                            'title': title,
                            'url': udemy_url,
                            'source': 'real.discount'
                        })
                        
        except Exception as e:
            logger.error(f"Error scraping Real Discount: {e}")
            
        return courses
    
    def scrape_discudemy(self) -> List[Dict[str, str]]:
        """
        Scrape courses from Discudemy website.
        
        Returns:
            List[Dict[str, str]]: List of course dictionaries
        """
        courses = []
        
        try:
            logger.info("Fetching courses from Discudemy...")
            
            # Scrape multiple pages concurrently
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                # Submit page scraping tasks
                future_to_page = {
                    executor.submit(self._scrape_discudemy_page, page): page 
                    for page in range(1, 6)  # Scrape first 5 pages
                }
                
                for future in concurrent.futures.as_completed(future_to_page):
                    page = future_to_page[future]
                    try:
                        page_courses = future.result()
                        courses.extend(page_courses)
                        logger.info(f"Scraped {len(page_courses)} courses from Discudemy page {page}")
                    except Exception as e:
                        logger.error(f"Error scraping Discudemy page {page}: {e}")
                        
        except Exception as e:
            logger.error(f"Error scraping Discudemy: {e}")
            
        return courses
    
    def _scrape_discudemy_page(self, page: int) -> List[Dict[str, str]]:
        """
        Scrape a single page from Discudemy.
        
        Args:
            page (int): Page number to scrape
            
        Returns:
            List[Dict[str, str]]: List of course dictionaries from this page
        """
        courses = []
        
        try:
            url = f"https://www.discudemy.com/all/{page}"
            response = self._make_request(url)
            
            if not response:
                return courses
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all course cards
            course_cards = soup.find_all('a', {'class': 'card-header'})
            
            # Process each course card
            for card in course_cards:
                try:
                    title = card.get_text(strip=True)
                    href = card.get('href', '')
                    
                    if title and href:
                        # Extract course ID from href
                        course_id = href.split('/')[-1]
                        
                        # Get the actual Udemy URL
                        udemy_url = self._get_discudemy_course_url(course_id)
                        
                        if udemy_url:
                            courses.append({
                                'title': title,
                                'url': udemy_url,
                                'source': 'discudemy.com'
                            })
                            
                except Exception as e:
                    logger.error(f"Error processing Discudemy course card: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping Discudemy page {page}: {e}")
            
        return courses
    
    def _get_discudemy_course_url(self, course_id: str) -> Optional[str]:
        """
        Get the actual Udemy URL for a Discudemy course.
        
        Args:
            course_id (str): The course ID from Discudemy
            
        Returns:
            Optional[str]: The Udemy URL or None if not found
        """
        try:
            url = f"https://www.discudemy.com/go/{course_id}"
            response = self._make_request(url)
            
            if not response:
                return None
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the segment with the Udemy link
            segment = soup.find('div', {'class': 'ui segment'})
            if segment:
                link = segment.find('a')
                if link and link.get('href'):
                    udemy_url = link.get('href')
                    
                    # Validate it's a Udemy URL
                    if 'udemy.com' in udemy_url:
                        return udemy_url
                        
        except Exception as e:
            logger.error(f"Error getting Discudemy course URL for {course_id}: {e}")
            
        return None
    
    def get_all_courses(self) -> List[Dict[str, str]]:
        """
        Get all courses from all supported sources.
        
        Returns:
            List[Dict[str, str]]: List of all course dictionaries
        """
        all_courses = []
        
        # Scrape from all sources
        real_discount_courses = self.scrape_real_discount()
        discudemy_courses = self.scrape_discudemy()
        
        # Combine all courses
        all_courses.extend(real_discount_courses)
        all_courses.extend(discudemy_courses)
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_courses = []
        
        for course in all_courses:
            if course['url'] not in seen_urls:
                seen_urls.add(course['url'])
                unique_courses.append(course)
                
        logger.info(f"Total unique courses found: {len(unique_courses)}")
        
        return unique_courses


def main():
    """
    Example usage of the UdemyCouponScraper class.
    """
    scraper = UdemyCouponScraper()
    
    print("🔍 Starting Udemy coupon scraper...")
    print("=" * 50)
    
    # Get all courses
    courses = scraper.get_all_courses()
    
    # Display results
    print(f"\n📊 Found {len(courses)} unique courses with coupons:")
    print("=" * 50)
    
    for i, course in enumerate(courses[:10], 1):  # Show first 10 courses
        print(f"\n{i}. {course['title']}")
        print(f"   Source: {course['source']}")
        print(f"   URL: {course['url']}")
    
    if len(courses) > 10:
        print(f"\n... and {len(courses) - 10} more courses")
    
    return courses


if __name__ == "__main__":
    main()
