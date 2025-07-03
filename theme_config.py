#!/usr/bin/env python3
"""
New Theme Configuration

Based on the new logo colors (purple and pink graduation theme),
this file contains the updated color scheme for the application.
"""

# New Color Scheme based on Education Logo (Purple & Pink)
NEW_COLORS = {
    # Primary colors from the logo
    'primary': "#6D4C7D",           # Purple from graduation cap
    'primary_hover': "#5A3F68",     # Darker purple
    'secondary': "#C86B85",         # Pink from discount badge
    'secondary_hover': "#B55A73",   # Darker pink
    
    # Accent colors
    'accent': "#8E44AD",            # Vibrant purple
    'accent_hover': "#7D3C98",      # Darker vibrant purple
    
    # Success and functional colors
    'success': "#27AE60",           # Educational green
    'success_hover': "#229954",     # Darker green
    'warning': "#F39C12",           # Academic orange
    'error': "#E74C3C",             # Alert red
    
    # Surface colors (neutral backgrounds)
    'surface': "#FFFFFF",           # Pure white
    'surface_variant': "#F8F9FA",   # Light gray
    'surface_container': "#F1F3F4", # Container background
    'outline': "#E1E4E8",           # Border color
    
    # Text colors
    'on_surface': "#2C3E50",        # Dark text
    'on_surface_variant': "#6C757D", # Secondary text
    'on_primary': "#FFFFFF",        # Text on primary
    'on_secondary': "#FFFFFF",      # Text on secondary
    
    # Educational theme specific
    'book_spine': "#34495E",        # Book spine color
    'page': "#FEFEFE",              # Page white
    'highlight': "#F7DC6F",         # Highlight yellow
    
    # Gradient colors for modern UI
    'gradient_start': "#6D4C7D",    # Purple start
    'gradient_end': "#C86B85",      # Pink end
}

# Dark mode variations
DARK_COLORS = {
    'primary': "#8E7CC3",           # Lighter purple for dark mode
    'primary_hover': "#7B6BAE",     # Darker version
    'secondary': "#D687A1",         # Lighter pink for dark mode
    'secondary_hover': "#C47A92",   # Darker version
    
    'surface': "#1A1A1A",           # Dark background
    'surface_variant': "#2D2D2D",   # Slightly lighter dark
    'surface_container': "#363636", # Container dark background
    'outline': "#404040",           # Dark border
    
    'on_surface': "#E8E8E8",        # Light text on dark
    'on_surface_variant': "#B0B0B0", # Secondary light text
    'on_primary': "#FFFFFF",
    'on_secondary': "#FFFFFF",
}

# Typography settings (education-focused)
FONTS = {
    'display': ("Segoe UI", 32, "bold"),        # Large headings
    'headline': ("Segoe UI", 24, "bold"),       # Section headers
    'title': ("Segoe UI", 18, "bold"),          # Card titles
    'title_medium': ("Segoe UI", 16, "bold"),   # Medium titles
    'body_large': ("Segoe UI", 14),             # Large body text
    'body': ("Segoe UI", 12),                   # Regular body text
    'body_small': ("Segoe UI", 11),             # Small body text
    'caption': ("Segoe UI", 10),                # Captions
    'button': ("Segoe UI", 12, "bold"),         # Button text
    'mono': ("Consolas", 10),                   # Monospace for code
}

# Animation and spacing settings
SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 16,
    'lg': 24,
    'xl': 32,
    'xxl': 48
}

RADIUS = {
    'small': 4,
    'medium': 8,
    'large': 12,
    'extra_large': 16
}

# Educational theme specific settings
EDUCATION_THEME = {
    'course_card_radius': 12,
    'button_height': 36,
    'icon_size': 24,
    'avatar_size': 40,
    'card_padding': 16,
    'section_spacing': 24
}

def get_color_scheme(dark_mode=False):
    """
    Get the appropriate color scheme based on theme mode.
    
    Args:
        dark_mode (bool): Whether to use dark mode colors
        
    Returns:
        dict: Color scheme dictionary
    """
    base_colors = NEW_COLORS.copy()
    
    if dark_mode:
        # Update with dark mode specific colors
        base_colors.update(DARK_COLORS)
    
    return base_colors

def apply_education_theme():
    """
    Apply the education-themed color scheme to customtkinter.
    This should be called before creating any UI elements.
    """
    import customtkinter as ctk
    
    # Set the custom color theme
    ctk.set_appearance_mode("system")
    
    # Create custom theme
    custom_theme = {
        "CTk": {
            "fg_color": [NEW_COLORS['surface'], DARK_COLORS['surface']]
        },
        "CTkToplevel": {
            "fg_color": [NEW_COLORS['surface'], DARK_COLORS['surface']]
        },
        "CTkFrame": {
            "corner_radius": RADIUS['medium'],
            "border_width": 0,
            "fg_color": [NEW_COLORS['surface_variant'], DARK_COLORS['surface_variant']],
            "top_fg_color": [NEW_COLORS['surface_container'], DARK_COLORS['surface_container']],
            "border_color": [NEW_COLORS['outline'], DARK_COLORS['outline']]
        },
        "CTkButton": {
            "corner_radius": RADIUS['medium'],
            "border_width": 0,
            "fg_color": [NEW_COLORS['primary'], DARK_COLORS['primary']],
            "hover_color": [NEW_COLORS['primary_hover'], DARK_COLORS['primary_hover']],
            "border_color": [NEW_COLORS['primary'], DARK_COLORS['primary']],
            "text_color": [NEW_COLORS['on_primary'], DARK_COLORS['on_primary']],
            "text_color_disabled": [NEW_COLORS['on_surface_variant'], DARK_COLORS['on_surface_variant']]
        },
        "CTkLabel": {
            "corner_radius": 0,
            "fg_color": "transparent",
            "text_color": [NEW_COLORS['on_surface'], DARK_COLORS['on_surface']]
        },
        "CTkEntry": {
            "corner_radius": RADIUS['medium'],
            "border_width": 1,
            "fg_color": [NEW_COLORS['surface'], DARK_COLORS['surface']],
            "border_color": [NEW_COLORS['outline'], DARK_COLORS['outline']],
            "text_color": [NEW_COLORS['on_surface'], DARK_COLORS['on_surface']],
            "placeholder_text_color": [NEW_COLORS['on_surface_variant'], DARK_COLORS['on_surface_variant']]
        }
    }
    
    return custom_theme

if __name__ == "__main__":
    # Test the color scheme
    print("🎨 New Education Theme Color Palette")
    print("="*50)
    
    colors = get_color_scheme(dark_mode=False)
    
    print("📚 Primary Colors:")
    print(f"  Primary: {colors['primary']}")
    print(f"  Secondary: {colors['secondary']}")
    print(f"  Accent: {colors['accent']}")
    
    print("\n🎯 Functional Colors:")
    print(f"  Success: {colors['success']}")
    print(f"  Warning: {colors['warning']}")
    print(f"  Error: {colors['error']}")
    
    print("\n🏗️ Surface Colors:")
    print(f"  Surface: {colors['surface']}")
    print(f"  Surface Variant: {colors['surface_variant']}")
    print(f"  Outline: {colors['outline']}")
    
    print("\n✨ Educational Theme Ready!")
