#!/usr/bin/env python3
"""
Main Entry Point for Udemy Course Enroller

This is the main entry point that orchestrates the entire application:
- Shows login window first
- Launches main GUI after successful login
- Starts the scheduler in the background
- Handles exceptions and provides user-friendly messages
"""

import logging
import sys
import tkinter.messagebox as messagebox
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('udemy_enroller.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class UdemyEnrollerApp:
    """
    Main application class that coordinates all components.
    """
    
    def __init__(self):
        """Initialize the application."""
        self.session = None
        self.user_info = None
        self.scheduler = None
        self.main_gui = None
        
        logger.info("Initializing Udemy Course Enroller")
    
    def run(self):
        """Run the main application."""
        try:
            logger.info("Starting Udemy Course Enroller application")
            
            # Step 1: Show login window
            if not self._show_login():
                logger.info("User cancelled login - exiting application")
                return
            
            # Step 2: Start scheduler in background
            self._start_scheduler()
            
            # Step 3: Show main GUI
            self._show_main_gui()
            
        except Exception as e:
            error_msg = f"Critical error in main application: {str(e)}"
            logger.critical(error_msg)
            self._show_error("Critical Error", error_msg)
        
        finally:
            self._cleanup()
    
    def _show_login(self) -> bool:
        """
        Show login window and handle authentication.
        
        Returns:
            bool: True if login was successful, False otherwise
        """
        try:
            logger.info("Showing login window")
            
            from login_window import LoginWindow
            
            # Create login window with callback
            login_window = LoginWindow(on_success_callback=self._on_login_success)
            
            # Show login window and wait for result
            login_result = login_window.show()
            
            # Check if authentication was successful
            if login_result and self.session is not None and self.user_info is not None:
                logger.info("Authentication successful - proceeding to main application")
                return True
            else:
                logger.info("Authentication failed or user cancelled login")
                # Show message in Arabic that login is required
                self._show_error("تسجيل الدخول مطلوب", 
                    "يجب عليك تسجيل الدخول أولاً لاستخدام الأداة.\n"
                    "You must login first to use this application.\n\n"
                    "يرجى إدخال بريدك الإلكتروني وكلمة المرور المربوطة بحساب يودمي الخاص بك.\n"
                    "Please enter your Udemy email and password to continue.")
                return False
            
        except ImportError as e:
            error_msg = "Required GUI libraries not available. Please install customtkinter."
            logger.error(f"Import error: {e}")
            self._show_error("Missing Dependencies", error_msg)
            return False
        
        except Exception as e:
            error_msg = f"Error showing login window: {str(e)}"
            logger.error(error_msg)
            self._show_error("Login Error", error_msg)
            return False
    
    def _on_login_success(self, session, user_info):
        """
        Callback function called when login is successful.
        
        Args:
            session: Authenticated requests session
            user_info: User information dictionary
        """
        self.session = session
        self.user_info = user_info
        
        user_name = user_info.get('display_name', 'Unknown') if user_info else 'Unknown'
        logger.info(f"Login successful for user: {user_name}")
    
    def _start_scheduler(self):
        """Start the background scheduler."""
        try:
            logger.info("Starting background scheduler")
            
            from scheduler import start_scheduler
            
            # Start scheduler with default settings (9:00 AM daily)
            self.scheduler = start_scheduler(
                session=self.session,
                user_info=self.user_info,
                schedule_time="09:00"
            )
            
            logger.info("Background scheduler started successfully")
            
        except ImportError as e:
            logger.warning(f"Scheduler not available: {e}")
            # Continue without scheduler
        
        except Exception as e:
            logger.error(f"Error starting scheduler: {e}")
            # Continue without scheduler - not critical
    
    def _show_main_gui(self):
        """Show the main GUI."""
        try:
            logger.info("Showing main GUI")
            
            from main_gui import MainGUI
            
            # Create and show main GUI
            self.main_gui = MainGUI(session=self.session, user_info=self.user_info)
            self.main_gui.show()
            
        except ImportError as e:
            error_msg = "Required GUI libraries not available. Please install customtkinter."
            logger.error(f"Import error: {e}")
            self._show_error("Missing Dependencies", error_msg)
        
        except Exception as e:
            error_msg = f"Error showing main GUI: {str(e)}"
            logger.error(error_msg)
            self._show_error("GUI Error", error_msg)
    
    def _cleanup(self):
        """Clean up resources before exiting."""
        try:
            logger.info("Cleaning up application resources")
            
            # Stop scheduler if running
            if self.scheduler:
                try:
                    self.scheduler.stop_scheduler()
                    logger.info("Scheduler stopped")
                except Exception as e:
                    logger.warning(f"Error stopping scheduler: {e}")
            
            # Close session if exists
            if self.session:
                try:
                    self.session.close()
                    logger.info("Session closed")
                except Exception as e:
                    logger.warning(f"Error closing session: {e}")
            
            logger.info("Application cleanup complete")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def _show_error(self, title: str, message: str):
        """
        Show error message to user.
        
        Args:
            title: Error dialog title
            message: Error message
        """
        try:
            messagebox.showerror(title, message)
        except Exception:
            # Fallback to console if GUI is not available
            print(f"ERROR - {title}: {message}")


def check_dependencies():
    """
    Check if all required dependencies are available.
    
    Returns:
        tuple: (success: bool, missing_deps: list)
    """
    required_packages = [
        ('requests', 'requests'),
        ('beautifulsoup4', 'bs4'),
        ('browser_cookie3', 'browser_cookie3'),
        ('customtkinter', 'customtkinter'),
        ('schedule', 'schedule'),
        ('plyer', 'plyer')
    ]
    
    missing_deps = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_deps.append(package_name)
    
    return len(missing_deps) == 0, missing_deps


def show_dependency_help(missing_deps):
    """
    Show help message for installing missing dependencies.
    
    Args:
        missing_deps: List of missing package names
    """
    print("Missing required dependencies:")
    for dep in missing_deps:
        print(f"  - {dep}")
    
    print("\nTo install missing dependencies, run:")
    print(f"pip install {' '.join(missing_deps)}")
    
    print("\nAlternatively, install all dependencies with:")
    print("pip install -r requirements.txt")


def create_requirements_file():
    """Create or update requirements.txt file."""
    requirements = [
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "lxml>=4.6.0",
        "browser-cookie3>=0.20.0",
        "customtkinter>=5.2.0",
        "schedule>=1.2.0",
        "plyer>=2.1.0"
    ]
    
    try:
        with open('requirements.txt', 'w') as f:
            f.write('\n'.join(requirements))
        
        logger.info("Created/updated requirements.txt")
        return True
        
    except Exception as e:
        logger.error(f"Error creating requirements.txt: {e}")
        return False


def main():
    """Main entry point of the application."""
    try:
        # Print banner
        print("=" * 60)
        print("           Udemy Course Enroller")
        print("    Automated Course Discovery and Enrollment")
        print("=" * 60)
        print()
        
        # Check dependencies
        logger.info("Checking dependencies...")
        deps_ok, missing_deps = check_dependencies()
        
        if not deps_ok:
            logger.error("Missing required dependencies")
            show_dependency_help(missing_deps)
            
            # Try to create requirements.txt
            if create_requirements_file():
                print("\nA requirements.txt file has been created.")
            
            print("\nPlease install the missing dependencies and try again.")
            sys.exit(1)
        
        logger.info("All dependencies available")
        
        # Create and run the application
        app = UdemyEnrollerApp()
        app.run()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\nApplication interrupted by user")
    
    except Exception as e:
        logger.critical(f"Unhandled exception in main: {e}")
        print(f"\nCritical error: {e}")
        print("Check the log file 'udemy_enroller.log' for more details.")
        sys.exit(1)
    
    finally:
        logger.info("Application shutdown complete")
        print("\nThank you for using Udemy Course Enroller!")


if __name__ == "__main__":
    main()
