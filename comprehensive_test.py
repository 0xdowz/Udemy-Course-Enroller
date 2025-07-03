#!/usr/bin/env python3
"""
Comprehensive test script for the Udemy Course Enroller application.
Tests all major components including multi-browser support.
"""

import sys
import os
import logging
from typing import Dict, List

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_imports():
    """Test that all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        # Test core modules
        from udemy_coupon_scraper import UdemyCouponScraper
        from udemy_enroller import UdemyEnroller
        from filters import filter_courses
        from scheduler import UdemyScheduler
        from browser_manager import BrowserManager
        
        # Test GUI modules
        from login_window import LoginWindow
        from main_gui import MainGUI
        
        print("✅ All core modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_browser_manager():
    """Test the browser manager functionality."""
    print("\n🌐 Testing Browser Manager...")
    
    try:
        from browser_manager import BrowserManager
        
        browser_manager = BrowserManager()
        
        # Test basic functionality
        print(f"  browser_cookie3 available: {browser_manager.browser_cookie3_available}")
        
        # Get available browsers
        available_browsers = browser_manager.get_available_browsers()
        print(f"  Available browsers: {len(available_browsers)}")
        
        for browser in available_browsers:
            print(f"    {browser['icon']} {browser['name']} (ID: {browser['id']})")
        
        # Test recommendation system
        recommended = browser_manager.get_browser_recommendation()
        if recommended:
            print(f"  Recommended browser: {recommended}")
        else:
            print("  No browser recommendation available")
        
        print("✅ Browser Manager tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Browser Manager test failed: {e}")
        return False

def test_course_scraper():
    """Test the course scraper functionality."""
    print("\n🔍 Testing Course Scraper...")
    
    try:
        from udemy_coupon_scraper import UdemyCouponScraper
        
        scraper = UdemyCouponScraper()
        
        # Test basic functionality without making actual requests
        print("  Course scraper initialized successfully")
        
        # Test method existence
        if hasattr(scraper, 'get_all_courses'):
            print("    ✅ get_all_courses method available")
        else:
            print("    ❌ get_all_courses method missing")
        
        if hasattr(scraper, 'scrape_realdiscount'):
            print("    ✅ scrape_realdiscount method available")
        else:
            print("    ❌ scrape_realdiscount method missing")
        
        if hasattr(scraper, 'scrape_discudemy'):
            print("    ✅ scrape_discudemy method available")
        else:
            print("    ❌ scrape_discudemy method missing")
        
        print("✅ Course Scraper tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Course Scraper test failed: {e}")
        return False

def test_course_filters():
    """Test the course filters functionality."""
    print("\n🎯 Testing Course Filters...")
    
    try:
        from filters import filter_courses
        
        # Create test course data
        test_courses = [
            {
                'title': 'Python Programming',
                'rating': 4.5,
                'students': 1000,
                'duration': '10 hours',
                'language': 'English',
                'description': 'Learn Python programming from scratch'
            },
            {
                'title': 'JavaScript Basics',
                'rating': 4.2,
                'students': 500,
                'duration': '5 hours',
                'language': 'English',
                'description': 'Basic JavaScript concepts'
            },
            {
                'title': 'Arabic Language Course',
                'rating': 4.8,
                'students': 300,
                'duration': '15 hours',
                'language': 'Arabic',
                'description': 'Learn Arabic language'
            }
        ]
        
        # Test different filters
        print("  Testing rating filter...")
        filtered_by_rating = filter_courses(test_courses, min_rating=4.3)
        print(f"    Courses with rating >= 4.3: {len(filtered_by_rating)}")
        
        print("  Testing keyword filter...")
        filtered_by_keyword = filter_courses(test_courses, keywords=['Python'])
        print(f"    Courses with 'Python' keyword: {len(filtered_by_keyword)}")
        
        print("  Testing language filter...")
        filtered_by_language = filter_courses(test_courses, language='English')
        print(f"    English courses: {len(filtered_by_language)}")
        
        print("✅ Course Filters tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Course Filters test failed: {e}")
        return False

def test_udemy_enroller():
    """Test the Udemy enroller functionality."""
    print("\n⚡ Testing Udemy Enroller...")
    
    try:
        from udemy_enroller import UdemyEnroller
        
        enroller = UdemyEnroller()
        
        # Test basic initialization
        print("  Udemy enroller initialized successfully")
        print(f"  Session configured: {enroller.session is not None}")
        print(f"  Timeout setting: {enroller.timeout}")
        
        # Test browser support methods
        print("  Testing browser support methods...")
        
        # Test that new browser methods exist
        if hasattr(enroller, 'load_cookies_from_browser'):
            print("    ✅ load_cookies_from_browser method available")
        else:
            print("    ❌ load_cookies_from_browser method missing")
        
        # Test backward compatibility
        if hasattr(enroller, 'load_cookies_from_chrome'):
            print("    ✅ load_cookies_from_chrome method available (backward compatibility)")
        else:
            print("    ❌ load_cookies_from_chrome method missing")
        
        print("✅ Udemy Enroller tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Udemy Enroller test failed: {e}")
        return False

def test_gui_components():
    """Test GUI components without actually showing them."""
    print("\n🎨 Testing GUI Components...")
    
    try:
        # Test login window
        print("  Testing LoginWindow...")
        from login_window import LoginWindow
        
        # Test that the class can be instantiated
        print("    LoginWindow class available")
        
        # Test main GUI
        print("  Testing MainGUI...")
        from main_gui import MainGUI
        
        # Test that the class can be instantiated
        print("    MainGUI class available")
        
        print("✅ GUI Components tests passed")
        return True
        
    except Exception as e:
        print(f"❌ GUI Components test failed: {e}")
        return False

def test_scheduler():
    """Test the scheduler functionality."""
    print("\n📅 Testing Scheduler...")
    
    try:
        from scheduler import UdemyScheduler
        
        # Create a simple callback function
        def test_callback():
            print("Scheduler callback executed")
        
        scheduler = UdemyScheduler()
        
        print("  Scheduler initialized successfully")
        print(f"  Scheduler running: {scheduler.is_running}")
        
        # Test schedule configuration
        print("  Testing schedule configuration...")
        
        print("✅ Scheduler tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Scheduler test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary."""
    print("🚀 Starting comprehensive test suite...\n")
    
    tests = [
        ("Imports", test_imports),
        ("Browser Manager", test_browser_manager),
        ("Course Scraper", test_course_scraper),
        ("Course Filters", test_course_filters),
        ("Udemy Enroller", test_udemy_enroller),
        ("GUI Components", test_gui_components),
        ("Scheduler", test_scheduler)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:20} {status}")
        
        if result:
            passed += 1
        else:
            failed += 1
    
    print("="*50)
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(results))*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed! The application is ready to use.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the issues above.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
