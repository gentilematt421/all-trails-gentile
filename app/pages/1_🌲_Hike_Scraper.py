"""
Hike Scraper Page

This page contains the AllTrails hike scraper functionality.
"""

import streamlit as st
import sys
import os

# Add the parent directory to the path so we can import from app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper import AllTrailsScraper, ScrapingError
from ui_components import HikeDataDisplay, ErrorDisplay
from validators import InputValidator


def render_scraper_page():
    """Render the scraper page content."""
    st.header("🌲 AllTrails Hike Scraper")
    
    # Check if URL is available in session state
    if 'hike_url' not in st.session_state or not st.session_state['hike_url']:
        st.warning("⚠️ No hike URL found!")
        st.markdown("""
        Please go back to the **Home** page and enter an AllTrails hike URL first.
        
        Once you've entered a URL on the main page, return here to scrape the hike data.
        """)
        return
    
    # Display the URL being used
    url = st.session_state['hike_url']
    st.success(f"📋 Using URL from main page: `{url}`")
    
    # Instructions for the user
    st.markdown("""
    ### 📝 Instructions
    Press the button below to grab information about the hike you entered on the main page.
    
    The scraper will extract details like trail name, difficulty, length, elevation gain, 
    ratings, reviews, and more from the AllTrails page.
    """)
    
    # Scrape button
    if st.button("🔍 Scrape Hike Data", type="primary"):
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
            st.error("No URL found. Please go back to the main page and enter a URL.")
        else:
            st.error(f"Invalid URL: {error_message}")
        return
    
    # Perform scraping
    with st.spinner("Scraping hike information..."):
        try:
            scraper = AllTrailsScraper()
            hike_data = scraper.scrape_hike(url)
            
            if hike_data:
                # Store hike data in session state for use in other pages
                st.session_state['hike_data'] = {
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
                }
                
                HikeDataDisplay.render_hike_data(hike_data)
                
                # Show success message with next steps
                st.success("✅ Hike data successfully scraped and saved!")
                st.info("🎯 Ready to generate an itinerary? Navigate to the '🏔️ Build A Day Around My Hike' page!")
                
            else:
                ErrorDisplay.show_scraping_failed_error()
                
        except ScrapingError as e:
            ErrorDisplay.show_scraping_error(str(e))
        except Exception as e:
            ErrorDisplay.show_scraping_error(f"Unexpected error: {str(e)}")


# Main page content
render_scraper_page() 