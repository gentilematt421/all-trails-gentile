"""
Daily Map Page

This page displays an interactive map showing the hike location and all places
mentioned in the generated itinerary.
"""

import streamlit as st
import sys
import os

# Add the parent directory to the path so we can import from app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from map_generator import MapDisplay


def render_daily_map_page():
    """Render the daily map page content."""
    # Get data from session state
    hike_data = st.session_state.get('hike_data', None)
    itinerary_text = st.session_state.get('generated_itinerary', None)
    
    # Render the map page
    MapDisplay.render_map_page(hike_data, itinerary_text)


# Main page content
render_daily_map_page() 