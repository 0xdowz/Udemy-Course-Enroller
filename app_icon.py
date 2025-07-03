#!/usr/bin/env python3
"""
App Icon Generator

This module generates a simple app icon for the Udemy Course Enroller application.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import logging

logger = logging.getLogger(__name__)

def create_app_icon(size=(256, 256), output_path="app_icon.png"):
    """
    Create a simple app icon.
    
    Args:
        size: Tuple of (width, height) for the icon
        output_path: Path to save the icon
    """
    try:
        # Create a new image with transparent background
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Define colors
        primary_color = (31, 83, 141)  # Blue
        secondary_color = (255, 255, 255)  # White
        accent_color = (45, 125, 50)  # Green
        
        # Draw background circle
        margin = 20
        draw.ellipse([margin, margin, size[0] - margin, size[1] - margin], 
                    fill=primary_color)
        
        # Draw graduation cap (simplified)
        center_x, center_y = size[0] // 2, size[1] // 2
        
        # Cap base
        cap_width = size[0] * 0.4
        cap_height = size[1] * 0.15
        cap_x = center_x - cap_width // 2
        cap_y = center_y - cap_height // 2
        
        draw.rectangle([cap_x, cap_y, cap_x + cap_width, cap_y + cap_height], 
                      fill=secondary_color)
        
        # Cap top
        top_width = cap_width * 1.2
        top_height = cap_height * 0.3
        top_x = center_x - top_width // 2
        top_y = cap_y - top_height
        
        draw.rectangle([top_x, top_y, top_x + top_width, top_y + top_height], 
                      fill=secondary_color)
        
        # Tassel
        tassel_x = center_x + cap_width // 2
        tassel_y = cap_y
        draw.line([tassel_x, tassel_y, tassel_x + 15, tassel_y + 30], 
                 fill=accent_color, width=3)
        draw.ellipse([tassel_x + 10, tassel_y + 25, tassel_x + 20, tassel_y + 35], 
                    fill=accent_color)
        
        # Save the icon
        img.save(output_path, 'PNG')
        logger.info(f"App icon created successfully: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error creating app icon: {str(e)}")
        return False

def main():
    """Generate app icon."""
    if create_app_icon():
        print("App icon generated successfully!")
    else:
        print("Failed to generate app icon")

if __name__ == "__main__":
    main()
