#!/usr/bin/env python3
"""
Example usage of the Udemy Coupon Scraper module.

This script demonstrates how to use the UdemyCouponScraper class
to fetch coupon-based Udemy courses from multiple sources.
"""

from udemy_coupon_scraper import UdemyCouponScraper
import json


def save_courses_to_json(courses, filename="udemy_courses.json"):
    """
    Save courses to a JSON file.
    
    Args:
        courses (List[Dict]): List of course dictionaries
        filename (str): Output filename
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(courses, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved {len(courses)} courses to {filename}")


def filter_courses_by_keyword(courses, keyword):
    """
    Filter courses by a keyword in the title.
    
    Args:
        courses (List[Dict]): List of course dictionaries
        keyword (str): Keyword to search for
        
    Returns:
        List[Dict]: Filtered courses
    """
    filtered = [
        course for course in courses 
        if keyword.lower() in course['title'].lower()
    ]
    return filtered


def main():
    """
    Main function demonstrating various usage scenarios.
    """
    print("🚀 Udemy Coupon Scraper - Example Usage")
    print("=" * 50)
    
    # Initialize the scraper
    scraper = UdemyCouponScraper()
    
    # Example 1: Get all courses
    print("\n1. Getting all courses...")
    all_courses = scraper.get_all_courses()
    
    # Example 2: Filter courses by keyword
    print("\n2. Filtering courses by keyword 'Python'...")
    python_courses = filter_courses_by_keyword(all_courses, 'Python')
    
    print(f"Found {len(python_courses)} Python courses:")
    for i, course in enumerate(python_courses[:5], 1):
        print(f"   {i}. {course['title']}")
        print(f"      Source: {course['source']}")
        print(f"      URL: {course['url'][:80]}...")
    
    # Example 3: Get courses from specific source
    print("\n3. Getting courses from Real Discount only...")
    real_discount_courses = scraper.scrape_real_discount()
    print(f"Found {len(real_discount_courses)} courses from Real Discount")
    
    print("\n4. Getting courses from Discudemy only...")
    discudemy_courses = scraper.scrape_discudemy()
    print(f"Found {len(discudemy_courses)} courses from Discudemy")
    
    # Example 4: Save courses to JSON
    print("\n5. Saving courses to JSON file...")
    save_courses_to_json(all_courses)
    
    # Example 5: Statistics
    print("\n6. Course statistics:")
    print(f"   Total courses: {len(all_courses)}")
    
    sources = {}
    for course in all_courses:
        source = course['source']
        sources[source] = sources.get(source, 0) + 1
    
    for source, count in sources.items():
        print(f"   {source}: {count} courses")
    
    print("\n✅ Example completed successfully!")


if __name__ == "__main__":
    main()
