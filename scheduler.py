#!/usr/bin/env python3
"""
Scheduler Module

This module provides scheduled task functionality for the Udemy Course Enroller.
It can automatically fetch and enroll in courses at specified times.
"""

import logging
import threading
import time
from datetime import datetime
from typing import Callable, Optional

import schedule
from plyer import notification

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UdemyScheduler:
    """
    Scheduler for automated Udemy course enrollment.
    
    This class handles:
    - Scheduling daily course fetching and enrollment
    - Sending desktop notifications
    - Logging scheduled events
    - Running tasks in background threads
    """
    
    def __init__(self, session=None, user_info=None):
        """
        Initialize the scheduler.
        
        Args:
            session: Authenticated requests session
            user_info: User information from login
        """
        self.session = session
        self.user_info = user_info
        self.is_running = False
        self.scheduler_thread = None
        
        # Setup logging to file
        self._setup_file_logging()
    
    def _setup_file_logging(self):
        """Setup file logging for scheduled events."""
        today = datetime.now().strftime('%Y-%m-%d')
        log_filename = f"udemy_scheduler_{today}.log"
        
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.info(f"Scheduler logging to: {log_filename}")
    
    def fetch_and_enroll(self):
        """
        Main function to fetch courses and enroll in them.
        This function is called by the scheduler.
        """
        try:
            logger.info("Starting scheduled fetch and enroll process")
            
            # Send notification that process is starting
            self._send_notification(
                "Udemy Enroller",
                "Starting scheduled course fetching and enrollment",
                timeout=5
            )
            
            # Fetch courses
            logger.info("Fetching courses from all sources")
            courses = self._fetch_courses()
            
            if not courses:
                logger.warning("No courses found")
                self._send_notification(
                    "Udemy Enroller",
                    "No courses found during scheduled fetch",
                    timeout=10
                )
                return
            
            logger.info(f"Found {len(courses)} courses")
            
            # Apply basic filters to reduce enrollment count
            filtered_courses = self._apply_default_filters(courses)
            logger.info(f"Filtered to {len(filtered_courses)} courses")
            
            if not filtered_courses:
                logger.info("No courses passed filters")
                self._send_notification(
                    "Udemy Enroller",
                    "No courses passed filters during scheduled enrollment",
                    timeout=10
                )
                return
            
            # Enroll in filtered courses
            logger.info("Starting enrollment process")
            results = self._enroll_in_courses(filtered_courses)
            
            # Process results
            successful = sum(1 for r in results.values() if r.get('success', False))
            total = len(results)
            
            # Log results
            logger.info(f"Enrollment complete: {successful}/{total} successful")
            
            # Send notification with results
            self._send_notification(
                "Udemy Enroller - Complete",
                f"Enrolled in {successful}/{total} courses",
                timeout=10
            )
            
            # Log individual results
            for url, result in results.items():
                if result.get('success', False):
                    logger.info(f"✓ SUCCESS: {result.get('message', 'Enrolled successfully')}")
                else:
                    logger.warning(f"✗ FAILED: {result.get('message', 'Enrollment failed')}")
            
        except Exception as e:
            error_msg = f"Error in scheduled fetch and enroll: {str(e)}"
            logger.error(error_msg)
            
            # Send error notification
            self._send_notification(
                "Udemy Enroller - Error",
                f"Scheduled task failed: {str(e)}",
                timeout=15
            )
    
    def _fetch_courses(self):
        """Fetch courses from all sources."""
        try:
            from udemy_coupon_scraper import UdemyCouponScraper
            
            scraper = UdemyCouponScraper()
            courses = scraper.get_all_courses()
            
            return courses
            
        except Exception as e:
            logger.error(f"Error fetching courses: {e}")
            return []
    
    def _apply_default_filters(self, courses):
        """Apply default filters to reduce the number of courses."""
        try:
            from filters import filter_courses
            
            # Apply reasonable defaults to avoid enrolling in too many courses
            filtered = filter_courses(
                courses,
                min_rating=4.0,  # Only high-rated courses
                max_duration=10.0,  # Maximum 10 hours
                keywords=['python', 'javascript', 'programming', 'development', 'web'],  # Programming focus
                exclude_keywords=['beginner', 'basic', 'intro']  # Exclude beginner courses
            )
            
            # Limit to maximum 10 courses per day
            return filtered[:10]
            
        except Exception as e:
            logger.error(f"Error applying filters: {e}")
            return courses[:5]  # Fallback to first 5 courses
    
    def _enroll_in_courses(self, courses):
        """Enroll in the given courses."""
        try:
            from udemy_enroller import UdemyEnroller
            
            enroller = UdemyEnroller()
            enroller.session = self.session
            enroller.user_info = self.user_info
            
            # Extract course URLs
            course_urls = [course.get('url') for course in courses if course.get('url')]
            
            if not course_urls:
                logger.warning("No valid course URLs found")
                return {}
            
            # Enroll in courses
            results = enroller.enroll_in_multiple_courses(course_urls)
            
            return results
            
        except Exception as e:
            logger.error(f"Error enrolling in courses: {e}")
            return {}
    
    def _send_notification(self, title: str, message: str, timeout: int = 10):
        """
        Send desktop notification.
        
        Args:
            title: Notification title
            message: Notification message
            timeout: Notification timeout in seconds
        """
        try:
            notification.notify(
                title=title,
                message=message,
                timeout=timeout,
                app_name="Udemy Course Enroller"
            )
            logger.info(f"Sent notification: {title} - {message}")
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
    
    def schedule_daily_at(self, time_str: str = "09:00"):
        """
        Schedule daily fetch and enroll at specified time.
        
        Args:
            time_str: Time in HH:MM format (24-hour)
        """
        try:
            schedule.every().day.at(time_str).do(self.fetch_and_enroll)
            logger.info(f"Scheduled daily fetch and enroll at {time_str}")
            
        except Exception as e:
            logger.error(f"Error scheduling daily task: {e}")
    
    def schedule_weekly_at(self, day: str, time_str: str = "09:00"):
        """
        Schedule weekly fetch and enroll at specified day and time.
        
        Args:
            day: Day of the week (e.g., 'monday', 'tuesday')
            time_str: Time in HH:MM format (24-hour)
        """
        try:
            day_method = getattr(schedule.every(), day.lower())
            day_method.at(time_str).do(self.fetch_and_enroll)
            logger.info(f"Scheduled weekly fetch and enroll on {day} at {time_str}")
            
        except Exception as e:
            logger.error(f"Error scheduling weekly task: {e}")
    
    def add_custom_schedule(self, schedule_func: Callable):
        """
        Add a custom schedule function.
        
        Args:
            schedule_func: Function that sets up the schedule
        """
        try:
            schedule_func()
            logger.info("Added custom schedule")
            
        except Exception as e:
            logger.error(f"Error adding custom schedule: {e}")
    
    def start_scheduler(self):
        """Start the scheduler in a background thread."""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
        
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("Scheduler started in background thread")
        
        # Send startup notification
        self._send_notification(
            "Udemy Enroller",
            "Scheduler started successfully",
            timeout=5
        )
    
    def stop_scheduler(self):
        """Stop the scheduler."""
        if not self.is_running:
            logger.warning("Scheduler is not running")
            return
        
        self.is_running = False
        schedule.clear()
        
        logger.info("Scheduler stopped")
        
        # Send shutdown notification
        self._send_notification(
            "Udemy Enroller",
            "Scheduler stopped",
            timeout=5
        )
    
    def _run_scheduler(self):
        """Main scheduler loop running in background thread."""
        logger.info("Scheduler loop started")
        
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying
    
    def get_scheduled_jobs(self):
        """Get list of scheduled jobs."""
        return schedule.jobs
    
    def run_now(self):
        """Run the fetch and enroll process immediately."""
        logger.info("Running fetch and enroll process immediately")
        
        # Run in separate thread to avoid blocking
        thread = threading.Thread(target=self.fetch_and_enroll, daemon=True)
        thread.start()
    
    def test_notification(self):
        """Test desktop notification functionality."""
        self._send_notification(
            "Udemy Enroller - Test",
            "This is a test notification",
            timeout=5
        )


def start_scheduler(session=None, user_info=None, schedule_time: str = "09:00"):
    """
    Convenience function to start the scheduler with default settings.
    
    Args:
        session: Authenticated requests session
        user_info: User information from login
        schedule_time: Time to run daily (HH:MM format)
        
    Returns:
        UdemyScheduler: The scheduler instance
    """
    scheduler = UdemyScheduler(session, user_info)
    scheduler.schedule_daily_at(schedule_time)
    scheduler.start_scheduler()
    
    return scheduler


def main():
    """
    Example usage of the scheduler.
    """
    # Create scheduler
    scheduler = UdemyScheduler()
    
    # Schedule daily at 9:00 AM
    scheduler.schedule_daily_at("09:00")
    
    # Test notification
    scheduler.test_notification()
    
    # Start scheduler
    scheduler.start_scheduler()
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down scheduler")
        scheduler.stop_scheduler()


if __name__ == "__main__":
    main()
