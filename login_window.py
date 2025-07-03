#!/usr/bin/env python3
"""
Login Window Module

This module provides a login interface for the Udemy Course Enroller application.
It supports both email/password login and browser cookie authentication.
"""

import logging
import threading
import tkinter.messagebox as messagebox
from typing import Callable, Optional

import customtkinter as ctk
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set appearance mode and color theme
ctk.set_appearance_mode("system")  # Follow system theme
ctk.set_default_color_theme("blue")

# Import new theme configuration
try:
    from theme_config import NEW_COLORS, FONTS as NEW_FONTS, apply_education_theme
    COLORS = NEW_COLORS
    FONTS = NEW_FONTS
    # Apply the education theme
    apply_education_theme()
except ImportError:
    # Fallback to original colors if theme_config is not available
    COLORS = {
        'primary': "#6D4C7D",
        'primary_hover': "#5A3F68", 
        'secondary': "#C86B85",
        'secondary_hover': "#B55A73",
        'success': "#27AE60",
        'success_hover': "#229954",
        'error': "#E74C3C",
        'surface': "#FFFFFF",
        'surface_variant': "#F8F9FA",
        'on_surface': "#2C3E50",
        'on_surface_variant': "#6C757D",
        'outline': "#E1E4E8"
    }
    
    # Typography
    FONTS = {
        'title': ("Segoe UI", 28, "bold"),
        'subtitle': ("Segoe UI", 14),
        'body': ("Segoe UI", 12),
        'small': ("Segoe UI", 10),
        'button': ("Segoe UI", 12, "bold")
    }


class LoginWindow:
    """
    Login window for Udemy Course Enroller application.
    
    Provides two authentication methods:
    1. Email/Password login
    2. Browser cookie authentication
    """
    
    def __init__(self, on_success_callback: Optional[Callable] = None):
        """
        Initialize the login window.
        
        Args:
            on_success_callback: Function to call on successful login
        """
        self.on_success_callback = on_success_callback
        self.window = None
        self.email_entry = None
        self.password_entry = None
        self.login_button = None
        self.cookie_button = None
        self.status_label = None
        self.progress_bar = None
        
        # Authentication state
        self.is_authenticated = False
        self.user_info = None
        self.session = None
        self.login_successful = False  # Add flag to track successful login
        
        self._setup_window()
    
    def _setup_window(self):
        """Setup the login window and its components."""
        # Create main window
        self.window = ctk.CTk()
        self.window.title("Udemy Course Enroller")
        self.window.geometry("450x650")
        self.window.resizable(False, False)
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.window.winfo_screenheight() // 2) - (650 // 2)
        self.window.geometry(f"450x650+{x}+{y}")
        
        # Create scrollable main frame
        self.main_frame = ctk.CTkScrollableFrame(
            self.window,
            corner_radius=0,
            fg_color="transparent"
        )
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Create content sections
        self._create_header()
        self._create_theme_toggle()
        self._create_login_sections()
        self._create_status_section()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        # Bind Enter key to login
        self.window.bind('<Return>', lambda event: self._on_email_login())
    
    def _create_header(self):
        """Create the header with logo and title."""
        # Header container
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        # App icon/logo with gradient effect
        logo_frame = ctk.CTkFrame(
            header_frame, 
            width=80, 
            height=80, 
            corner_radius=40,
            fg_color=COLORS['primary']
        )
        logo_frame.pack(pady=(0, 20))
        logo_frame.pack_propagate(False)
        
        # Use education-themed emoji
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="🎓",
            font=("Segoe UI", 36),
            text_color="white"
        )
        logo_label.pack(expand=True)
        
        # Title with education theme
        title_label = ctk.CTkLabel(
            header_frame,
            text="Udemy Course Enroller",
            font=FONTS['title'],
            text_color=COLORS['primary']
        )
        title_label.pack(pady=(0, 8))
        
        # Subtitle with educational context
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="📚 Discover & Enroll in Free Courses",
            font=FONTS['subtitle'],
            text_color=COLORS['secondary']
        )
        subtitle_label.pack()
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Discover and enroll in free courses automatically",
            font=FONTS['subtitle'],
            text_color="gray60"
        )
        subtitle_label.pack()
    
    def _create_theme_toggle(self):
        """Create theme toggle button."""
        theme_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        theme_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        self.theme_button = ctk.CTkButton(
            theme_frame,
            text="🌙 Dark Mode",
            command=self._toggle_theme,
            width=120,
            height=32,
            font=FONTS['small'],
            fg_color="gray20",
            hover_color="gray30"
        )
        self.theme_button.pack(side="right")
    
    def _create_login_sections(self):
        """Create both login method sections."""
        # Container for login methods
        login_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        login_container.pack(fill="x", padx=30, pady=20)
        
        # Email/Password Login Card
        self._create_email_login_card(login_container)
        
        # Divider
        divider_frame = ctk.CTkFrame(login_container, fg_color="transparent")
        divider_frame.pack(fill="x", pady=25)
        
        divider_line = ctk.CTkFrame(divider_frame, height=1, fg_color="gray80")
        divider_line.pack(fill="x", pady=10)
        
        divider_text = ctk.CTkLabel(
            divider_frame,
            text="OR",
            font=FONTS['small'],
            text_color="gray60"
        )
        divider_text.place(relx=0.5, rely=0.5, anchor="center")
        
        # Browser Cookie Login Card
        self._create_cookie_login_card(login_container)
    
    def _create_email_login_card(self, parent):
        """Create the email/password login card."""
        # Main card frame
        card_frame = ctk.CTkFrame(parent, corner_radius=12)
        card_frame.pack(fill="x", pady=(0, 10))
        
        # Card header
        header_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(25, 15))
        
        # Icon and title with new theme
        icon_label = ctk.CTkLabel(
            header_frame,
            text="📧",  # Updated email icon
            font=("Segoe UI", 24)
        )
        icon_label.pack(side="left")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Email & Password",
            font=FONTS['button'],
            text_color=COLORS['primary']
        )
        title_label.pack(side="left", padx=(12, 0))
        
        # Form container
        form_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=25, pady=(0, 25))
        
        # Email field
        email_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        email_container.pack(fill="x", pady=(0, 15))
        
        email_label = ctk.CTkLabel(
            email_container,
            text="Email Address",
            font=FONTS['body'],
            anchor="w"
        )
        email_label.pack(fill="x", pady=(0, 5))
        
        self.email_entry = ctk.CTkEntry(
            email_container,
            placeholder_text="your.email@example.com",
            height=45,
            font=FONTS['body'],
            corner_radius=8
        )
        self.email_entry.pack(fill="x")
        
        # Password field
        password_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_container.pack(fill="x", pady=(0, 20))
        
        password_label = ctk.CTkLabel(
            password_container,
            text="Password",
            font=FONTS['body'],
            anchor="w"
        )
        password_label.pack(fill="x", pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            password_container,
            placeholder_text="Enter your password",
            show="*",
            height=45,
            font=FONTS['body'],
            corner_radius=8
        )
        self.password_entry.pack(fill="x")
        
        # Login button with new theme
        self.login_button = ctk.CTkButton(
            form_frame,
            text="🎯 Sign In",  # Updated icon
            command=self._on_email_login,
            height=45,
            font=FONTS['button'],
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover'],
            corner_radius=12  # More rounded corners
        )
        self.login_button.pack(fill="x")
    
    def _create_cookie_login_card(self, parent):
        """Create the browser cookie login card."""
        # Main card frame
        card_frame = ctk.CTkFrame(parent, corner_radius=12)
        card_frame.pack(fill="x", pady=(10, 0))
        
        # Card content
        content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=25, pady=25)
        
        # Icon and title with education theme
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))
        
        icon_label = ctk.CTkLabel(
            header_frame,
            text="🌐",  # Updated browser icon
            font=("Segoe UI", 24)
        )
        icon_label.pack(side="left")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Browser Session",
            font=FONTS['button'],
            text_color=COLORS['secondary']  # Use secondary color
        )
        title_label.pack(side="left", padx=(12, 0))
        
        # Browser detection and setup
        self._setup_browser_options(content_frame)
    
    def _setup_browser_options(self, parent):
        """Setup browser options based on available browsers."""
        try:
            from browser_manager import BrowserManager
            
            browser_manager = BrowserManager()
            available_browsers = browser_manager.get_available_browsers_sorted()  # Use sorted version
            
            if not available_browsers:
                # No browsers available
                warning_label = ctk.CTkLabel(
                    parent,
                    text="⚠️ No supported browsers found with browser_cookie3 support.\nPlease use email/password login instead.",
                    font=FONTS['small'],
                    text_color="orange",
                    justify="center"
                )
                warning_label.pack(fill="x", pady=(0, 20))
                
                # Disabled button
                self.cookie_button = ctk.CTkButton(
                    parent,
                    text="🚫 Browser Login Unavailable",
                    command=None,
                    height=45,
                    font=FONTS['button'],
                    fg_color="gray50",
                    hover_color="gray50",
                    corner_radius=8,
                    state="disabled"
                )
                self.cookie_button.pack(fill="x")
                return
            
            # Show default browser info if available
            default_browser_info = browser_manager.get_default_browser_info()
            if default_browser_info:
                default_note = ctk.CTkLabel(
                    parent,
                    text=f"💡 Detected default browser: {default_browser_info['name']}",
                    font=FONTS['small'],
                    text_color="blue",
                    justify="center"
                )
                default_note.pack(fill="x", pady=(0, 10))
            
            # Show available browsers
            if len(available_browsers) == 1:
                # Single browser available
                browser = available_browsers[0]
                browser_name = browser['name'].replace(' (Default)', '')  # Clean name for description
                description = ctk.CTkLabel(
                    parent,
                    text=f"Use your existing {browser_name} session\nMake sure you're logged into Udemy in {browser_name}",
                    font=FONTS['small'],
                    text_color="gray60",
                    justify="left"
                )
                description.pack(fill="x", pady=(0, 20))
                
                # Single browser button with new theme
                self.cookie_button = ctk.CTkButton(
                    parent,
                    text=f"{browser['icon']} Use {browser['name']} Session",
                    command=lambda: self._on_cookie_login(browser['id']),
                    height=45,
                    font=FONTS['button'],
                    fg_color=COLORS['secondary'],  # Use secondary color
                    hover_color=COLORS['secondary_hover'],
                    corner_radius=12  # More rounded corners
                )
                self.cookie_button.pack(fill="x")
                
            else:
                # Multiple browsers available
                description = ctk.CTkLabel(
                    parent,
                    text="Select your preferred browser to use existing session\nBrowsers are sorted by preference (default first)",
                    font=FONTS['small'],
                    text_color="gray60",
                    justify="left"
                )
                description.pack(fill="x", pady=(0, 15))
                
                # Browser selection frame
                browser_frame = ctk.CTkFrame(parent, fg_color="transparent")
                browser_frame.pack(fill="x", pady=(0, 10))
                
                # Create buttons for each browser (sorted by priority)
                for i, browser in enumerate(available_browsers):
                    # Use different colors for default browser
                    if browser.get('is_default', False):
                        button_color = COLORS['primary']
                        button_hover = COLORS['primary_hover']
                    else:
                        button_color = COLORS['secondary']  # Use secondary instead of success
                        button_hover = COLORS['secondary_hover']
                    
                    browser_button = ctk.CTkButton(
                        browser_frame,
                        text=f"{browser['icon']} {browser['name']}",
                        command=lambda b_id=browser['id']: self._on_cookie_login(b_id),
                        height=40,
                        font=FONTS['body'],
                        fg_color=button_color,
                        hover_color=button_hover,
                        corner_radius=6
                    )
                    browser_button.pack(fill="x", pady=(0, 5))
                
                # Set the first button as the main cookie button for reference
                self.cookie_button = browser_button
                
        except Exception as e:
            logger.error(f"Error setting up browser options: {e}")
            
            # Fallback to Chrome-only mode
            description = ctk.CTkLabel(
                parent,
                text="Use your existing Chrome session (recommended)\nMake sure you're logged into Udemy in Chrome",
                font=FONTS['small'],
                text_color="gray60",
                justify="left"
            )
            description.pack(fill="x", pady=(0, 20))
            
            # Cookie login button
            self.cookie_button = ctk.CTkButton(
                parent,
                text="🔐 Use Browser Session",
                command=lambda: self._on_cookie_login('chrome'),
                height=45,
                font=FONTS['button'],
                fg_color=COLORS['success'],
                hover_color=COLORS['success_hover'],
                corner_radius=8
            )
            self.cookie_button.pack(fill="x")
    
    def _create_status_section(self):
        """Create the status and progress section."""
        # Status container
        status_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        status_container.pack(fill="x", padx=30, pady=(20, 30))
        
        # Status card
        status_card = ctk.CTkFrame(status_container, corner_radius=8, height=80)
        status_card.pack(fill="x")
        status_card.pack_propagate(False)
        
        # Status content
        status_content = ctk.CTkFrame(status_card, fg_color="transparent")
        status_content.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            status_content,
            text="🟢 Ready to login",
            font=FONTS['body'],
            text_color="gray70"
        )
        self.status_label.pack(anchor="w")
        
        # Progress bar (initially hidden)
        self.progress_bar = ctk.CTkProgressBar(
            status_content,
            height=6,
            corner_radius=3,
            progress_color=COLORS['primary']
        )
        self.progress_bar.pack(fill="x", pady=(8, 0))
        self.progress_bar.pack_forget()  # Hide initially
    
    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Light":
            ctk.set_appearance_mode("dark")
            self.theme_button.configure(text="☀️ Light Mode")
        else:
            ctk.set_appearance_mode("light")
            self.theme_button.configure(text="🌙 Dark Mode")
    
    def _on_email_login(self):
        """Handle email/password login."""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
        
        # Disable UI and show progress
        self._set_ui_state(False)
        self._show_status("Connecting to Udemy...", "loading", show_progress=True)
        
        # Start login in separate thread
        thread = threading.Thread(target=self._perform_email_login, args=(email, password))
        thread.daemon = True
        thread.start()
    
    def _on_cookie_login(self, browser_id: str = 'chrome'):
        """Handle browser cookie login."""
        # Disable UI and show progress
        self._set_ui_state(False)
        self._show_status(f"Loading browser session from {browser_id}...", "loading", show_progress=True)
        
        # Start cookie login in separate thread
        thread = threading.Thread(target=self._perform_cookie_login, args=(browser_id,))
        thread.daemon = True
        thread.start()
    
    def _perform_email_login(self, email: str, password: str):
        """
        Perform email/password authentication in background thread.
        
        Args:
            email: User's email
            password: User's password
        """
        try:
            logger.info(f"Attempting login for email: {email}")
            
            # Import UdemyEnroller
            from udemy_enroller import UdemyEnroller
            
            # Update status
            self.window.after(0, lambda: self._show_status("Connecting to Udemy...", "loading"))
            
            # Create enroller and attempt login
            enroller = UdemyEnroller()
            
            # Attempt login with email and password
            if not enroller.login_with_email_password(email, password):
                raise Exception("Invalid email or password. Please check your credentials.")
            
            # Validate authentication
            self.window.after(0, lambda: self._show_status("Validating credentials...", "loading"))
            
            if not enroller.validate_authentication():
                raise Exception("Authentication validation failed. Please try again.")
            
            # Success
            self.session = enroller.session
            self.user_info = enroller.user_info
            self.is_authenticated = True
            
            user_name = self.user_info.get('display_name', 'Unknown User')
            self.window.after(0, lambda: self._on_login_success(f"Welcome, {user_name}!"))
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Email login failed: {error_msg}")
            self.window.after(0, lambda: self._on_login_error(error_msg))
    
    def _perform_cookie_login(self, browser_id: str = 'chrome'):
        """Perform browser cookie authentication in background thread."""
        try:
            # Import here to avoid issues if module is not available
            from udemy_enroller import UdemyEnroller
            from browser_manager import BrowserManager
            
            logger.info(f"Attempting browser cookie login from {browser_id}")
            
            # Get browser name for user messages
            browser_manager = BrowserManager()
            available_browsers = browser_manager.get_available_browsers()
            browser_name = next((b['name'] for b in available_browsers if b['id'] == browser_id), browser_id.title())
            
            # Update status
            self.window.after(0, lambda: self._show_status(f"Reading {browser_name} session...", "loading"))
            
            # Create enroller and load cookies
            enroller = UdemyEnroller()
            
            if not enroller.load_cookies_from_browser(browser_id):
                raise Exception(f"Failed to load cookies from {browser_name}. Make sure you're logged into Udemy in {browser_name}.")
            
            # Validate authentication
            self.window.after(0, lambda: self._show_status("Validating session...", "loading"))
            
            if not enroller.validate_authentication():
                raise Exception(f"Authentication failed. Please login to Udemy in {browser_name} first.")
            
            # Success
            self.session = enroller.session
            self.user_info = enroller.user_info
            self.is_authenticated = True
            
            user_name = self.user_info.get('display_name', 'Unknown')
            self.window.after(0, lambda: self._on_login_success(f"Welcome, {user_name}!"))
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Cookie login failed: {error_msg}")
            self.window.after(0, lambda: self._on_login_error(error_msg))
    
    def _on_login_success(self, message: str):
        """Handle successful login with modern feedback."""
        self._show_status(f"Success! {message}", "success", show_progress=False)
        
        # Re-enable UI briefly to show success state
        self.login_button.configure(text="✅ Success!", fg_color=COLORS['success'])
        self.cookie_button.configure(text="✅ Success!", fg_color=COLORS['success'])
        
        # Call success callback if provided
        if self.on_success_callback:
            self.on_success_callback(self.session, self.user_info)
        
        # Wait a moment then close window
        self.window.after(1500, self._close_and_continue)
    
    def _close_and_continue(self):
        """Close login window and continue to main application."""
        self.login_successful = True
        self.window.destroy()
    
    def _on_login_error(self, error_message: str):
        """Handle login error with better UX."""
        self._show_status(f"Login failed: {error_message}", "error", show_progress=False)
        self._set_ui_state(True)
        
        # Reset button colors to original
        self.login_button.configure(fg_color=COLORS['primary'])
        self.cookie_button.configure(fg_color=COLORS['success'])
        
        # Show error dialog with better formatting
        messagebox.showerror(
            "Authentication Failed", 
            f"Unable to log in:\n\n{error_message}\n\nPlease check your credentials and try again."
        )
    
    def _close_and_continue(self):
        """Close login window and continue to main app."""
        if self.on_success_callback and self.is_authenticated:
            self.on_success_callback(self.session, self.user_info)
        
        self.window.destroy()
    
    def _set_ui_state(self, enabled: bool):
        """Enable/disable UI elements with visual feedback."""
        if enabled:
            # Enable all inputs and buttons
            self.email_entry.configure(state="normal")
            self.password_entry.configure(state="normal")
            self.login_button.configure(state="normal", text="🚀 Sign In")
            self.cookie_button.configure(state="normal", text="🔐 Use Browser Session")
        else:
            # Disable inputs and show loading state
            self.email_entry.configure(state="disabled")
            self.password_entry.configure(state="disabled")
            self.login_button.configure(state="disabled", text="⏳ Signing In...")
            self.cookie_button.configure(state="disabled", text="⏳ Connecting...")
    
    def _show_status(self, message: str, status_type: str = "info", show_progress: bool = False):
        """Update status message with icons and colors."""
        # Status icons and colors
        status_config = {
            "info": {"icon": "🔵", "color": "gray70"},
            "success": {"icon": "🟢", "color": COLORS['success']},
            "error": {"icon": "🔴", "color": COLORS['error']},
            "warning": {"icon": "🟡", "color": "#f57c00"},
            "loading": {"icon": "⏳", "color": COLORS['primary']}
        }
        
        config = status_config.get(status_type, status_config["info"])
        status_text = f"{config['icon']} {message}"
        
        self.status_label.configure(text=status_text, text_color=config['color'])
        
        if show_progress:
            self.progress_bar.pack(fill="x", pady=(8, 0))
            self.progress_bar.set(0.5)  # Indeterminate progress
        else:
            self.progress_bar.pack_forget()
    
    def _on_window_close(self):
        """Handle window close event."""
        if not self.is_authenticated:
            if messagebox.askokcancel("Quit", "You must login to use the application. Do you want to quit?"):
                self.login_successful = False
                self.window.destroy()
        else:
            self.login_successful = True
            self.window.destroy()
    
    def show(self):
        """
        Show the login window and start the GUI loop.
        
        Returns:
            bool: True if login was successful, False otherwise
        """
        logger.info("Showing login window")
        
        # Handle window close protocol
        self.window.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        # Start the main loop
        self.window.mainloop()
        
        # Return whether login was successful
        return self.login_successful and self.is_authenticated
    
    def get_authentication_info(self):
        """
        Get authentication information after successful login.
        
        Returns:
            tuple: (session, user_info) or (None, None) if not authenticated
        """
        if self.is_authenticated:
            return self.session, self.user_info
        return None, None


def main():
    """
    Example usage of the LoginWindow class.
    """
    def on_login_success(session, user_info):
        """Callback function called on successful login."""
        print(f"Login successful! User: {user_info.get('display_name', 'Unknown')}")
        print("Session and user info are now available for the main application")
    
    # Create and show login window
    login_window = LoginWindow(on_success_callback=on_login_success)
    login_window.show()


if __name__ == "__main__":
    main()
