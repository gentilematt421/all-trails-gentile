"""
UI Components Module

This module contains all Streamlit UI components and display logic.
It follows single responsibility principle by focusing only on presentation
and user interface concerns.
"""

import streamlit as st
import re
from typing import Optional
from scraper import HikeData


def clean_location_string(location: str) -> str:
    """
    Clean location string by removing bullet points and other unwanted characters.
    
    Args:
        location: The raw location string from scraping
        
    Returns:
        Cleaned location string
    """
    if not location:
        return ""
    
    # Remove bullet points, dashes, and other common list markers
    cleaned = re.sub(r'^[\s\·\•\-\*→▶▸▹▻▪▫◦‣⁃]+', '', location.strip())
    
    # Remove any remaining leading/trailing whitespace
    cleaned = cleaned.strip()
    
    return cleaned


class HikeDataDisplay:
    """Handles the display of hike data in the Streamlit interface."""
    
    @staticmethod
    def render_hike_data(hike_data: HikeData) -> None:
        """
        Render hike data in a clean, organized format.
        
        Args:
            hike_data: The HikeData object to display
        """
        st.success("Successfully scraped hike data!")
        
        # Display basic information in columns
        col1, col2 = st.columns(2)
        
        with col1:
            HikeDataDisplay._render_basic_info(hike_data)
        
        with col2:
            HikeDataDisplay._render_ratings_info(hike_data)
        
        # Display description if available
        if hike_data.description:
            st.subheader("📝 Description")
            st.write(hike_data.description)
        
        # Display features if available
        if hike_data.features:
            HikeDataDisplay._render_features(hike_data.features)
        
        # Show raw data for debugging
        HikeDataDisplay._render_debug_data(hike_data)
    
    @staticmethod
    def _render_basic_info(hike_data: HikeData) -> None:
        """Render basic hike information."""
        st.subheader("📋 Basic Information")
        
        if hike_data.name:
            st.write(f"**Trail Name:** {hike_data.name}")
        if hike_data.location:
            cleaned_location = clean_location_string(hike_data.location)
            if cleaned_location:
                st.write(f"**Location:** {cleaned_location}")
        if hike_data.difficulty:
            st.write(f"**Difficulty:** {hike_data.difficulty}")
        if hike_data.length:
            st.write(f"**Length:** {hike_data.length}")
        if hike_data.elevation_gain:
            st.write(f"**Elevation Gain:** {hike_data.elevation_gain}")
        if hike_data.route_type:
            st.write(f"**Route Type:** {hike_data.route_type}")
    
    @staticmethod
    def _render_ratings_info(hike_data: HikeData) -> None:
        """Render ratings and reviews information."""
        st.subheader("⭐ Ratings & Reviews")
        
        if hike_data.rating:
            st.write(f"**Rating:** {hike_data.rating}")
        if hike_data.reviews_count:
            st.write(f"**Reviews:** {hike_data.reviews_count}")
    
    @staticmethod
    def _render_features(features: list) -> None:
        """Render features and tags."""
        st.subheader("🏷️ Features & Tags")
        for feature in features:
            st.write(f"• {feature}")
    
    @staticmethod
    def _render_debug_data(hike_data: HikeData) -> None:
        """Render raw data for debugging purposes."""
        with st.expander("🔍 Raw Data (for debugging)"):
            st.json({
                'name': hike_data.name,
                'location': hike_data.location,
                'difficulty': hike_data.difficulty,
                'length': hike_data.length,
                'elevation_gain': hike_data.elevation_gain,
                'route_type': hike_data.route_type,
                'rating': hike_data.rating,
                'reviews_count': hike_data.reviews_count,
                'description': hike_data.description,
                'features': hike_data.features
            })


class InputComponents:
    """Handles user input components."""
    
    @staticmethod
    def get_hike_url() -> str:
        """Get hike URL from user input."""
        return st.text_input(
            "Enter AllTrails hike URL:",
            placeholder="https://www.alltrails.com/trail/..."
        )
    
    @staticmethod
    def get_scrape_button() -> bool:
        """Get scrape button state."""
        return st.button("Scrape Hike Data")


class ErrorDisplay:
    """Handles error message display."""
    
    @staticmethod
    def show_scraping_error(error_message: str) -> None:
        """Display scraping error message."""
        st.error(f"Error scraping the page: {error_message}")
        
        # Provide specific guidance for 403 errors
        if "403" in error_message or "Access denied" in error_message:
            st.warning("🚫 **AllTrails is blocking automated requests**")
            st.markdown("""
            **This is common and can happen for several reasons:**
            
            🔄 **Try these solutions:**
            1. **Wait a few minutes** and try again
            2. **Use a different AllTrails URL** - some pages may be less protected
            3. **Try during off-peak hours** (early morning or late evening)
            4. **Check if the URL is accessible** in your regular browser
            
            💡 **Alternative approach:**
            - Copy the hike information manually from AllTrails
            - Use the data to create your itinerary manually
            
            **Note:** AllTrails occasionally blocks automated access to protect their servers. 
            This is normal behavior and not a problem with your app.
            """)
    
    @staticmethod
    def show_invalid_url_error() -> None:
        """Display invalid URL error message."""
        st.error("Please enter a valid AllTrails URL (should contain 'alltrails.com')")
    
    @staticmethod
    def show_no_url_warning() -> None:
        """Display warning when no URL is provided."""
        st.warning("Please enter a URL to scrape.")
    
    @staticmethod
    def show_scraping_failed_error() -> None:
        """Display error when scraping fails."""
        st.error("Failed to scrape data from the URL. Please check if the URL is correct and the page is accessible.") 