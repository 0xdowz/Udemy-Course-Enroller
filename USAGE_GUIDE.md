# Udemy Course Enroller - Complete Application

A comprehensive Python application that automatically discovers, filters, and enrolls in Udemy courses using coupon codes. The application features a modern GUI, automatic scheduling, and support for multiple course sources.

## 🌟 Features

### Core Functionality
- **Multi-source Course Scraping**: Fetches courses from Real Discount and Discudemy
- **Intelligent Filtering**: Filter by rating, duration, language, keywords, and more
- **Automated Enrollment**: Bulk enrollment using browser cookies or email/password
- **Scheduled Tasks**: Automatic daily course discovery and enrollment
- **Desktop Notifications**: Real-time updates on enrollment status

### User Interface
- **Modern GUI**: Clean, dark-themed interface using CustomTkinter
- **Login Options**: Browser cookie authentication or email/password login
- **Course Browser**: Searchable and filterable course list
- **Real-time Status**: Progress bars and status updates
- **Detailed Results**: Comprehensive enrollment reporting

### Advanced Features
- **Smart Filtering**: Exclude beginner courses, focus on high-rated content
- **Rate Limiting**: Respectful scraping with proper delays
- **Error Handling**: Graceful handling of network issues and API changes
- **Logging**: Comprehensive logging for debugging and monitoring
- **Background Processing**: Non-blocking operations with threading

## 📋 Requirements

### System Requirements
- Python 3.7 or higher
- Windows, macOS, or Linux
- Chrome browser (for cookie authentication)
- Active internet connection

### Python Dependencies
```
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
browser-cookie3>=0.20.0
customtkinter>=5.2.0
schedule>=1.2.0
plyer>=2.1.0
```

## 🚀 Installation

### 1. Clone or Download
```bash
git clone <repository-url>
cd udemy-course-enroller
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python main.py
```

## 📖 Usage Guide

### First Time Setup

1. **Launch the Application**
   ```bash
   python main.py
   ```

2. **Login Options**
   - **Browser Session**: Automatically use your Chrome browser's Udemy session
   - **Email/Password**: Manual login with your Udemy credentials

3. **Main Interface**
   - Click "Fetch Coupons" to discover available courses
   - Use filters to narrow down courses
   - Click "Enroll All" to enroll in filtered courses

### Course Filtering

The application provides powerful filtering options:

- **Rating Filter**: Set minimum course rating (0.0 to 5.0)
- **Duration Filter**: Set maximum course duration in hours
- **Language Filter**: Filter by course language
- **Keyword Filter**: Search for specific topics (comma-separated)

### Automated Scheduling

The application automatically schedules daily course discovery at 9:00 AM:

- Fetches new courses from all sources
- Applies intelligent filters to avoid low-quality courses
- Enrolls in up to 10 high-quality courses per day
- Sends desktop notifications with results

## 🔧 Module Overview

### Core Modules

#### `udemy_coupon_scraper.py`
- Scrapes courses from multiple sources
- Handles rate limiting and anti-detection
- Returns structured course data

#### `udemy_enroller.py`
- Manages Udemy authentication
- Handles course enrollment via API
- Supports both browser cookies and manual login

#### `filters.py`
- Provides flexible course filtering
- Supports multiple filter criteria
- Includes search and sorting functionality

#### `login_window.py`
- Modern login interface using CustomTkinter
- Supports dual authentication methods
- Handles errors gracefully

#### `main_gui.py`
- Main application interface
- Course browsing and management
- Real-time status updates

#### `scheduler.py`
- Background task scheduling
- Desktop notifications
- Automated course discovery and enrollment

#### `main.py`
- Application entry point
- Coordinates all components
- Handles dependency checking

## 🎯 Usage Examples

### Basic Usage
```python
# Run the complete application
python main.py
```

### Scraper Only
```python
from udemy_coupon_scraper import UdemyCouponScraper

scraper = UdemyCouponScraper()
courses = scraper.get_all_courses()
print(f"Found {len(courses)} courses")
```

### Filtering Courses
```python
from filters import filter_courses

filtered = filter_courses(
    courses,
    min_rating=4.0,
    max_duration=10.0,
    keywords=['python', 'javascript']
)
```

### Manual Enrollment
```python
from udemy_enroller import UdemyEnroller

enroller = UdemyEnroller()
enroller.load_cookies_from_chrome()
enroller.validate_authentication()

success, message = enroller.enroll_in_course(course_url)
```

### Custom Scheduling
```python
from scheduler import UdemyScheduler

scheduler = UdemyScheduler(session, user_info)
scheduler.schedule_daily_at("10:00")  # 10:00 AM daily
scheduler.start_scheduler()
```

## ⚙️ Configuration

### Filter Defaults
You can modify the default filters in `scheduler.py`:

```python
def _apply_default_filters(self, courses):
    filtered = filter_courses(
        courses,
        min_rating=4.0,        # Minimum rating
        max_duration=10.0,     # Maximum duration
        keywords=['python', 'javascript', 'programming'],
        exclude_keywords=['beginner', 'basic']
    )
    return filtered[:10]  # Limit to 10 courses per day
```

### Schedule Times
Modify scheduling in `main.py`:

```python
# Change from 9:00 AM to 2:00 PM
self.scheduler = start_scheduler(
    session=self.session,
    user_info=self.user_info,
    schedule_time="14:00"  # 24-hour format
)
```

## 🔍 Troubleshooting

### Common Issues

#### "No module named 'customtkinter'"
```bash
pip install customtkinter
```

#### "Failed to load cookies from Chrome"
- Make sure you're logged into Udemy in Chrome
- Close Chrome completely and try again
- Try manual email/password login instead

#### "No courses found"
- Check internet connection
- Verify the source websites are accessible
- Try running with different filters

#### "Enrollment failed"
- Verify you're logged into Udemy
- Check if the coupon is still valid
- Ensure you haven't already enrolled in the course

### Debug Mode
Enable debug logging by modifying the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

### Log Files
Check these log files for detailed information:
- `udemy_enroller.log` - Main application log
- `udemy_scheduler_YYYY-MM-DD.log` - Daily scheduler logs

## 🛡️ Legal and Ethical Considerations

### Important Notes
- This tool is for educational purposes only
- Respect the terms of service of all websites
- Use reasonable delays to avoid overloading servers
- Only enroll in courses you genuinely intend to take
- Be aware of storage limits on your Udemy account

### Rate Limiting
The application includes built-in rate limiting:
- 2-second delays between enrollment requests
- Respectful scraping with proper headers
- Automatic retry logic for failed requests

## 🤝 Contributing

Feel free to contribute by:
- Adding new course sources
- Improving the user interface
- Enhancing filter capabilities
- Optimizing performance
- Fixing bugs

## 📝 License

This project is provided as-is for educational purposes. Use responsibly and in accordance with the terms of service of the websites being accessed.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the log files for error details
3. Ensure all dependencies are properly installed
4. Verify your internet connection and browser login status

## 🔄 Updates

To update the application:
1. Download the latest version
2. Install any new dependencies: `pip install -r requirements.txt`
3. Restart the application

The application will automatically check for course source changes and adapt accordingly.
