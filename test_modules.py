#!/usr/bin/env python3
"""
Test Script for Udemy Course Enroller Modules

This script tests the individual modules to ensure they work correctly.
"""

import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_coupon_scraper():
    """Test the coupon scraper module."""
    try:
        print("\n=== Testing Coupon Scraper ===")
        
        from udemy_coupon_scraper import UdemyCouponScraper
        
        scraper = UdemyCouponScraper()
        
        # Test Real Discount scraping
        print("Testing Real Discount scraping...")
        rd_courses = scraper.scrape_real_discount()
        print(f"Real Discount courses found: {len(rd_courses)}")
        
        if rd_courses:
            print("Sample course:")
            print(f"  Title: {rd_courses[0]['title']}")
            print(f"  Source: {rd_courses[0]['source']}")
            print(f"  URL: {rd_courses[0]['url'][:80]}...")
        
        print("✓ Coupon scraper test passed")
        return True
        
    except Exception as e:
        print(f"✗ Coupon scraper test failed: {e}")
        return False


def test_filters():
    """Test the filters module."""
    try:
        print("\n=== Testing Filters ===")
        
        from filters import filter_courses, filter_by_rating, search_courses
        
        # Test data
        test_courses = [
            {
                'title': 'Python Programming Bootcamp',
                'rating': 4.5,
                'duration': 8.5,
                'language': 'English',
                'category': 'Programming',
                'instructor': 'John Doe',
                'url': 'https://example.com/course1'
            },
            {
                'title': 'JavaScript Fundamentals',
                'rating': 4.2,
                'duration': 5.0,
                'language': 'English',
                'category': 'Programming',
                'instructor': 'Jane Smith',
                'url': 'https://example.com/course2'
            },
            {
                'title': 'Data Science with R',
                'rating': 3.8,
                'duration': 12.0,
                'language': 'English',
                'category': 'Data Science',
                'instructor': 'Bob Johnson',
                'url': 'https://example.com/course3'
            }
        ]
        
        # Test rating filter
        high_rated = filter_by_rating(test_courses, 4.0)
        print(f"High-rated courses (>=4.0): {len(high_rated)}")
        
        # Test search
        python_courses = search_courses(test_courses, 'Python')
        print(f"Python courses found: {len(python_courses)}")
        
        # Test combined filters
        filtered = filter_courses(
            test_courses,
            min_rating=4.0,
            max_duration=10.0,
            keywords=['programming']
        )
        print(f"Combined filter results: {len(filtered)}")
        
        print("✓ Filters test passed")
        return True
        
    except Exception as e:
        print(f"✗ Filters test failed: {e}")
        return False


def test_enroller():
    """Test the enroller module (without actual enrollment)."""
    try:
        print("\n=== Testing Enroller ===")
        
        from udemy_enroller import UdemyEnroller
        
        enroller = UdemyEnroller()
        
        # Test cookie loading (will fail if no cookies, but shouldn't crash)
        try:
            cookies_loaded = enroller.load_cookies_from_chrome()
            print(f"Cookies loaded: {cookies_loaded}")
        except Exception as e:
            print(f"Cookie loading failed (expected): {e}")
        
        # Test URL parsing
        test_url = "https://www.udemy.com/course/python-bootcamp/?couponCode=FREE123"
        course_info = enroller._extract_course_info(test_url)
        
        if course_info:
            print(f"Course info extracted: {course_info}")
            print("✓ Enroller test passed")
            return True
        else:
            print("✗ Failed to extract course info")
            return False
        
    except Exception as e:
        print(f"✗ Enroller test failed: {e}")
        return False


def test_scheduler():
    """Test the scheduler module."""
    try:
        print("\n=== Testing Scheduler ===")
        
        from scheduler import UdemyScheduler
        
        scheduler = UdemyScheduler()
        
        # Test notification
        print("Testing notification...")
        scheduler.test_notification()
        
        # Test job scheduling
        scheduler.schedule_daily_at("10:00")
        jobs = scheduler.get_scheduled_jobs()
        print(f"Scheduled jobs: {len(jobs)}")
        
        print("✓ Scheduler test passed")
        return True
        
    except Exception as e:
        print(f"✗ Scheduler test failed: {e}")
        return False


def test_gui_imports():
    """Test GUI module imports."""
    try:
        print("\n=== Testing GUI Imports ===")
        
        # Test customtkinter import
        try:
            import customtkinter
            print("✓ customtkinter imported successfully")
        except ImportError as e:
            print(f"✗ customtkinter import failed: {e}")
            return False
        
        # Test login window import
        try:
            from login_window import LoginWindow
            print("✓ LoginWindow imported successfully")
        except ImportError as e:
            print(f"✗ LoginWindow import failed: {e}")
            return False
        
        # Test main GUI import
        try:
            from main_gui import MainGUI
            print("✓ MainGUI imported successfully")
        except ImportError as e:
            print(f"✗ MainGUI import failed: {e}")
            return False
        
        print("✓ GUI imports test passed")
        return True
        
    except Exception as e:
        print(f"✗ GUI imports test failed: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("Starting Udemy Course Enroller Module Tests")
    print("=" * 50)
    
    tests = [
        test_coupon_scraper,
        test_filters,
        test_enroller,
        test_scheduler,
        test_gui_imports
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed. Check the output above.")
        return False


def main():
    """Main test function."""
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
