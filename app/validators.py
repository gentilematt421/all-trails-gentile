"""
Validators Module

This module contains validation logic for user inputs and business rules.
It follows single responsibility principle by focusing only on validation concerns.
"""

import re
from typing import Tuple


class URLValidator:
    """Validates URLs and URL-related inputs."""
    
    @staticmethod
    def is_alltrails_url(url: str) -> bool:
        """
        Check if the provided URL is a valid AllTrails URL.
        
        Args:
            url: The URL to validate
            
        Returns:
            True if it's a valid AllTrails URL, False otherwise
        """
        if not url or not isinstance(url, str):
            return False
        
        # Check if it contains alltrails.com
        return "alltrails.com" in url.lower()
    
    @staticmethod
    def is_valid_url_format(url: str) -> bool:
        """
        Check if the URL has a valid format.
        
        Args:
            url: The URL to validate
            
        Returns:
            True if it's a valid URL format, False otherwise
        """
        if not url or not isinstance(url, str):
            return False
        
        # Basic URL pattern validation
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(url_pattern.match(url))


class InputValidator:
    """Validates user inputs and provides validation results."""
    
    @staticmethod
    def validate_hike_url(url: str) -> Tuple[bool, str]:
        """
        Validate a hike URL input.
        
        Args:
            url: The URL to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not url:
            return False, "Please enter a URL to scrape."
        
        if not URLValidator.is_alltrails_url(url):
            return False, "Please enter a valid AllTrails URL (should contain 'alltrails.com')"
        
        if not URLValidator.is_valid_url_format(url):
            return False, "Please enter a valid URL format."
        
        return True, "" 