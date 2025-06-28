"""
Hike Scraper Page

This page contains the AllTrails hike scraper functionality.
"""

import streamlit as st
from ..scraper import AllTrailsScraper, ScrapingError
from ..ui_components import HikeDataDisplay, InputComponents, ErrorDisplay
from ..validators import InputValidator


def render_scraper_page():
    """Render the scraper page content."""
    st.header("🌲 AllTrails Hike Scraper")
    st.markdown("Enter an AllTrails hike URL to extract key information about the trail.")
    
    # Get user input
    url = InputComponents.get_hike_url()
    scrape_button = InputComponents.get_scrape_button()
    
    if scrape_button:
        process_scraping_request(url)


def process_scraping_request(url: str):
    """
    Process the scraping request for the given URL.
    
    Args:
        url: The AllTrails URL to scrape
    """
    # Validate input
    is_valid, error_message = InputValidator.validate_hike_url(url)
    
    if not is_valid:
        if "Please enter a URL" in error_message:
            ErrorDisplay.show_no_url_warning()
        else:
            ErrorDisplay.show_invalid_url_error()
        return
    
    # Perform scraping
    with st.spinner("Scraping hike information..."):
        try:
            scraper = AllTrailsScraper()
            hike_data = scraper.scrape_hike(url)
            
            if hike_data:
                HikeDataDisplay.render_hike_data(hike_data)
            else:
                ErrorDisplay.show_scraping_failed_error()
                
        except ScrapingError as e:
            ErrorDisplay.show_scraping_error(str(e))
        except Exception as e:
            ErrorDisplay.show_scraping_error(f"Unexpected error: {str(e)}")


# Main page content
render_scraper_page() 