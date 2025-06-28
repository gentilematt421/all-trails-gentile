"""
Main Application Entry Point - Home Page

This module serves as the home page for the AllTrails Data Project.
It provides an introduction and URL input that can be used across pages.
"""

import streamlit as st
from ui_components import InputComponents


def configure_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="AllTrails Senior Product Analyst App",
        layout="centered"
    )


def render_header():
    """Render the application header."""
    st.title("I want to work at AllTrails! 🥾🌲")
    st.markdown(
        "This is a personal project to showcase my data skills, "
        "product thinking, and love for the outdoors."
    )


def render_home_content():
    """Render the home page content."""
    st.header("Welcome to Your AllTrails Adventure! 🏔️")
    
    st.markdown("""
    This app helps you explore and plan your hiking adventures. Use the navigation 
    on the left to access different features:
    
    **🌲 Hike Scraper** - Extract detailed information from AllTrails hike pagec<br>
    **🏔️ Build A Day Around My Hike** - Plan the perfect day around your trail with a generated daily intinerary
    
    Start by entering an AllTrails URL below to get hike information!
    """)
    
    # URL input from user
    st.markdown("Enter an AllTrails hike URL to get started:")
    
    # Store URL in session state for sharing across pages
    url = InputComponents.get_hike_url()
    
    if url:
        # Store the URL in session state
        st.session_state['hike_url'] = url
        st.success(f"URL entered: {url}")
        st.info("Navigate to the '🌲 Hike Scraper' page to extract hike data!")
    else:
        # Clear the URL from session state if no URL is entered
        if 'hike_url' in st.session_state:
            del st.session_state['hike_url']


def main():
    """Main application function that orchestrates the home page."""
    configure_page()
    render_header()
    render_home_content()


if __name__ == "__main__":
    main()


