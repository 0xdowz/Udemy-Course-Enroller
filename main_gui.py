#!/usr/bin/env python3
"""
Main GUI Module

This module provides the main interface for the Udemy Course Enroller application.
It includes course fetching, filtering, and enrollment functionality.
"""

import json
import logging
import threading
import tkinter.messagebox as messagebox
from datetime import datetime
from typing import Dict, List, Optional

import customtkinter as ctk

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
        'warning': "#F39C12",
        'error': "#E74C3C",
        'surface': "#FFFFFF",
        'surface_variant': "#F8F9FA",
        'surface_container': "#F1F3F4",
        'outline': "#E1E4E8",
        'on_surface': "#2C3E50",
        'on_surface_variant': "#6C757D"
    }

FONTS = {
    'display': ("Segoe UI", 32, "bold"),
    'headline': ("Segoe UI", 24, "bold"),
    'title': ("Segoe UI", 18, "bold"),
    'body_large': ("Segoe UI", 14),
    'body': ("Segoe UI", 12),
    'label': ("Segoe UI", 11),
    'button': ("Segoe UI", 12, "bold")
}

SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 16,
    'lg': 24,
    'xl': 32,
    'xxl': 48
}


class MainGUI:
    """
    Main GUI for the Udemy Course Enroller application.
    
    Provides functionality for:
    - Fetching courses from multiple sources
    - Filtering courses by various criteria
    - Enrolling in courses
    - Viewing enrollment status and logs
    """
    
    def __init__(self, session=None, user_info=None):
        """
        Initialize the main GUI.
        
        Args:
            session: Authenticated requests session
            user_info: User information from login
        """
        self.session = session
        self.user_info = user_info
        self.window = None
        
        # Course data
        self.all_courses = []
        self.filtered_courses = []
        self.selected_courses = []
        
        # GUI components
        self.courses_listbox = None
        self.status_label = None
        self.status_icon = None
        self.progress_bar = None
        self.filter_frame = None
        self.stats_label = None
        
        # Modern UI components
        self.total_stat = None
        self.filtered_stat = None
        self.success_stat = None
        self.content_title = None
        self.course_count_label = None
        self.selection_label = None
        self.theme_button = None
        self.fetch_button = None
        self.enroll_button = None
        self.enroll_selected_btn = None
        self.select_all_btn = None
        self.sort_var = None
        self.sort_dropdown = None
        
        # Filter controls
        self.rating_var = None
        self.duration_var = None
        self.language_var = None
        self.keyword_var = None
        
        # Status tracking
        self.is_fetching = False
        self.is_enrolling = False
        self.enrollment_results = {}
        
        # Debug panel (can be toggled)
        self.debug_mode = False
        self.debug_panel = None
        self.debug_text = None
        
        self._setup_window()
    
    def _setup_window(self):
        """Setup the main window with modern layout."""
        # Create main window
        self.window = ctk.CTk()
        self.window.title("Udemy Course Enroller")
        self.window.geometry("1400x900")
        self.window.minsize(1200, 700)
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (900 // 2)
        self.window.geometry(f"1400x900+{x}+{y}")
        
        # Configure grid weights for responsive layout
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        
        # Create layout sections
        self._create_header()
        self._create_main_content()
        self._create_status_bar()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self._on_window_close)
    
    def _create_header(self):
        """Create modern header with branding and main actions."""
        # Header frame
        header_frame = ctk.CTkFrame(self.window, height=80, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Left section - Logo and title
        left_section = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_section.grid(row=0, column=0, sticky="w", padx=SPACING['lg'], pady=SPACING['md'])
        
        # App icon
        icon_frame = ctk.CTkFrame(left_section, width=50, height=50, corner_radius=25, fg_color=COLORS['primary'])
        icon_frame.grid(row=0, column=0, padx=(0, SPACING['md']))
        icon_frame.grid_propagate(False)
        
        icon_label = ctk.CTkLabel(icon_frame, text="🎓", font=("Segoe UI", 24))
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title and user info
        title_section = ctk.CTkFrame(left_section, fg_color="transparent")
        title_section.grid(row=0, column=1)
        
        app_title = ctk.CTkLabel(
            title_section,
            text="Udemy Course Enroller",
            font=FONTS['title'],
            text_color=COLORS['primary']
        )
        app_title.pack(anchor="w")
        
        user_name = self.user_info.get('display_name', 'Guest') if self.user_info else 'Guest'
        user_label = ctk.CTkLabel(
            title_section,
            text=f"Welcome back, {user_name}",
            font=FONTS['label'],
            text_color=COLORS['on_surface_variant']
        )
        user_label.pack(anchor="w")
        
        # Right section - Main actions
        right_section = ctk.CTkFrame(header_frame, fg_color="transparent")
        right_section.grid(row=0, column=2, sticky="e", padx=SPACING['lg'], pady=SPACING['md'])
        
        # Debug toggle (hidden by default)
        self.debug_button = ctk.CTkButton(
            right_section,
            text="🐛",
            command=self._toggle_debug,
            width=40,
            height=40,
            font=("Segoe UI", 16),
            fg_color="transparent",
            hover_color=COLORS['surface_variant'],
            corner_radius=20
        )
        self.debug_button.pack(side="right", padx=(SPACING['sm'], 0))
        
        # Theme toggle
        self.theme_button = ctk.CTkButton(
            right_section,
            text="🌙",
            command=self._toggle_theme,
            width=40,
            height=40,
            font=("Segoe UI", 16),
            fg_color="transparent",
            hover_color=COLORS['surface_variant'],
            corner_radius=20
        )
        self.theme_button.pack(side="right", padx=(SPACING['sm'], 0))
        
        # Fetch button
        self.fetch_button = ctk.CTkButton(
            right_section,
            text="🔍 Discover Courses",
            command=self._on_fetch_courses,
            width=160,
            height=40,
            font=FONTS['button'],
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover'],
            corner_radius=8
        )
        self.fetch_button.pack(side="right", padx=(0, SPACING['sm']))
        
        # Enroll button
        self.enroll_button = ctk.CTkButton(
            right_section,
            text="⚡ Enroll All",
            command=self._on_enroll_all,
            width=140,
            height=40,
            font=FONTS['button'],
            fg_color=COLORS['success'],
            hover_color=COLORS['success_hover'],
            corner_radius=8,
            state="disabled"
        )
        self.enroll_button.pack(side="right", padx=(0, SPACING['sm']))
    
    def _create_main_content(self):
        """Create the main content area with modern, responsive layout."""
        # Main container with responsive grid
        main_container = ctk.CTkFrame(self.window, fg_color="transparent")
        main_container.grid(row=1, column=0, sticky="nsew", padx=SPACING['md'], pady=(0, SPACING['md']))
        
        # Configure grid weights for responsive layout
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)
        
        # Left sidebar - Filters and statistics
        self._create_sidebar(main_container)
        
        # Main content area - Course list and actions
        self._create_content_area(main_container)
    
    def _create_sidebar(self, parent):
        """Create the left sidebar with filters and statistics."""
        sidebar = ctk.CTkFrame(parent, width=300, corner_radius=12)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING['md']))
        sidebar.grid_propagate(False)
        
        # Sidebar header
        sidebar_header = ctk.CTkFrame(sidebar, fg_color="transparent", height=60)
        sidebar_header.pack(fill="x", padx=SPACING['md'], pady=(SPACING['md'], 0))
        sidebar_header.pack_propagate(False)
        
        filter_icon = ctk.CTkLabel(sidebar_header, text="🔍", font=("Segoe UI", 20))
        filter_icon.pack(side="left", pady=SPACING['sm'])
        
        filter_title = ctk.CTkLabel(
            sidebar_header,
            text="Smart Filters",
            font=FONTS['title'],
            text_color=COLORS['on_surface']
        )
        filter_title.pack(side="left", padx=(SPACING['sm'], 0), pady=SPACING['sm'])
        
        # Filter controls
        self._create_filter_controls(sidebar)
        
        # Statistics panel
        self._create_statistics_panel(sidebar)
        
        # Quick actions
        self._create_quick_actions(sidebar)
    
    def _create_filter_controls(self, parent):
        """Create modern filter controls."""
        filters_frame = ctk.CTkFrame(parent, fg_color="transparent")
        filters_frame.pack(fill="x", padx=SPACING['md'], pady=(SPACING['md'], 0))
        
        # Rating filter
        self._create_filter_input(
            filters_frame,
            "⭐ Minimum Rating",
            "rating_var",
            "4.5",
            "Enter minimum rating (0.0 - 5.0)"
        )
        
        # Duration filter
        self._create_filter_input(
            filters_frame,
            "⏱️ Max Duration (hours)",
            "duration_var",
            "",
            "Enter maximum duration in hours"
        )
        
        # Language filter
        self._create_filter_input(
            filters_frame,
            "🌍 Language",
            "language_var",
            "",
            "e.g., English, Spanish, French"
        )
        
        # Keywords filter
        self._create_filter_input(
            filters_frame,
            "🔍 Keywords",
            "keyword_var",
            "",
            "e.g., Python, Web Development, AI"
        )
        
        # Filter actions
        filter_actions = ctk.CTkFrame(filters_frame, fg_color="transparent")
        filter_actions.pack(fill="x", pady=(SPACING['lg'], 0))
        
        # Apply filters button
        self.apply_filters_btn = ctk.CTkButton(
            filter_actions,
            text="Apply Filters",
            command=self._on_apply_filters,
            height=40,
            font=FONTS['button'],
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover'],
            corner_radius=8
        )
        self.apply_filters_btn.pack(fill="x", pady=(0, SPACING['sm']))
        
        # Clear filters button
        self.clear_filters_btn = ctk.CTkButton(
            filter_actions,
            text="Clear All",
            command=self._on_clear_filters,
            height=36,
            font=FONTS['label'],
            fg_color="transparent",
            hover_color=COLORS['surface_variant'],
            text_color=COLORS['on_surface_variant'],
            border_width=1,
            border_color=COLORS['outline'],
            corner_radius=8
        )
        self.clear_filters_btn.pack(fill="x")
    
    def _create_filter_input(self, parent, label_text, var_name, default_value, placeholder):
        """Create a modern filter input field."""
        # Container for label and input
        input_container = ctk.CTkFrame(parent, fg_color="transparent")
        input_container.pack(fill="x", pady=(0, SPACING['md']))
        
        # Label
        label = ctk.CTkLabel(
            input_container,
            text=label_text,
            font=FONTS['label'],
            text_color=COLORS['on_surface']
        )
        label.pack(anchor="w", pady=(0, SPACING['xs']))
        
        # Input field
        var = ctk.StringVar(value=default_value)
        setattr(self, var_name, var)
        
        entry = ctk.CTkEntry(
            input_container,
            textvariable=var,
            placeholder_text=placeholder,
            height=36,
            font=FONTS['body'],
            corner_radius=8,
            border_width=1,
            border_color=COLORS['outline']
        )
        entry.pack(fill="x")
        
        # Bind Enter key to apply filters
        entry.bind('<Return>', lambda e: self._on_apply_filters())
    
    def _create_statistics_panel(self, parent):
        """Create statistics panel with modern cards."""
        stats_frame = ctk.CTkFrame(parent, corner_radius=12)
        stats_frame.pack(fill="x", padx=SPACING['md'], pady=(SPACING['lg'], 0))
        
        # Stats header
        stats_header = ctk.CTkLabel(
            stats_frame,
            text="📊 Statistics",
            font=FONTS['body_large'],
            text_color=COLORS['on_surface']
        )
        stats_header.pack(pady=(SPACING['md'], SPACING['sm']))
        
        # Stats grid
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=SPACING['md'], pady=(0, SPACING['md']))
        
        # Total courses stat
        self.total_stat = self._create_stat_card(stats_grid, "Total", "0", "📚")
        self.total_stat.pack(fill="x", pady=(0, SPACING['xs']))
        
        # Filtered courses stat
        self.filtered_stat = self._create_stat_card(stats_grid, "Filtered", "0", "🔍")
        self.filtered_stat.pack(fill="x", pady=(0, SPACING['xs']))
        
        # Success rate stat
        self.success_stat = self._create_stat_card(stats_grid, "Success Rate", "0%", "✅")
        self.success_stat.pack(fill="x")
    
    def _create_stat_card(self, parent, label, value, icon):
        """Create a statistics card."""
        card = ctk.CTkFrame(parent, fg_color=COLORS['surface_variant'], corner_radius=8)
        
        # Card content
        card_content = ctk.CTkFrame(card, fg_color="transparent")
        card_content.pack(fill="both", expand=True, padx=SPACING['sm'], pady=SPACING['sm'])
        
        # Icon and label
        header_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        header_frame.pack(fill="x")
        
        icon_label = ctk.CTkLabel(header_frame, text=icon, font=("Segoe UI", 14))
        icon_label.pack(side="left")
        
        label_text = ctk.CTkLabel(
            header_frame,
            text=label,
            font=FONTS['label'],
            text_color=COLORS['on_surface_variant']
        )
        label_text.pack(side="left", padx=(SPACING['xs'], 0))
        
        # Value
        value_label = ctk.CTkLabel(
            card_content,
            text=value,
            font=FONTS['body_large'],
            text_color=COLORS['on_surface']
        )
        value_label.pack(anchor="w", pady=(SPACING['xs'], 0))
        
        # Store value label for updates
        card.value_label = value_label
        
        return card
    
    def _create_quick_actions(self, parent):
        """Create quick action buttons."""
        actions_frame = ctk.CTkFrame(parent, fg_color="transparent")
        actions_frame.pack(fill="x", padx=SPACING['md'], pady=(SPACING['lg'], SPACING['md']))
        
        # Quick action buttons
        self.refresh_btn = ctk.CTkButton(
            actions_frame,
            text="🔄 Refresh",
            command=self._on_refresh,
            height=40,
            font=FONTS['button'],
            fg_color=COLORS['secondary'],
            hover_color=COLORS['primary_hover'],
            corner_radius=8
        )
        self.refresh_btn.pack(fill="x", pady=(0, SPACING['sm']))
        
        self.export_btn = ctk.CTkButton(
            actions_frame,
            text="📤 Export List",
            command=self._on_export_courses,
            height=40,
            font=FONTS['button'],
            fg_color="transparent",
            hover_color=COLORS['surface_variant'],
            text_color=COLORS['on_surface_variant'],
            border_width=1,
            border_color=COLORS['outline'],
            corner_radius=8
        )
        self.export_btn.pack(fill="x")
    
    def _create_content_area(self, parent):
        """Create the main content area."""
        content_frame = ctk.CTkFrame(parent, corner_radius=12)
        content_frame.grid(row=0, column=1, sticky="nsew")
        
        # Content header
        self._create_content_header(content_frame)
        
        # Course list
        self._create_course_list(content_frame)
        
        # Action bar
        self._create_action_bar(content_frame)
    
    def _create_content_header(self, parent):
        """Create the content area header."""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent", height=60)
        header_frame.pack(fill="x", padx=SPACING['md'], pady=(SPACING['md'], 0))
        header_frame.pack_propagate(False)
        
        # Title and course count
        title_section = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_section.pack(side="left", fill="y")
        
        self.content_title = ctk.CTkLabel(
            title_section,
            text="📚 Available Courses",
            font=FONTS['title'],
            text_color=COLORS['on_surface']
        )
        self.content_title.pack(anchor="w", pady=(SPACING['sm'], 0))
        
        self.course_count_label = ctk.CTkLabel(
            title_section,
            text="Ready to discover amazing courses",
            font=FONTS['label'],
            text_color=COLORS['on_surface_variant']
        )
        self.course_count_label.pack(anchor="w")
        
        # View options
        view_options = ctk.CTkFrame(header_frame, fg_color="transparent")
        view_options.pack(side="right", fill="y")
        
        # Sort dropdown
        self.sort_var = ctk.StringVar(value="Recent")
        self.sort_dropdown = ctk.CTkComboBox(
            view_options,
            variable=self.sort_var,
            values=["Recent", "Rating", "Duration", "Title"],
            command=self._on_sort_changed,
            width=120,
            height=32,
            font=FONTS['body']
        )
        self.sort_dropdown.pack(side="right", padx=(SPACING['sm'], 0))
        
        sort_label = ctk.CTkLabel(
            view_options,
            text="Sort by:",
            font=FONTS['label'],
            text_color=COLORS['on_surface_variant']
        )
        sort_label.pack(side="right", pady=SPACING['sm'])
    
    def _create_course_list(self, parent):
        """Create the scrollable course list."""
        # Create scrollable frame
        self.courses_scrollable = ctk.CTkScrollableFrame(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )
        self.courses_scrollable.pack(fill="both", expand=True, padx=SPACING['md'], pady=(SPACING['md'], 0))
        
        # Initially show empty state
        self._show_empty_state()
    
    def _create_action_bar(self, parent):
        """Create the bottom action bar."""
        action_bar = ctk.CTkFrame(parent, height=70, corner_radius=0)
        action_bar.pack(fill="x", side="bottom")
        action_bar.pack_propagate(False)
        
        # Selection info
        selection_frame = ctk.CTkFrame(action_bar, fg_color="transparent")
        selection_frame.pack(side="left", fill="y", padx=SPACING['md'])
        
        self.selection_label = ctk.CTkLabel(
            selection_frame,
            text="No courses selected",
            font=FONTS['body'],
            text_color=COLORS['on_surface_variant']
        )
        self.selection_label.pack(anchor="w", pady=(SPACING['md'], 0))
        
        # Bulk actions
        bulk_actions = ctk.CTkFrame(action_bar, fg_color="transparent")
        bulk_actions.pack(side="right", fill="y", padx=SPACING['md'])
        
        # Select all button
        self.select_all_btn = ctk.CTkButton(
            bulk_actions,
            text="Select All",
            command=self._on_select_all,
            width=100,
            height=36,
            font=FONTS['label'],
            fg_color="transparent",
            hover_color=COLORS['surface_variant'],
            text_color=COLORS['on_surface_variant'],
            border_width=1,
            border_color=COLORS['outline']
        )
        self.select_all_btn.pack(side="right", padx=(SPACING['sm'], 0), pady=SPACING['md'])
        
        # Enroll selected button
        self.enroll_selected_btn = ctk.CTkButton(
            bulk_actions,
            text="⚡ Enroll Selected",
            command=self._on_enroll_selected,
            width=140,
            height=36,
            font=FONTS['button'],
            fg_color=COLORS['success'],
            hover_color=COLORS['success_hover'],
            state="disabled"
        )
        self.enroll_selected_btn.pack(side="right", padx=(0, SPACING['sm']), pady=SPACING['md'])
    
    def _create_status_bar(self):
        """Create the modern status bar at the bottom."""
        status_frame = ctk.CTkFrame(self.window, height=50, corner_radius=0)
        status_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        status_frame.grid_propagate(False)
        status_frame.grid_columnconfigure(1, weight=1)
        
        # Status icon and message
        status_content = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_content.grid(row=0, column=0, sticky="w", padx=SPACING['md'], pady=SPACING['sm'])
        
        self.status_icon = ctk.CTkLabel(
            status_content,
            text="✅",
            font=("Segoe UI", 16)
        )
        self.status_icon.pack(side="left", padx=(0, SPACING['xs']))
        
        self.status_label = ctk.CTkLabel(
            status_content,
            text="Ready to discover amazing courses",
            font=FONTS['body'],
            text_color=COLORS['on_surface']
        )
        self.status_label.pack(side="left")
        
        # Progress indicator
        progress_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
        progress_frame.grid(row=0, column=1, sticky="e", padx=SPACING['md'], pady=SPACING['sm'])
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            width=200,
            height=8,
            corner_radius=4
        )
        self.progress_bar.pack(side="right")
        self.progress_bar.pack_forget()  # Hide initially
        
        # Version info
        version_label = ctk.CTkLabel(
            status_frame,
            text="v1.0.0",
            font=FONTS['label'],
            text_color=COLORS['on_surface_variant']
        )
        version_label.grid(row=0, column=2, sticky="e", padx=SPACING['md'], pady=SPACING['sm'])
    
    def _show_empty_state(self):
        """Show modern empty state when no courses are loaded."""
        # Clear existing widgets
        for widget in self.courses_scrollable.winfo_children():
            widget.destroy()
        
        # Empty state container
        empty_container = ctk.CTkFrame(self.courses_scrollable, fg_color="transparent")
        empty_container.pack(expand=True, fill="both", pady=100)
        
        # Empty state icon
        empty_icon = ctk.CTkLabel(
            empty_container,
            text="🎯",
            font=("Segoe UI", 48)
        )
        empty_icon.pack(pady=(0, SPACING['md']))
        
        # Empty state title
        empty_title = ctk.CTkLabel(
            empty_container,
            text="Ready to Discover Courses",
            font=FONTS['headline'],
            text_color=COLORS['on_surface']
        )
        empty_title.pack(pady=(0, SPACING['sm']))
        
        # Empty state description
        empty_desc = ctk.CTkLabel(
            empty_container,
            text="Click 'Discover Courses' to find amazing free courses\nfrom multiple sources with available coupons",
            font=FONTS['body'],
            text_color=COLORS['on_surface_variant'],
            justify="center"
        )
        empty_desc.pack(pady=(0, SPACING['lg']))
        
        # Quick start button
        quick_start_btn = ctk.CTkButton(
            empty_container,
            text="🚀 Get Started",
            command=self._on_fetch_courses,
            height=48,
            width=200,
            font=FONTS['button'],
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover'],
            corner_radius=24
        )
        quick_start_btn.pack()
    
    def _on_fetch_courses(self):
        """Handle fetch courses button click with improved UX."""
        if self.is_fetching:
            return
        
        self.is_fetching = True
        self.fetch_button.configure(text="⏳ Discovering...", state="disabled")
        self._show_status("Discovering courses from multiple sources...", show_progress=True, status_type="loading")
        
        # Start fetching in separate thread
        thread = threading.Thread(target=self._fetch_courses_thread)
        thread.daemon = True
        thread.start()
    
    def _fetch_courses_thread(self):
        """Fetch courses in background thread."""
        try:
            # Import here to avoid circular imports
            from udemy_coupon_scraper import UdemyCouponScraper
            
            logger.info("Starting course fetching")
            
            # Create scraper and fetch courses
            scraper = UdemyCouponScraper()
            courses = scraper.get_all_courses()
            
            # Update UI in main thread
            self.window.after(0, lambda: self._on_courses_fetched(courses))
            
        except Exception as e:
            error_msg = f"Error fetching courses: {str(e)}"
            logger.error(error_msg)
            self.window.after(0, lambda: self._on_fetch_error(error_msg))
    
    def _on_courses_fetched(self, courses: List[Dict]):
        """Handle successful course fetching with improved UX."""
        self.all_courses = courses
        self.filtered_courses = courses.copy()
        
        # Clear selection since courses changed
        self.selected_courses.clear()
        
        self._update_course_display()
        self._update_stats()
        self._update_selection_info()
        
        self.is_fetching = False
        self.fetch_button.configure(text="🔍 Discover Courses", state="normal")
        self.enroll_button.configure(state="normal")
        
        # Show success status
        self._show_status(f"Successfully discovered {len(courses)} courses!", status_type="success")
        
        logger.info(f"Successfully fetched {len(courses)} courses")
    
    def _on_fetch_error(self, error_msg: str):
        """Handle course fetching error with improved UX."""
        self.is_fetching = False
        self.fetch_button.configure(text="🔍 Discover Courses", state="normal")
        self._show_status(f"Discovery failed: {error_msg}", status_type="error")
        
        messagebox.showerror("Discovery Error", f"Failed to discover courses:\n\n{error_msg}")
    
    def _on_enrollment_complete(self, results: Dict):
        """Handle successful completion of enrollment with improved UX."""
        self.enrollment_results = results
        
        # Count successful enrollments
        successful = sum(1 for r in results.values() if r.get('success', False))
        total = len(results)
        
        self.is_enrolling = False
        self.enroll_button.configure(text="⚡ Enroll All", state="normal")
        
        # Show success status
        if successful == total:
            status_msg = f"Perfect! All {total} courses enrolled successfully!"
            status_type = "success"
        elif successful > 0:
            status_msg = f"Partially complete: {successful}/{total} courses enrolled"
            status_type = "warning"
        else:
            status_msg = f"No courses enrolled successfully"
            status_type = "error"
        
        self._show_status(status_msg, status_type=status_type)
        
        # Update statistics
        self._update_stats()
        
        # Show detailed results
        self._show_enrollment_results(results)
        
        logger.info(f"Enrollment complete: {successful}/{total} successful")
    
    def _on_enrollment_error(self, error_msg: str):
        """Handle enrollment error with improved UX."""
        self.is_enrolling = False
        self.enroll_button.configure(text="⚡ Enroll All", state="normal")
        self._show_status(f"Enrollment failed: {error_msg}", status_type="error")
        
        messagebox.showerror("Enrollment Error", f"Enrollment process failed:\n\n{error_msg}")
    
    def _enroll_in_courses(self, courses: List[Dict]):
        """Enroll in multiple courses with improved UX."""
        if self.is_enrolling:
            return
        
        self.is_enrolling = True
        self.enroll_button.configure(text="⚡ Enrolling...", state="disabled")
        self._show_status(f"Starting enrollment in {len(courses)} courses...", show_progress=True, status_type="loading")
        
        # Start enrollment in separate thread
        thread = threading.Thread(target=self._enroll_courses_thread, args=(courses,))
        thread.daemon = True
        thread.start()
    
    def _on_apply_filters(self):
        """Apply filters to the course list."""
        if not self.all_courses:
            messagebox.showwarning("No Courses", "Please fetch courses first")
            return
        
        try:
            # Import filter function
            from filters import filter_courses
            
            # Get filter values
            min_rating = float(self.rating_var.get()) if self.rating_var.get() else 0.0
            max_duration = float(self.duration_var.get()) if self.duration_var.get() else None
            language = self.language_var.get().strip() if self.language_var.get() else None
            keywords = self.keyword_var.get().strip() if self.keyword_var.get() else None
            
            # Split keywords by comma
            if keywords:
                keywords = [kw.strip() for kw in keywords.split(',') if kw.strip()]
            
            # Apply filters
            self.filtered_courses = filter_courses(
                self.all_courses,
                min_rating=min_rating,
                max_duration=max_duration,
                language=language,
                keywords=keywords
            )
            
            self._update_course_display()
            self._update_stats()
            
            self._show_status(f"Applied filters - {len(self.filtered_courses)} courses match")
            
        except ValueError as e:
            messagebox.showerror("Filter Error", f"Invalid filter value: {str(e)}")
        except Exception as e:
            error_msg = f"Error applying filters: {str(e)}"
            logger.error(error_msg)
            messagebox.showerror("Filter Error", error_msg)
    
    def _on_clear_filters(self):
        """Clear all filters."""
        self.rating_var.set("0.0")
        self.duration_var.set("")
        self.language_var.set("")
        self.keyword_var.set("")
        
        self.filtered_courses = self.all_courses.copy()
        self._update_course_display()
        self._update_stats()
        
        self._show_status("Filters cleared")
    
    def _update_course_display(self):
        """Update the course list display with modern styling."""
        # Clear existing widgets
        for widget in self.courses_scrollable.winfo_children():
            widget.destroy()
        
        if not self.filtered_courses:
            # Show "no results" state
            no_results_container = ctk.CTkFrame(self.courses_scrollable, fg_color="transparent")
            no_results_container.pack(expand=True, fill="both", pady=100)
            
            # No results icon
            no_results_icon = ctk.CTkLabel(
                no_results_container,
                text="🔍",
                font=("Segoe UI", 36)
            )
            no_results_icon.pack(pady=(0, SPACING['md']))
            
            # No results title
            no_results_title = ctk.CTkLabel(
                no_results_container,
                text="No Courses Found",
                font=FONTS['title'],
                text_color=COLORS['on_surface']
            )
            no_results_title.pack(pady=(0, SPACING['sm']))
            
            # No results description
            no_results_desc = ctk.CTkLabel(
                no_results_container,
                text="Try adjusting your filters or fetch new courses",
                font=FONTS['body'],
                text_color=COLORS['on_surface_variant']
            )
            no_results_desc.pack()
            
            return
        
        # Display courses
        for i, course in enumerate(self.filtered_courses):
            self._create_course_widget(course, i)
        
        # Update course count in header
        self._update_course_count()
    
    def _create_course_widget(self, course: Dict, index: int):
        """Create a modern widget for displaying a single course."""
        # Course card
        course_card = ctk.CTkFrame(self.courses_scrollable, corner_radius=12)
        course_card.pack(fill="x", pady=SPACING['sm'], padx=SPACING['xs'])
        
        # Add selection state
        course_card.selected = False
        course_card.course_data = course
        course_card.course_index = index
        
        # Main content frame
        content_frame = ctk.CTkFrame(course_card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=SPACING['md'], pady=SPACING['md'])
        
        # Header row
        header_row = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_row.pack(fill="x", pady=(0, SPACING['sm']))
        
        # Selection checkbox
        checkbox_var = ctk.BooleanVar()
        checkbox = ctk.CTkCheckBox(
            header_row,
            text="",
            variable=checkbox_var,
            command=lambda: self._on_course_selection_changed(course_card, checkbox_var.get()),
            width=20,
            height=20
        )
        checkbox.pack(side="left", padx=(0, SPACING['sm']))
        course_card.checkbox = checkbox
        course_card.checkbox_var = checkbox_var
        
        # Source badge
        source = course.get('source', 'Unknown')
        source_badge = ctk.CTkLabel(
            header_row,
            text=f"📋 {source}",
            font=FONTS['label'],
            text_color=COLORS['primary'],
            fg_color=COLORS['surface_variant'],
            corner_radius=12,
            width=80,
            height=24
        )
        source_badge.pack(side="left", padx=(0, SPACING['sm']))
        
        # Rating badge (if available)
        if 'rating' in course and course['rating']:
            rating_badge = ctk.CTkLabel(
                header_row,
                text=f"⭐ {course['rating']}",
                font=FONTS['label'],
                text_color=COLORS['success'],
                fg_color=COLORS['surface_variant'],
                corner_radius=12,
                width=60,
                height=24
            )
            rating_badge.pack(side="left", padx=(0, SPACING['sm']))
        
        # Course title
        title = course.get('title', 'Unknown Title')
        title_label = ctk.CTkLabel(
            content_frame,
            text=title,
            font=FONTS['body_large'],
            text_color=COLORS['on_surface'],
            anchor="w",
            wraplength=500
        )
        title_label.pack(fill="x", pady=(0, SPACING['xs']))
        
        # Course details
        details_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        details_frame.pack(fill="x", pady=(0, SPACING['sm']))
        
        # Duration (if available)
        if 'duration' in course and course['duration']:
            duration_label = ctk.CTkLabel(
                details_frame,
                text=f"⏱️ {course['duration']}",
                font=FONTS['label'],
                text_color=COLORS['on_surface_variant']
            )
            duration_label.pack(side="left", padx=(0, SPACING['md']))
        
        # Language (if available)
        if 'language' in course and course['language']:
            language_label = ctk.CTkLabel(
                details_frame,
                text=f"🌍 {course['language']}",
                font=FONTS['label'],
                text_color=COLORS['on_surface_variant']
            )
            language_label.pack(side="left", padx=(0, SPACING['md']))
        
        # Action buttons
        action_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        action_frame.pack(fill="x", pady=(SPACING['sm'], 0))
        
        # View course button
        view_btn = ctk.CTkButton(
            action_frame,
            text="👁️ View",
            command=lambda: self._on_view_course(course),
            width=80,
            height=32,
            font=FONTS['label'],
            fg_color="transparent",
            hover_color=COLORS['surface_variant'],
            text_color=COLORS['on_surface_variant'],
            border_width=1,
            border_color=COLORS['outline']
        )
        view_btn.pack(side="left", padx=(0, SPACING['sm']))
        
        # Enroll button
        enroll_btn = ctk.CTkButton(
            action_frame,
            text="⚡ Enroll",
            command=lambda: self._on_enroll_single(index),
            width=100,
            height=32,
            font=FONTS['button'],
            fg_color=COLORS['success'],
            hover_color=COLORS['success_hover'],
            corner_radius=16
        )
        enroll_btn.pack(side="right")
        
        # Hover effects
        def on_enter(event):
            course_card.configure(fg_color=COLORS['surface_variant'])
        
        def on_leave(event):
            if not course_card.selected:
                course_card.configure(fg_color=["gray86", "gray17"])
        
        course_card.bind("<Enter>", on_enter)
        course_card.bind("<Leave>", on_leave)
        
        return course_card
    
    def _on_course_selection_changed(self, course_card, selected):
        """Handle course selection change."""
        course_card.selected = selected
        
        if selected:
            course_card.configure(fg_color=COLORS['primary'])
            self.selected_courses.append(course_card.course_data)
        else:
            course_card.configure(fg_color=["gray86", "gray17"])
            if course_card.course_data in self.selected_courses:
                self.selected_courses.remove(course_card.course_data)
        
        self._update_selection_info()
    
    def _on_select_all(self):
        """Handle select all button click."""
        all_selected = len(self.selected_courses) == len(self.filtered_courses)
        
        # Clear current selection
        self.selected_courses.clear()
        
        # Update all checkboxes
        for widget in self.courses_scrollable.winfo_children():
            if hasattr(widget, 'checkbox_var'):
                if all_selected:
                    widget.checkbox_var.set(False)
                    widget.selected = False
                    widget.configure(fg_color=["gray86", "gray17"])
                else:
                    widget.checkbox_var.set(True)
                    widget.selected = True
                    widget.configure(fg_color=COLORS['primary'])
                    self.selected_courses.append(widget.course_data)
        
        self._update_selection_info()
    
    def _on_enroll_selected(self):
        """Handle enroll selected courses."""
        if not self.selected_courses:
            messagebox.showwarning("No Selection", "Please select courses to enroll in")
            return
        
        # Confirm enrollment
        result = messagebox.askyesno(
            "Confirm Enrollment",
            f"Are you sure you want to enroll in {len(self.selected_courses)} selected courses?"
        )
        
        if result:
            self._enroll_in_courses(self.selected_courses)
    
    def _on_view_course(self, course):
        """Handle view course button click."""
        course_url = course.get('url', '')
        if course_url:
            try:
                import webbrowser
                webbrowser.open(course_url)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open course URL: {str(e)}")
        else:
            messagebox.showwarning("No URL", "Course URL not available")
    
    def _on_sort_changed(self, sort_option):
        """Handle sort option change."""
        if not self.filtered_courses:
            return
        
        try:
            if sort_option == "Rating":
                self.filtered_courses.sort(key=lambda x: float(x.get('rating', 0)), reverse=True)
            elif sort_option == "Duration":
                self.filtered_courses.sort(key=lambda x: self._parse_duration(x.get('duration', '')))
            elif sort_option == "Title":
                self.filtered_courses.sort(key=lambda x: x.get('title', '').lower())
            else:  # Recent
                pass  # Keep original order
            
            self._update_course_display()
            self._show_status(f"Sorted by {sort_option}")
        except Exception as e:
            logger.error(f"Error sorting courses: {str(e)}")
    
    def _parse_duration(self, duration_str):
        """Parse duration string to hours for sorting."""
        if not duration_str:
            return 0
        
        try:
            # Extract numbers from duration string
            import re
            numbers = re.findall(r'\d+', str(duration_str))
            if numbers:
                return float(numbers[0])
        except:
            pass
        
        return 0
    
    def _on_refresh(self):
        """Handle refresh button click."""
        self._on_fetch_courses()
    
    def _on_export_courses(self):
        """Handle export courses button click."""
        if not self.filtered_courses:
            messagebox.showwarning("No Courses", "No courses to export")
            return
        
        try:
            from tkinter import filedialog
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Export Courses"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.filtered_courses, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Export Success", f"Courses exported to {filename}")
                self._show_status(f"Exported {len(self.filtered_courses)} courses")
        except Exception as e:
            error_msg = f"Export failed: {str(e)}"
            logger.error(error_msg)
            messagebox.showerror("Export Error", error_msg)
    
    def _toggle_theme(self):
        """Toggle between light and dark theme."""
        current_mode = ctk.get_appearance_mode()
        
        if current_mode == "Dark":
            ctk.set_appearance_mode("Light")
            self.theme_button.configure(text="🌙")
        else:
            ctk.set_appearance_mode("Dark")
            self.theme_button.configure(text="☀️")
        
        self._show_status("Theme changed")
    
    def _update_selection_info(self):
        """Update selection information display."""
        count = len(self.selected_courses)
        
        if count == 0:
            self.selection_label.configure(text="No courses selected")
            self.enroll_selected_btn.configure(state="disabled")
            self.select_all_btn.configure(text="Select All")
        elif count == len(self.filtered_courses):
            self.selection_label.configure(text=f"All {count} courses selected")
            self.enroll_selected_btn.configure(state="normal")
            self.select_all_btn.configure(text="Deselect All")
        else:
            self.selection_label.configure(text=f"{count} of {len(self.filtered_courses)} courses selected")
            self.enroll_selected_btn.configure(state="normal")
            self.select_all_btn.configure(text="Select All")
    
    def _update_course_count(self):
        """Update course count display."""
        if not self.filtered_courses:
            self.course_count_label.configure(text="Ready to discover amazing courses")
        else:
            total = len(self.all_courses)
            filtered = len(self.filtered_courses)
            
            if total == filtered:
                self.course_count_label.configure(text=f"Showing {filtered} courses")
            else:
                self.course_count_label.configure(text=f"Showing {filtered} of {total} courses")
    
    def _on_enroll_all(self):
        """Handle enroll all button click."""
        if not self.filtered_courses:
            messagebox.showwarning("No Courses", "No courses available for enrollment")
            return
        
        if self.is_enrolling:
            return
        
        # Confirm enrollment
        result = messagebox.askyesno(
            "Confirm Enrollment",
            f"Are you sure you want to enroll in {len(self.filtered_courses)} courses?"
        )
        
        if result:
            self._enroll_in_courses(self.filtered_courses)
    
    def _enroll_in_courses(self, courses: List[Dict]):
        """Enroll in multiple courses."""
        if self.is_enrolling:
            return
        
        self.is_enrolling = True
        self.enroll_button.configure(text="Enrolling...", state="disabled")
        self._show_status("Starting enrollment process...", show_progress=True)
        
        # Start enrollment in separate thread
        thread = threading.Thread(target=self._enroll_courses_thread, args=(courses,))
        thread.daemon = True
        thread.start()
    
    def _enroll_courses_thread(self, courses: List[Dict]):
        """Enroll in courses in background thread."""
        try:
            # Import here to avoid circular imports
            from udemy_enroller import UdemyEnroller
            
            logger.info(f"Starting enrollment for {len(courses)} courses")
            
            # Create enroller with existing session
            enroller = UdemyEnroller()
            enroller.session = self.session
            enroller.user_info = self.user_info
            
            # Extract course URLs
            course_urls = [course.get('url') for course in courses if course.get('url')]
            
            if not course_urls:
                raise Exception("No valid course URLs found")
            
            # Enroll in courses
            results = enroller.enroll_in_multiple_courses(course_urls)
            
            # Update UI in main thread
            self.window.after(0, lambda: self._on_enrollment_complete(results))
            
        except Exception as e:
            error_msg = f"Error during enrollment: {str(e)}"
            logger.error(error_msg)
            self.window.after(0, lambda: self._on_enrollment_error(error_msg))
    
    def _on_enrollment_complete(self, results: Dict):
        """Handle successful completion of enrollment."""
        self.enrollment_results = results
        
        # Count successful enrollments
        successful = sum(1 for r in results.values() if r.get('success', False))
        total = len(results)
        
        self.is_enrolling = False
        self.enroll_button.configure(text="Enroll All", state="normal")
        
        status_msg = f"Enrollment complete: {successful}/{total} successful"
        self._show_status(status_msg, show_progress=False)
        
        # Show detailed results
        self._show_enrollment_results(results)
        
        logger.info(f"Enrollment complete: {successful}/{total} successful")
    
    def _on_enrollment_error(self, error_msg: str):
        """Handle enrollment error."""
        self.is_enrolling = False
        self.enroll_button.configure(text="Enroll All", state="normal")
        self._show_status(f"Enrollment error: {error_msg}", show_progress=False)
        
        messagebox.showerror("Enrollment Error", error_msg)
    
    def _show_enrollment_results(self, results: Dict):
        """Show detailed enrollment results in a dialog."""
        results_window = ctk.CTkToplevel(self.window)
        results_window.title("Enrollment Results")
        results_window.geometry("600x400")
        
        # Results text
        results_text = ctk.CTkTextbox(results_window, width=580, height=350)
        results_text.pack(padx=10, pady=10)
        
        # Format results
        text_content = "Enrollment Results:\n\n"
        
        for url, result in results.items():
            success = result.get('success', False)
            message = result.get('message', 'No message')
            
            status = "✓ SUCCESS" if success else "✗ FAILED"
            text_content += f"{status}: {message}\n"
            text_content += f"URL: {url}\n\n"
        
        results_text.insert("0.0", text_content)
        results_text.configure(state="disabled")
        
        # Close button
        close_btn = ctk.CTkButton(
            results_window,
            text="Close",
            command=results_window.destroy,
            width=100
        )
        close_btn.pack(pady=10)
    
    def _update_stats(self):
        """Update the statistics display with modern cards."""
        if not self.all_courses:
            self.total_stat.value_label.configure(text="0")
            self.filtered_stat.value_label.configure(text="0")
            self.success_stat.value_label.configure(text="0%")
            return
        
        total = len(self.all_courses)
        filtered = len(self.filtered_courses)
        
        # Update statistics
        self.total_stat.value_label.configure(text=str(total))
        self.filtered_stat.value_label.configure(text=str(filtered))
        
        # Calculate success rate from previous enrollment results
        if self.enrollment_results:
            successful = sum(1 for r in self.enrollment_results.values() if r.get('success', False))
            total_enrolled = len(self.enrollment_results)
            success_rate = (successful / total_enrolled * 100) if total_enrolled > 0 else 0
            self.success_stat.value_label.configure(text=f"{success_rate:.1f}%")
        else:
            self.success_stat.value_label.configure(text="0%")
        
        # Update course count display
        self._update_course_count()
    
    def _show_status(self, message: str, show_progress: bool = False, status_type: str = "info"):
        """Update status message with icon and optionally show progress bar."""
        # Status icons
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "loading": "⏳"
        }
        
        # Update status
        self.status_icon.configure(text=icons.get(status_type, "ℹ️"))
        self.status_label.configure(text=message)
        
        if show_progress:
            self.progress_bar.pack(side="right", padx=(SPACING['sm'], 0))
            self.progress_bar.set(0.5)  # Indeterminate progress
            self.status_icon.configure(text="⏳")
        else:
            self.progress_bar.pack_forget()
        
        # Log status message
        logger.info(f"Status: {message}")
        
        # Add to debug console if enabled
        if self.debug_mode:
            self._add_debug_message(f"STATUS [{status_type.upper()}]: {message}")
    
    def _toggle_debug(self):
        """Toggle debug mode and show/hide debug panel."""
        self.debug_mode = not self.debug_mode
        
        if self.debug_mode:
            self._show_debug_panel()
            self.debug_button.configure(fg_color=COLORS['warning'])
            self._show_status("Debug mode enabled", status_type="info")
        else:
            self._hide_debug_panel()
            self.debug_button.configure(fg_color="transparent")
            self._show_status("Debug mode disabled", status_type="info")
    
    def _show_debug_panel(self):
        """Show the debug panel."""
        if self.debug_panel is None:
            # Create debug panel
            self.debug_panel = ctk.CTkFrame(self.window, height=200, corner_radius=8)
            self.debug_panel.grid(row=3, column=0, sticky="ew", padx=SPACING['md'], pady=(0, SPACING['md']))
            self.debug_panel.grid_propagate(False)
            
            # Debug panel header
            debug_header = ctk.CTkFrame(self.debug_panel, fg_color="transparent", height=40)
            debug_header.pack(fill="x", padx=SPACING['md'], pady=(SPACING['sm'], 0))
            debug_header.pack_propagate(False)
            
            debug_title = ctk.CTkLabel(
                debug_header,
                text="🐛 Debug Console",
                font=FONTS['body_large'],
                text_color=COLORS['warning']
            )
            debug_title.pack(side="left", pady=SPACING['sm'])
            
            # Clear button
            clear_btn = ctk.CTkButton(
                debug_header,
                text="Clear",
                command=self._clear_debug,
                width=60,
                height=28,
                font=FONTS['label'],
                fg_color="transparent",
                hover_color=COLORS['surface_variant'],
                text_color=COLORS['on_surface_variant'],
                border_width=1,
                border_color=COLORS['outline']
            )
            clear_btn.pack(side="right", pady=SPACING['sm'])
            
            # Debug text area
            self.debug_text = ctk.CTkTextbox(
                self.debug_panel,
                height=150,
                font=("Courier New", 10),
                wrap="word"
            )
            self.debug_text.pack(fill="both", expand=True, padx=SPACING['md'], pady=(0, SPACING['md']))
            
            # Add initial debug info
            self._add_debug_message("Debug mode enabled")
            self._add_debug_message(f"Session: {'Active' if self.session else 'Not active'}")
            self._add_debug_message(f"User: {self.user_info.get('display_name', 'Unknown') if self.user_info else 'Not logged in'}")
        else:
            self.debug_panel.grid()
    
    def _hide_debug_panel(self):
        """Hide the debug panel."""
        if self.debug_panel:
            self.debug_panel.grid_remove()
    
    def _clear_debug(self):
        """Clear debug console."""
        if self.debug_text:
            self.debug_text.delete("0.0", "end")
    
    def _add_debug_message(self, message):
        """Add a message to the debug console."""
        if self.debug_text and self.debug_mode:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.debug_text.insert("end", f"[{timestamp}] {message}\n")
            self.debug_text.see("end")
    
    def _on_window_close(self):
        """Handle window close event."""
        if self.is_fetching or self.is_enrolling:
            if not messagebox.askokcancel("Quit", "Operations are in progress. Are you sure you want to quit?"):
                return
        
        self.window.destroy()
    
    def show(self):
        """Show the main window and start the GUI loop."""
        logger.info("Showing main GUI")
        self.window.mainloop()
    

def main():
    """
    Example usage of the MainGUI class.
    """
    # For testing without login
    gui = MainGUI()
    gui.show()


if __name__ == "__main__":
    main()
