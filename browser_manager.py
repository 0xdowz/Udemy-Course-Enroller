#!/usr/bin/env python3
"""
Browser Manager Module

This module handles browser cookie extraction from multiple browsers
including Chrome, Firefox, Edge, and Safari.
"""

import logging
import os
import platform
from typing import Dict, List, Optional, Tuple

try:
    import browser_cookie3
except ImportError:
    browser_cookie3 = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BrowserManager:
    """
    Manages browser cookie extraction from various browsers.
    """
    
    def __init__(self):
        """Initialize the browser manager."""
        self.supported_browsers = {
            'chrome': {
                'name': 'Google Chrome',
                'icon': '🔵',
                'function': self._get_chrome_cookies,
                'available': self._is_chrome_available(),
                'priority': 2
            },
            'firefox': {
                'name': 'Mozilla Firefox',
                'icon': '🦊',
                'function': self._get_firefox_cookies,
                'available': self._is_firefox_available(),
                'priority': 3
            },
            'edge': {
                'name': 'Microsoft Edge',
                'icon': '🟢',
                'function': self._get_edge_cookies,
                'available': self._is_edge_available(),
                'priority': 4
            },
            'safari': {
                'name': 'Safari',
                'icon': '🔷',
                'function': self._get_safari_cookies,
                'available': self._is_safari_available(),
                'priority': 5
            },
            'brave': {
                'name': 'Brave Browser',
                'icon': '🦁',
                'function': self._get_brave_cookies,
                'available': self._is_brave_available(),
                'priority': 6
            },
            'opera': {
                'name': 'Opera',
                'icon': '🔴',
                'function': self._get_opera_cookies,
                'available': self._is_opera_available(),
                'priority': 7
            },
            'opera_gx': {
                'name': 'Opera GX',
                'icon': '🎮',
                'function': self._get_opera_gx_cookies,
                'available': self._is_opera_gx_available(),
                'priority': 8
            }
        }
        
        # Check if browser_cookie3 is available
        self.browser_cookie3_available = browser_cookie3 is not None
        
        if not self.browser_cookie3_available:
            logger.warning("browser_cookie3 not available. Browser cookie login will be disabled.")
        
        # Detect default browser
        self.default_browser = self._get_default_browser()
    
    def get_available_browsers(self) -> List[Dict]:
        """
        Get list of available browsers for cookie extraction.
        
        Returns:
            List[Dict]: List of available browser information
        """
        if not self.browser_cookie3_available:
            return []
        
        available = []
        for browser_id, browser_info in self.supported_browsers.items():
            if browser_info['available']:
                available.append({
                    'id': browser_id,
                    'name': browser_info['name'],
                    'icon': browser_info['icon']
                })
        
        return available
    
    def load_cookies_from_browser(self, browser_id: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Load cookies from specified browser.
        
        Args:
            browser_id: Browser identifier (chrome, firefox, edge, safari)
            
        Returns:
            Tuple[bool, Optional[Dict], Optional[str]]: (success, cookies_dict, error_message)
        """
        if not self.browser_cookie3_available:
            return False, None, "browser_cookie3 module not available"
        
        if browser_id not in self.supported_browsers:
            return False, None, f"Unsupported browser: {browser_id}"
        
        browser_info = self.supported_browsers[browser_id]
        
        if not browser_info['available']:
            return False, None, f"{browser_info['name']} is not available or not installed"
        
        try:
            logger.info(f"Loading cookies from {browser_info['name']}")
            return browser_info['function']()
        except Exception as e:
            error_msg = f"Error loading cookies from {browser_info['name']}: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
    
    def _get_chrome_cookies(self) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Load cookies from Chrome browser."""
        try:
            cookies = browser_cookie3.chrome(domain_name='udemy.com')
            return self._process_cookies(cookies, 'Chrome')
        except Exception as e:
            return False, None, f"Chrome cookies error: {str(e)}"
    
    def _get_firefox_cookies(self) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Load cookies from Firefox browser."""
        try:
            cookies = browser_cookie3.firefox(domain_name='udemy.com')
            return self._process_cookies(cookies, 'Firefox')
        except Exception as e:
            return False, None, f"Firefox cookies error: {str(e)}"
    
    def _get_edge_cookies(self) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Load cookies from Edge browser."""
        try:
            cookies = browser_cookie3.edge(domain_name='udemy.com')
            return self._process_cookies(cookies, 'Edge')
        except Exception as e:
            return False, None, f"Edge cookies error: {str(e)}"
    
    def _get_safari_cookies(self) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Load cookies from Safari browser."""
        try:
            cookies = browser_cookie3.safari(domain_name='udemy.com')
            return self._process_cookies(cookies, 'Safari')
        except Exception as e:
            return False, None, f"Safari cookies error: {str(e)}"
    
    def _get_brave_cookies(self) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Load cookies from Brave browser."""
        try:
            # Brave uses Chrome-based cookie format
            cookies = browser_cookie3.brave(domain_name='udemy.com')
            return self._process_cookies(cookies, 'Brave')
        except Exception as e:
            return False, None, f"Brave cookies error: {str(e)}"
    
    def _get_opera_cookies(self) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Load cookies from Opera browser."""
        try:
            cookies = browser_cookie3.opera(domain_name='udemy.com')
            return self._process_cookies(cookies, 'Opera')
        except Exception as e:
            return False, None, f"Opera cookies error: {str(e)}"
    
    def _get_opera_gx_cookies(self) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Load cookies from Opera GX browser."""
        try:
            # Opera GX uses Opera-based cookie format
            cookies = browser_cookie3.opera_gx(domain_name='udemy.com')
            return self._process_cookies(cookies, 'Opera GX')
        except Exception as e:
            return False, None, f"Opera GX cookies error: {str(e)}"
    
    def _process_cookies(self, cookies, browser_name: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Process cookies from browser.
        
        Args:
            cookies: Raw cookies from browser
            browser_name: Name of the browser
            
        Returns:
            Tuple[bool, Optional[Dict], Optional[str]]: (success, cookies_dict, error_message)
        """
        if not cookies:
            return False, None, f"No Udemy cookies found in {browser_name}"
        
        # Convert cookies to dictionary
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie.name] = cookie.value
        
        # Check for essential cookies
        essential_cookies = ['access_token', 'client_id']
        missing_cookies = [cookie for cookie in essential_cookies if cookie not in cookie_dict]
        
        if missing_cookies:
            return False, None, f"Essential cookies missing in {browser_name}: {', '.join(missing_cookies)}"
        
        logger.info(f"Successfully loaded {len(cookie_dict)} cookies from {browser_name}")
        return True, cookie_dict, None
    
    def _is_chrome_available(self) -> bool:
        """Check if Chrome is available."""
        try:
            system = platform.system()
            if system == "Windows":
                # Check common Chrome installation paths
                chrome_paths = [
                    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data"),
                    os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
                    os.path.expandvars(r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe")
                ]
                return any(os.path.exists(path) for path in chrome_paths)
            elif system == "Darwin":  # macOS
                return os.path.exists("/Applications/Google Chrome.app") or \
                       os.path.exists(os.path.expanduser("~/Library/Application Support/Google/Chrome"))
            else:  # Linux
                return os.path.exists(os.path.expanduser("~/.config/google-chrome")) or \
                       os.path.exists(os.path.expanduser("~/.config/chromium"))
        except Exception:
            return False
    
    def _is_firefox_available(self) -> bool:
        """Check if Firefox is available."""
        try:
            system = platform.system()
            if system == "Windows":
                firefox_paths = [
                    os.path.expandvars(r"%APPDATA%\Mozilla\Firefox\Profiles"),
                    os.path.expandvars(r"%PROGRAMFILES%\Mozilla Firefox\firefox.exe"),
                    os.path.expandvars(r"%PROGRAMFILES(X86)%\Mozilla Firefox\firefox.exe")
                ]
                return any(os.path.exists(path) for path in firefox_paths)
            elif system == "Darwin":  # macOS
                return os.path.exists("/Applications/Firefox.app") or \
                       os.path.exists(os.path.expanduser("~/Library/Application Support/Firefox"))
            else:  # Linux
                return os.path.exists(os.path.expanduser("~/.mozilla/firefox"))
        except Exception:
            return False
    
    def _is_edge_available(self) -> bool:
        """Check if Edge is available."""
        try:
            system = platform.system()
            if system == "Windows":
                edge_paths = [
                    os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data"),
                    os.path.expandvars(r"%PROGRAMFILES%\Microsoft\Edge\Application\msedge.exe"),
                    os.path.expandvars(r"%PROGRAMFILES(X86)%\Microsoft\Edge\Application\msedge.exe")
                ]
                return any(os.path.exists(path) for path in edge_paths)
            elif system == "Darwin":  # macOS
                return os.path.exists("/Applications/Microsoft Edge.app") or \
                       os.path.exists(os.path.expanduser("~/Library/Application Support/Microsoft Edge"))
            else:  # Linux
                return os.path.exists(os.path.expanduser("~/.config/microsoft-edge"))
        except Exception:
            return False
    
    def _is_safari_available(self) -> bool:
        """Check if Safari is available."""
        try:
            system = platform.system()
            if system == "Darwin":  # macOS only
                return os.path.exists("/Applications/Safari.app") or \
                       os.path.exists(os.path.expanduser("~/Library/Safari"))
            return False
        except Exception:
            return False
    
    def _is_brave_available(self) -> bool:
        """Check if Brave is available."""
        try:
            system = platform.system()
            if system == "Windows":
                brave_paths = [
                    os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data"),
                    os.path.expandvars(r"%PROGRAMFILES%\BraveSoftware\Brave-Browser\Application\brave.exe"),
                    os.path.expandvars(r"%PROGRAMFILES(X86)%\BraveSoftware\Brave-Browser\Application\brave.exe")
                ]
                return any(os.path.exists(path) for path in brave_paths)
            elif system == "Darwin":  # macOS
                return os.path.exists("/Applications/Brave Browser.app") or \
                       os.path.exists(os.path.expanduser("~/Library/Application Support/BraveSoftware/Brave-Browser"))
            else:  # Linux
                return os.path.exists(os.path.expanduser("~/.config/BraveSoftware/Brave-Browser"))
        except Exception:
            return False
    
    def _is_opera_available(self) -> bool:
        """Check if Opera is available."""
        try:
            system = platform.system()
            if system == "Windows":
                opera_paths = [
                    os.path.expandvars(r"%APPDATA%\Opera Software\Opera Stable"),
                    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Opera\opera.exe"),
                    os.path.expandvars(r"%PROGRAMFILES%\Opera\opera.exe")
                ]
                return any(os.path.exists(path) for path in opera_paths)
            elif system == "Darwin":  # macOS
                return os.path.exists("/Applications/Opera.app") or \
                       os.path.exists(os.path.expanduser("~/Library/Application Support/com.operasoftware.Opera"))
            else:  # Linux
                return os.path.exists(os.path.expanduser("~/.config/opera"))
        except Exception:
            return False
    
    def _is_opera_gx_available(self) -> bool:
        """Check if Opera GX is available."""
        try:
            system = platform.system()
            if system == "Windows":
                opera_gx_paths = [
                    os.path.expandvars(r"%APPDATA%\Opera Software\Opera GX Stable"),
                    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Opera GX\opera.exe"),
                    os.path.expandvars(r"%PROGRAMFILES%\Opera GX\opera.exe")
                ]
                return any(os.path.exists(path) for path in opera_gx_paths)
            elif system == "Darwin":  # macOS
                return os.path.exists("/Applications/Opera GX.app") or \
                       os.path.exists(os.path.expanduser("~/Library/Application Support/com.operasoftware.OperaGX"))
            else:  # Linux
                return os.path.exists(os.path.expanduser("~/.config/opera-gx"))
        except Exception:
            return False
    
    def _get_default_browser(self) -> Optional[str]:
        """
        Detect the user's default browser.
        
        Returns:
            Optional[str]: Default browser ID or None if can't detect
        """
        try:
            system = platform.system()
            
            if system == "Windows":
                return self._get_default_browser_windows()
            elif system == "Darwin":  # macOS
                return self._get_default_browser_macos()
            else:  # Linux
                return self._get_default_browser_linux()
                
        except Exception as e:
            logger.warning(f"Could not detect default browser: {e}")
            return None
    
    def _get_default_browser_windows(self) -> Optional[str]:
        """Get default browser on Windows."""
        try:
            import winreg
            
            # Check registry for default browser
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice") as key:
                prog_id = winreg.QueryValueEx(key, "ProgId")[0]
            
            # Map ProgId to our browser IDs
            browser_mapping = {
                'ChromeHTML': 'chrome',
                'FirefoxURL': 'firefox',
                'MSEdgeHTM': 'edge',
                'BraveHTML': 'brave',
                'OperaStable': 'opera',
                'Opera.GX': 'opera_gx'
            }
            
            for prog_id_pattern, browser_id in browser_mapping.items():
                if prog_id_pattern in prog_id:
                    if self.supported_browsers[browser_id]['available']:
                        return browser_id
            
        except Exception as e:
            logger.debug(f"Registry check failed: {e}")
        
        return None
    
    def _get_default_browser_macos(self) -> Optional[str]:
        """Get default browser on macOS."""
        try:
            import subprocess
            
            # Get default browser bundle ID
            result = subprocess.run(['defaults', 'read', 'com.apple.LaunchServices/com.apple.launchservices.secure', 'LSHandlers'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                output = result.stdout
                
                # Map bundle IDs to our browser IDs
                browser_mapping = {
                    'com.google.chrome': 'chrome',
                    'org.mozilla.firefox': 'firefox',
                    'com.microsoft.edgemac': 'edge',
                    'com.brave.browser': 'brave',
                    'com.operasoftware.opera': 'opera',
                    'com.operasoftware.operagx': 'opera_gx',
                    'com.apple.safari': 'safari'
                }
                
                for bundle_id, browser_id in browser_mapping.items():
                    if bundle_id in output and self.supported_browsers[browser_id]['available']:
                        return browser_id
                        
        except Exception as e:
            logger.debug(f"macOS default browser detection failed: {e}")
        
        return None
    
    def _get_default_browser_linux(self) -> Optional[str]:
        """Get default browser on Linux."""
        try:
            import subprocess
            
            # Try xdg-settings
            result = subprocess.run(['xdg-settings', 'get', 'default-web-browser'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                browser_app = result.stdout.strip().lower()
                
                # Map application names to our browser IDs
                browser_mapping = {
                    'google-chrome': 'chrome',
                    'firefox': 'firefox',
                    'microsoft-edge': 'edge',
                    'brave': 'brave',
                    'opera': 'opera'
                }
                
                for app_name, browser_id in browser_mapping.items():
                    if app_name in browser_app and self.supported_browsers[browser_id]['available']:
                        return browser_id
                        
        except Exception as e:
            logger.debug(f"Linux default browser detection failed: {e}")
        
        return None
    
    def get_browser_recommendation(self) -> Optional[str]:
        """
        Get recommended browser based on availability and user's default browser.
        
        Returns:
            Optional[str]: Recommended browser ID or None if none available
        """
        available_browsers = self.get_available_browsers()
        
        if not available_browsers:
            return None
        
        # First priority: User's default browser if available
        if self.default_browser and self.default_browser in [b['id'] for b in available_browsers]:
            logger.info(f"Recommending default browser: {self.default_browser}")
            return self.default_browser
        
        # Second priority: Sort by priority and availability
        available_browser_ids = [b['id'] for b in available_browsers]
        sorted_browsers = sorted(
            [(bid, binfo) for bid, binfo in self.supported_browsers.items() 
             if bid in available_browser_ids],
            key=lambda x: x[1]['priority']
        )
        
        if sorted_browsers:
            recommended = sorted_browsers[0][0]
            logger.info(f"Recommending by priority: {recommended}")
            return recommended
        
        # Fallback: Return first available
        return available_browsers[0]['id']
    
    def get_available_browsers_sorted(self) -> List[Dict]:
        """
        Get available browsers sorted by recommendation priority.
        
        Returns:
            List[Dict]: Sorted list of available browser information
        """
        available_browsers = self.get_available_browsers()
        
        if not available_browsers:
            return []
        
        # Create a list with priority information
        browsers_with_priority = []
        for browser in available_browsers:
            browser_info = browser.copy()
            browser_id = browser['id']
            
            # Set priority based on default browser and system priority
            if browser_id == self.default_browser:
                browser_info['is_default'] = True
                browser_info['sort_priority'] = 1  # Highest priority
                browser_info['name'] = f"🌟 {browser_info['name']} (Default)"
            else:
                browser_info['is_default'] = False
                browser_info['sort_priority'] = self.supported_browsers[browser_id]['priority']
            
            browsers_with_priority.append(browser_info)
        
        # Sort by priority (lower number = higher priority)
        return sorted(browsers_with_priority, key=lambda x: x['sort_priority'])
    
    def get_default_browser_info(self) -> Optional[Dict]:
        """
        Get information about the user's default browser.
        
        Returns:
            Optional[Dict]: Default browser information or None
        """
        if not self.default_browser:
            return None
            
        if self.default_browser in self.supported_browsers:
            browser_info = self.supported_browsers[self.default_browser].copy()
            browser_info['id'] = self.default_browser
            return browser_info
            
        return None
