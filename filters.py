#!/usr/bin/env python3
"""
Course Filtering Module

This module provides functionality to filter Udemy courses based on various criteria
such as rating, duration, language, and keywords.
"""

import logging
import re
from typing import Dict, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def filter_courses(
    courses: List[Dict],
    min_rating: float = 0.0,
    max_duration: Optional[float] = None,
    language: Optional[str] = None,
    keywords: Optional[Union[str, List[str]]] = None,
    exclude_keywords: Optional[Union[str, List[str]]] = None,
    min_students: Optional[int] = None,
    max_students: Optional[int] = None,
    categories: Optional[Union[str, List[str]]] = None,
    exclude_categories: Optional[Union[str, List[str]]] = None,
    instructors: Optional[Union[str, List[str]]] = None,
    exclude_instructors: Optional[Union[str, List[str]]] = None,
    case_sensitive: bool = False
) -> List[Dict]:
    """
    Filter courses based on multiple criteria.
    
    Args:
        courses (List[Dict]): List of course dictionaries
        min_rating (float): Minimum course rating (0.0 to 5.0)
        max_duration (float, optional): Maximum duration in hours
        language (str, optional): Course language filter
        keywords (str|List[str], optional): Keywords to search for in title/description
        exclude_keywords (str|List[str], optional): Keywords to exclude from results
        min_students (int, optional): Minimum number of students
        max_students (int, optional): Maximum number of students
        categories (str|List[str], optional): Categories to include
        exclude_categories (str|List[str], optional): Categories to exclude
        instructors (str|List[str], optional): Instructors to include
        exclude_instructors (str|List[str], optional): Instructors to exclude
        case_sensitive (bool): Whether text matching should be case sensitive
        
    Returns:
        List[Dict]: Filtered list of courses
    """
    if not courses:
        return []
    
    logger.info(f"Filtering {len(courses)} courses with criteria:")
    logger.info(f"  Min rating: {min_rating}")
    logger.info(f"  Max duration: {max_duration}")
    logger.info(f"  Language: {language}")
    logger.info(f"  Keywords: {keywords}")
    logger.info(f"  Exclude keywords: {exclude_keywords}")
    
    filtered_courses = []
    
    # Convert string inputs to lists for easier processing
    keywords = _ensure_list(keywords)
    exclude_keywords = _ensure_list(exclude_keywords)
    categories = _ensure_list(categories)
    exclude_categories = _ensure_list(exclude_categories)
    instructors = _ensure_list(instructors)
    exclude_instructors = _ensure_list(exclude_instructors)
    
    for course in courses:
        # Skip if course doesn't have required fields
        if not isinstance(course, dict) or 'title' not in course:
            continue
        
        # Apply filters
        if not _passes_rating_filter(course, min_rating):
            continue
        
        if not _passes_duration_filter(course, max_duration):
            continue
        
        if not _passes_language_filter(course, language, case_sensitive):
            continue
        
        if not _passes_keyword_filter(course, keywords, exclude_keywords, case_sensitive):
            continue
        
        if not _passes_student_filter(course, min_students, max_students):
            continue
        
        if not _passes_category_filter(course, categories, exclude_categories, case_sensitive):
            continue
        
        if not _passes_instructor_filter(course, instructors, exclude_instructors, case_sensitive):
            continue
        
        filtered_courses.append(course)
    
    logger.info(f"Filtered results: {len(filtered_courses)} courses")
    return filtered_courses


def filter_by_rating(courses: List[Dict], min_rating: float) -> List[Dict]:
    """
    Filter courses by minimum rating.
    
    Args:
        courses (List[Dict]): List of course dictionaries
        min_rating (float): Minimum rating (0.0 to 5.0)
        
    Returns:
        List[Dict]: Filtered courses
    """
    return [course for course in courses if _passes_rating_filter(course, min_rating)]


def filter_by_duration(courses: List[Dict], max_duration: float) -> List[Dict]:
    """
    Filter courses by maximum duration.
    
    Args:
        courses (List[Dict]): List of course dictionaries
        max_duration (float): Maximum duration in hours
        
    Returns:
        List[Dict]: Filtered courses
    """
    return [course for course in courses if _passes_duration_filter(course, max_duration)]


def filter_by_language(courses: List[Dict], language: str, case_sensitive: bool = False) -> List[Dict]:
    """
    Filter courses by language.
    
    Args:
        courses (List[Dict]): List of course dictionaries
        language (str): Language to filter by
        case_sensitive (bool): Whether matching should be case sensitive
        
    Returns:
        List[Dict]: Filtered courses
    """
    return [course for course in courses if _passes_language_filter(course, language, case_sensitive)]


def filter_by_keywords(courses: List[Dict], keywords: Union[str, List[str]], case_sensitive: bool = False) -> List[Dict]:
    """
    Filter courses by keywords in title or description.
    
    Args:
        courses (List[Dict]): List of course dictionaries
        keywords (str|List[str]): Keywords to search for
        case_sensitive (bool): Whether matching should be case sensitive
        
    Returns:
        List[Dict]: Filtered courses
    """
    keywords = _ensure_list(keywords)
    return [course for course in courses if _passes_keyword_filter(course, keywords, [], case_sensitive)]


def search_courses(courses: List[Dict], query: str, case_sensitive: bool = False) -> List[Dict]:
    """
    Search courses by a query string in title, description, or instructor.
    
    Args:
        courses (List[Dict]): List of course dictionaries
        query (str): Search query
        case_sensitive (bool): Whether matching should be case sensitive
        
    Returns:
        List[Dict]: Matching courses
    """
    if not query:
        return courses
    
    search_terms = query.split()
    results = []
    
    for course in courses:
        # Search in title
        title = course.get('title', '')
        
        # Search in description if available
        description = course.get('description', '')
        
        # Search in instructor if available
        instructor = course.get('instructor', '')
        
        # Search in category if available
        category = course.get('category', '')
        
        # Combine all searchable text
        searchable_text = f"{title} {description} {instructor} {category}"
        
        if not case_sensitive:
            searchable_text = searchable_text.lower()
            search_terms = [term.lower() for term in search_terms]
        
        # Check if all search terms are present
        if all(term in searchable_text for term in search_terms):
            results.append(course)
    
    return results


def sort_courses(courses: List[Dict], sort_by: str = 'rating', reverse: bool = True) -> List[Dict]:
    """
    Sort courses by specified criteria.
    
    Args:
        courses (List[Dict]): List of course dictionaries
        sort_by (str): Sort criteria ('rating', 'duration', 'students', 'title')
        reverse (bool): Whether to sort in descending order
        
    Returns:
        List[Dict]: Sorted courses
    """
    if not courses:
        return courses
    
    def get_sort_key(course):
        if sort_by == 'rating':
            return _get_numeric_value(course, 'rating', 0.0)
        elif sort_by == 'duration':
            return _get_numeric_value(course, 'duration', 0.0)
        elif sort_by == 'students':
            return _get_numeric_value(course, 'students', 0)
        elif sort_by == 'title':
            return course.get('title', '').lower()
        else:
            return 0
    
    try:
        return sorted(courses, key=get_sort_key, reverse=reverse)
    except Exception as e:
        logger.error(f"Error sorting courses: {e}")
        return courses


def get_unique_values(courses: List[Dict], field: str) -> List[str]:
    """
    Get unique values for a specific field across all courses.
    
    Args:
        courses (List[Dict]): List of course dictionaries
        field (str): Field name to extract values from
        
    Returns:
        List[str]: List of unique values
    """
    unique_values = set()
    
    for course in courses:
        value = course.get(field)
        if value:
            if isinstance(value, list):
                unique_values.update(value)
            else:
                unique_values.add(str(value))
    
    return sorted(list(unique_values))


def get_filter_statistics(courses: List[Dict]) -> Dict:
    """
    Get statistics about filterable fields in the course list.
    
    Args:
        courses (List[Dict]): List of course dictionaries
        
    Returns:
        Dict: Statistics about the courses
    """
    if not courses:
        return {}
    
    stats = {
        'total_courses': len(courses),
        'languages': get_unique_values(courses, 'language'),
        'categories': get_unique_values(courses, 'category'),
        'instructors': get_unique_values(courses, 'instructor'),
        'rating_range': {
            'min': min(_get_numeric_value(c, 'rating', 0.0) for c in courses),
            'max': max(_get_numeric_value(c, 'rating', 0.0) for c in courses)
        },
        'duration_range': {
            'min': min(_get_numeric_value(c, 'duration', 0.0) for c in courses),
            'max': max(_get_numeric_value(c, 'duration', 0.0) for c in courses)
        }
    }
    
    return stats


# Helper functions

def _ensure_list(value: Union[str, List[str], None]) -> List[str]:
    """Convert string or None to list."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return value


def _get_numeric_value(course: Dict, field: str, default: Union[int, float]) -> Union[int, float]:
    """Extract numeric value from course dictionary."""
    value = course.get(field, default)
    
    if isinstance(value, (int, float)):
        return value
    
    if isinstance(value, str):
        # Try to extract number from string
        try:
            # Handle ratings like "4.5" or "4.5 stars"
            if field == 'rating':
                rating_match = re.search(r'(\d+\.?\d*)', value)
                if rating_match:
                    return float(rating_match.group(1))
            
            # Handle duration like "5.5 hours" or "2h 30m"
            elif field == 'duration':
                # Pattern for "X hours" or "X.Y hours"
                hours_match = re.search(r'(\d+\.?\d*)\s*(?:hours?|hrs?|h)', value, re.IGNORECASE)
                if hours_match:
                    return float(hours_match.group(1))
                
                # Pattern for "Xh Ym" format
                time_match = re.search(r'(\d+)h\s*(\d+)m', value, re.IGNORECASE)
                if time_match:
                    hours = int(time_match.group(1))
                    minutes = int(time_match.group(2))
                    return hours + minutes / 60.0
            
            # Handle student count like "1,234 students"
            elif field == 'students':
                students_match = re.search(r'([\d,]+)', value)
                if students_match:
                    return int(students_match.group(1).replace(',', ''))
            
            # Generic number extraction
            return float(value)
            
        except (ValueError, AttributeError):
            return default
    
    return default


def _passes_rating_filter(course: Dict, min_rating: float) -> bool:
    """Check if course passes rating filter."""
    if min_rating <= 0:
        return True
    
    rating = _get_numeric_value(course, 'rating', 0.0)
    return rating >= min_rating


def _passes_duration_filter(course: Dict, max_duration: Optional[float]) -> bool:
    """Check if course passes duration filter."""
    if max_duration is None:
        return True
    
    duration = _get_numeric_value(course, 'duration', 0.0)
    return duration <= max_duration


def _passes_language_filter(course: Dict, language: Optional[str], case_sensitive: bool) -> bool:
    """Check if course passes language filter."""
    if not language:
        return True
    
    course_language = course.get('language', '')
    
    if not case_sensitive:
        course_language = course_language.lower()
        language = language.lower()
    
    return language in course_language


def _passes_keyword_filter(course: Dict, keywords: List[str], exclude_keywords: List[str], case_sensitive: bool) -> bool:
    """Check if course passes keyword filter."""
    # Get searchable text
    title = course.get('title', '')
    description = course.get('description', '')
    searchable_text = f"{title} {description}"
    
    if not case_sensitive:
        searchable_text = searchable_text.lower()
        keywords = [kw.lower() for kw in keywords]
        exclude_keywords = [kw.lower() for kw in exclude_keywords]
    
    # Check include keywords
    if keywords:
        if not any(keyword in searchable_text for keyword in keywords):
            return False
    
    # Check exclude keywords
    if exclude_keywords:
        if any(keyword in searchable_text for keyword in exclude_keywords):
            return False
    
    return True


def _passes_student_filter(course: Dict, min_students: Optional[int], max_students: Optional[int]) -> bool:
    """Check if course passes student count filter."""
    students = _get_numeric_value(course, 'students', 0)
    
    if min_students is not None and students < min_students:
        return False
    
    if max_students is not None and students > max_students:
        return False
    
    return True


def _passes_category_filter(course: Dict, categories: List[str], exclude_categories: List[str], case_sensitive: bool) -> bool:
    """Check if course passes category filter."""
    course_category = course.get('category', '')
    
    if not case_sensitive:
        course_category = course_category.lower()
        categories = [cat.lower() for cat in categories]
        exclude_categories = [cat.lower() for cat in exclude_categories]
    
    # Check include categories
    if categories:
        if not any(category in course_category for category in categories):
            return False
    
    # Check exclude categories
    if exclude_categories:
        if any(category in course_category for category in exclude_categories):
            return False
    
    return True


def _passes_instructor_filter(course: Dict, instructors: List[str], exclude_instructors: List[str], case_sensitive: bool) -> bool:
    """Check if course passes instructor filter."""
    course_instructor = course.get('instructor', '')
    
    if not case_sensitive:
        course_instructor = course_instructor.lower()
        instructors = [inst.lower() for inst in instructors]
        exclude_instructors = [inst.lower() for inst in exclude_instructors]
    
    # Check include instructors
    if instructors:
        if not any(instructor in course_instructor for instructor in instructors):
            return False
    
    # Check exclude instructors
    if exclude_instructors:
        if any(instructor in course_instructor for instructor in exclude_instructors):
            return False
    
    return True


def main():
    """
    Example usage of the filtering functions.
    """
    # Example courses data
    example_courses = [
        {
            'title': 'Python Programming Bootcamp',
            'rating': 4.5,
            'duration': 8.5,
            'language': 'English',
            'category': 'Programming',
            'instructor': 'John Doe',
            'students': 1500,
            'url': 'https://example.com/course1'
        },
        {
            'title': 'JavaScript Fundamentals',
            'rating': 4.2,
            'duration': 5.0,
            'language': 'English',
            'category': 'Programming',
            'instructor': 'Jane Smith',
            'students': 800,
            'url': 'https://example.com/course2'
        },
        {
            'title': 'Data Science with R',
            'rating': 3.8,
            'duration': 12.0,
            'language': 'English',
            'category': 'Data Science',
            'instructor': 'Bob Johnson',
            'students': 600,
            'url': 'https://example.com/course3'
        }
    ]
    
    # Test filtering
    print("Original courses:", len(example_courses))
    
    # Filter by rating
    high_rated = filter_by_rating(example_courses, 4.0)
    print("High rated courses (>=4.0):", len(high_rated))
    
    # Filter by duration
    short_courses = filter_by_duration(example_courses, 6.0)
    print("Short courses (<=6h):", len(short_courses))
    
    # Filter by keywords
    python_courses = filter_by_keywords(example_courses, ['Python', 'programming'])
    print("Python courses:", len(python_courses))
    
    # Combined filters
    filtered = filter_courses(
        example_courses,
        min_rating=4.0,
        max_duration=10.0,
        keywords=['programming']
    )
    print("Combined filter results:", len(filtered))
    
    # Get statistics
    stats = get_filter_statistics(example_courses)
    print("Course statistics:", stats)


if __name__ == "__main__":
    main()
