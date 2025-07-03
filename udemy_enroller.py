#!/usr/bin/env python3
"""
Udemy Course Enroller Module

This module handles the enrollment process for Udemy courses using browser cookies.
It can automatically enroll users in courses using coupons and handles various
enrollment scenarios and errors.
"""

import json
import logging
import re
import time
from typing import Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

import browser_cookie3
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UdemyEnroller:
    """
    Handles Udemy course enrollment using browser cookies.
    
    This class provides functionality to:
    - Extract cookies from Chrome browser
    - Validate user authentication
    - Enroll in courses using coupon codes
    - Handle various enrollment scenarios (already enrolled, expired coupons, etc.)
    """
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the Udemy Enroller.
        
        Args:
            timeout (int): Request timeout in seconds
        """
        self.timeout = timeout
        self.session = None
        self.cookies = None
        self.user_info = None
        self.enrolled_courses = set()
        
        # Setup session with retry strategy
        self._setup_session()
    
    def _setup_session(self):
        """Setup requests session with retry strategy and realistic headers."""
        self.session = requests.Session()
        
        # Setup retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set realistic headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        })
    
    def load_cookies_from_chrome(self) -> bool:
        """
        Load Udemy cookies from Chrome browser.
        Kept for backward compatibility.
        
        Returns:
            bool: True if cookies loaded successfully, False otherwise
        """
        return self.load_cookies_from_browser('chrome')
    
    def load_cookies_from_browser(self, browser_id: str) -> bool:
        """
        Load Udemy cookies from specified browser.
        
        Args:
            browser_id: Browser identifier (chrome, firefox, edge, safari)
            
        Returns:
            bool: True if cookies loaded successfully, False otherwise
        """
        try:
            from browser_manager import BrowserManager
            
            browser_manager = BrowserManager()
            success, cookie_dict, error_message = browser_manager.load_cookies_from_browser(browser_id)
            
            if not success:
                logger.error(f"Failed to load cookies from {browser_id}: {error_message}")
                return False
            
            # Update session with cookies
            # Convert cookie_dict back to browser_cookie3 format for session
            from browser_manager import BrowserManager
            browser_manager = BrowserManager()
            
            # Get raw cookies for session
            if browser_id == 'chrome':
                raw_cookies = browser_cookie3.chrome(domain_name='udemy.com')
            elif browser_id == 'firefox':
                raw_cookies = browser_cookie3.firefox(domain_name='udemy.com')
            elif browser_id == 'edge':
                raw_cookies = browser_cookie3.edge(domain_name='udemy.com')
            elif browser_id == 'safari':
                raw_cookies = browser_cookie3.safari(domain_name='udemy.com')
            elif browser_id == 'brave':
                raw_cookies = browser_cookie3.brave(domain_name='udemy.com')
            elif browser_id == 'opera':
                raw_cookies = browser_cookie3.opera(domain_name='udemy.com')
            elif browser_id == 'opera_gx':
                raw_cookies = browser_cookie3.opera_gx(domain_name='udemy.com')
            else:
                logger.error(f"Unsupported browser: {browser_id}")
                return False
            
            self.session.cookies.update(raw_cookies)
            self.cookies = cookie_dict
            
            logger.info(f"Cookies loaded successfully from {browser_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading cookies from {browser_id}: {e}")
            return False
    
    def validate_authentication(self) -> bool:
        """
        Validate user authentication by checking Udemy API.
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        try:
            logger.info("Validating authentication...")
            
            # Check authentication status
            response = self.session.get(
                'https://www.udemy.com/api-2.0/contexts/me/?header=True',
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                logger.error(f"Authentication check failed: {response.status_code}")
                return False
            
            data = response.json()
            
            # Check if user is logged in
            if not data.get('header', {}).get('isLoggedIn', False):
                logger.error("User is not logged in")
                return False
            
            # Store user information
            self.user_info = data.get('header', {}).get('user', {})
            logger.info(f"Authenticated as: {self.user_info.get('display_name', 'Unknown')}")
            
            # Load enrolled courses
            self._load_enrolled_courses()
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating authentication: {e}")
            return False
    
    def _load_enrolled_courses(self):
        """Load list of enrolled courses to avoid duplicate enrollments."""
        try:
            logger.info("Loading enrolled courses...")
            
            # Get enrolled courses from Udemy API
            url = 'https://www.udemy.com/api-2.0/users/me/subscribed-courses/'
            params = {
                'ordering': '-enroll_time',
                'fields[course]': 'enrollment_time,url',
                'page_size': 100
            }
            
            enrolled_courses = set()
            
            while url:
                response = self.session.get(url, params=params, timeout=self.timeout)
                
                if response.status_code != 200:
                    logger.warning(f"Failed to load enrolled courses: {response.status_code}")
                    break
                
                data = response.json()
                
                # Extract course slugs from URLs
                for course in data.get('results', []):
                    course_url = course.get('url', '')
                    if course_url:
                        # Extract slug from URL like /course/python-bootcamp/
                        slug_match = re.search(r'/course/([^/]+)/', course_url)
                        if slug_match:
                            enrolled_courses.add(slug_match.group(1))
                
                # Check for next page
                url = data.get('next')
                params = None  # Only use params for first request
            
            self.enrolled_courses = enrolled_courses
            logger.info(f"Loaded {len(enrolled_courses)} enrolled courses")
            
        except Exception as e:
            logger.error(f"Error loading enrolled courses: {e}")
            self.enrolled_courses = set()
    
    def _extract_course_info(self, course_url: str) -> Optional[Dict]:
        """
        Extract course information from Udemy course URL.
        
        Args:
            course_url (str): Udemy course URL with coupon
            
        Returns:
            dict: Course information including slug, coupon code, and course ID
        """
        try:
            parsed_url = urlparse(course_url)
            
            # Extract course slug from URL path
            path_parts = parsed_url.path.strip('/').split('/')
            if len(path_parts) < 2 or path_parts[0] != 'course':
                logger.error(f"Invalid course URL format: {course_url}")
                return None
            
            slug = path_parts[1]
            
            # Extract coupon code from query parameters
            query_params = parse_qs(parsed_url.query)
            coupon_code = query_params.get('couponCode', [None])[0]
            
            if not coupon_code:
                logger.error(f"No coupon code found in URL: {course_url}")
                return None
            
            return {
                'slug': slug,
                'coupon_code': coupon_code,
                'url': course_url
            }
            
        except Exception as e:
            logger.error(f"Error extracting course info from URL {course_url}: {e}")
            return None
    
    def _get_course_details(self, course_info: Dict) -> Optional[Dict]:
        """
        Get detailed course information from Udemy API.
        
        Args:
            course_info (dict): Basic course information
            
        Returns:
            dict: Detailed course information
        """
        try:
            # Get course page to extract course ID and other details
            response = self.session.get(course_info['url'], timeout=self.timeout)
            
            if response.status_code != 200:
                logger.error(f"Failed to load course page: {response.status_code}")
                return None
            
            # Extract course ID from the page
            course_id_match = re.search(r'"id":(\d+)', response.text)
            if not course_id_match:
                logger.error("Could not extract course ID from page")
                return None
            
            course_id = course_id_match.group(1)
            
            # Extract course title
            title_match = re.search(r'<title>(.+?)</title>', response.text)
            title = title_match.group(1) if title_match else course_info['slug']
            
            course_info.update({
                'course_id': course_id,
                'title': title
            })
            
            return course_info
            
        except Exception as e:
            logger.error(f"Error getting course details: {e}")
            return None
    
    def enroll_in_course(self, course_url: str) -> Tuple[bool, str]:
        """
        Enroll in a Udemy course using the provided coupon URL.
        
        Args:
            course_url (str): Udemy course URL with coupon code
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            logger.info(f"Attempting to enroll in course: {course_url}")
            
            # Extract course information
            course_info = self._extract_course_info(course_url)
            if not course_info:
                return False, "Invalid course URL"
            
            # Check if already enrolled
            if course_info['slug'] in self.enrolled_courses:
                message = f"Already enrolled in course: {course_info['slug']}"
                logger.info(message)
                return True, message
            
            # Get detailed course information
            course_info = self._get_course_details(course_info)
            if not course_info:
                return False, "Failed to get course details"
            
            # Attempt enrollment
            success, message = self._attempt_enrollment(course_info)
            
            if success:
                # Add to enrolled courses set
                self.enrolled_courses.add(course_info['slug'])
                logger.info(f"Successfully enrolled in: {course_info['title']}")
            
            return success, message
            
        except Exception as e:
            error_msg = f"Error enrolling in course: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    def _attempt_enrollment(self, course_info: Dict) -> Tuple[bool, str]:
        """
        Attempt to enroll in the course using Udemy's enrollment API.
        
        Args:
            course_info (dict): Course information
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # First, check if the course is free with coupon
            checkout_url = f"https://www.udemy.com/course/subscribe/?courseId={course_info['course_id']}"
            
            # Add coupon code to checkout URL
            if course_info['coupon_code']:
                checkout_url += f"&couponCode={course_info['coupon_code']}"
            
            # Attempt to enroll
            response = self.session.get(checkout_url, timeout=self.timeout)
            
            if response.status_code == 200:
                # Check if enrollment was successful by verifying course subscription
                return self._verify_enrollment(course_info)
            
            elif response.status_code == 404:
                return False, "Course not found or coupon expired"
            
            elif response.status_code == 403:
                return False, "Access denied - invalid coupon or course not available"
            
            else:
                return False, f"Enrollment failed with status: {response.status_code}"
                
        except Exception as e:
            return False, f"Enrollment error: {e}"
    
    def _verify_enrollment(self, course_info: Dict) -> Tuple[bool, str]:
        """
        Verify if enrollment was successful.
        
        Args:
            course_info (dict): Course information
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Check if course appears in subscribed courses
            check_url = f"https://www.udemy.com/api-2.0/users/me/subscribed-courses/{course_info['course_id']}/"
            params = {
                'fields[course]': '@default,buyable_object_type,primary_subcategory,is_private'
            }
            
            response = self.session.get(check_url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('_class') == 'course':
                    return True, f"Successfully enrolled in: {course_info['title']}"
                else:
                    return False, "Enrollment verification failed"
            
            elif response.status_code == 404:
                return False, "Course not found in enrolled courses"
            
            else:
                return False, f"Verification failed with status: {response.status_code}"
                
        except Exception as e:
            return False, f"Verification error: {e}"
    
    def enroll_in_multiple_courses(self, course_urls: List[str]) -> Dict[str, Dict]:
        """
        Enroll in multiple courses with rate limiting.
        
        Args:
            course_urls (List[str]): List of course URLs
            
        Returns:
            dict: Results for each course
        """
        results = {}
        
        logger.info(f"Starting enrollment for {len(course_urls)} courses")
        
        for i, course_url in enumerate(course_urls, 1):
            logger.info(f"Processing course {i}/{len(course_urls)}")
            
            success, message = self.enroll_in_course(course_url)
            
            results[course_url] = {
                'success': success,
                'message': message
            }
            
            # Rate limiting - wait between requests
            if i < len(course_urls):
                time.sleep(2)
        
        # Log summary
        successful = sum(1 for r in results.values() if r['success'])
        logger.info(f"Enrollment complete: {successful}/{len(course_urls)} successful")
        
        return results
    
    def get_enrollment_summary(self) -> Dict:
        """
        Get summary of enrollment capabilities and status.
        
        Returns:
            dict: Summary information
        """
        return {
            'authenticated': self.user_info is not None,
            'user_name': self.user_info.get('display_name', 'Unknown') if self.user_info else None,
            'enrolled_courses_count': len(self.enrolled_courses),
            'cookies_loaded': self.cookies is not None
        }
    
    def login_with_email_password(self, email: str, password: str) -> bool:
        """
        Login to Udemy using email and password.
        
        Args:
            email (str): User's email address
            password (str): User's password
            
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            logger.info(f"Attempting login with email: {email}")
            
            # Get login page to extract CSRF token
            login_url = "https://www.udemy.com/join/login-popup/"
            response = self.session.get(login_url, timeout=self.timeout)
            
            if response.status_code != 200:
                logger.error(f"Failed to load login page: {response.status_code}")
                return False
            
            # Extract CSRF token from cookies
            csrf_token = None
            for cookie in self.session.cookies:
                if cookie.name == 'csrftoken':
                    csrf_token = cookie.value
                    break
            
            if not csrf_token:
                logger.error("Could not find CSRF token")
                return False
            
            # Prepare login data
            login_data = {
                'email': email,
                'password': password,
                'csrfmiddlewaretoken': csrf_token,
                'locale': 'en_US',
                'next': 'https://www.udemy.com/'
            }
            
            # Set headers for login request
            login_headers = {
                'Referer': login_url,
                'X-CSRFToken': csrf_token,
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            
            # Perform login
            login_response = self.session.post(
                "https://www.udemy.com/join/login-popup/",
                data=login_data,
                headers=login_headers,
                timeout=self.timeout
            )
            
            if login_response.status_code == 200:
                # Check if login was successful by validating authentication
                return self.validate_authentication()
            else:
                logger.error(f"Login failed with status: {login_response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error during email login: {e}")
            return False
    
def main():
    """
    Example usage of the UdemyEnroller class.
    """
    # Initialize enroller
    enroller = UdemyEnroller()
    
    # Load cookies from Chrome
    if not enroller.load_cookies_from_chrome():
        print("Failed to load cookies from Chrome")
        return
    
    # Validate authentication
    if not enroller.validate_authentication():
        print("Authentication failed")
        return
    
    # Print summary
    summary = enroller.get_enrollment_summary()
    print(f"Authenticated as: {summary['user_name']}")
    print(f"Enrolled courses: {summary['enrolled_courses_count']}")
    
    # Example enrollment (uncomment to test)
    # course_url = "https://www.udemy.com/course/example-course/?couponCode=EXAMPLE123"
    # success, message = enroller.enroll_in_course(course_url)
    # print(f"Enrollment result: {success} - {message}")


if __name__ == "__main__":
    main()
