#!/usr/bin/env python3
"""
Test script for enhanced browser manager functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from browser_manager import BrowserManager

def test_browser_manager():
    """Test the enhanced browser manager functionality."""
    print("=== Testing Enhanced Browser Manager ===\n")
    
    # Initialize browser manager
    browser_manager = BrowserManager()
    
    # Check if browser_cookie3 is available
    print(f"browser_cookie3 available: {browser_manager.browser_cookie3_available}")
    
    if not browser_manager.browser_cookie3_available:
        print("❌ browser_cookie3 not available. Please install it with: pip install browser-cookie3")
        return
    
    # Test default browser detection
    print(f"\n🌟 Default browser detection:")
    default_browser = browser_manager.default_browser
    if default_browser:
        default_info = browser_manager.get_default_browser_info()
        if default_info:
            print(f"  Detected default browser: {default_info['icon']} {default_info['name']}")
        else:
            print(f"  Default browser ID: {default_browser} (but not available)")
    else:
        print("  Could not detect default browser")
    
    # Get available browsers
    available_browsers = browser_manager.get_available_browsers()
    print(f"\n🌐 Available browsers: {len(available_browsers)}")
    
    for browser in available_browsers:
        print(f"  {browser['icon']} {browser['name']} (ID: {browser['id']})")
    
    # Get sorted browsers
    sorted_browsers = browser_manager.get_available_browsers_sorted()
    print(f"\n📊 Browsers sorted by priority: {len(sorted_browsers)}")
    
    for i, browser in enumerate(sorted_browsers, 1):
        default_marker = " 🌟 (DEFAULT)" if browser.get('is_default', False) else ""
        print(f"  {i}. {browser['icon']} {browser['name']}{default_marker}")
    
    if not available_browsers:
        print("❌ No browsers available for cookie extraction")
        return
    
    # Get recommendation
    recommended = browser_manager.get_browser_recommendation()
    print(f"\n✨ Recommended browser: {recommended}")
    
    # Test cookie loading (without actually loading)
    print("\n=== Testing Cookie Loading Support ===")
    
    # Test all supported browsers (even if not available)
    all_browsers = [
        ('chrome', 'Google Chrome'),
        ('firefox', 'Mozilla Firefox'),
        ('edge', 'Microsoft Edge'),
        ('safari', 'Safari'),
        ('brave', 'Brave Browser'),
        ('opera', 'Opera'),
        ('opera_gx', 'Opera GX')
    ]
    
    for browser_id, browser_name in all_browsers:
        browser_info = browser_manager.supported_browsers.get(browser_id)
        if browser_info:
            status = "✅ Available" if browser_info['available'] else "⚠️ Not found"
            print(f"  {browser_info['icon']} {browser_name}: {status}")
        else:
            print(f"  ❌ {browser_name}: Not supported")
    
    # Test actual cookie loading for available browsers
    print("\n=== Testing Actual Cookie Loading ===")
    for browser in available_browsers[:2]:  # Test first 2 available browsers
        browser_id = browser['id']
        print(f"\nTesting {browser['name']} ({browser_id})...")
        
        try:
            success, cookies, error = browser_manager.load_cookies_from_browser(browser_id)
            
            if success:
                print(f"✅ Successfully loaded {len(cookies)} cookies from {browser['name']}")
            else:
                print(f"⚠️ Failed to load cookies from {browser['name']}: {error}")
                
        except Exception as e:
            print(f"❌ Error testing {browser['name']}: {str(e)}")

if __name__ == "__main__":
    test_browser_manager()
