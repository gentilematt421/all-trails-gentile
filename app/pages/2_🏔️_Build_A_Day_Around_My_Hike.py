"""
Build A Day Around My Hike Page

This page generates personalized daily itineraries using ChatGPT based on hike data.
"""

import streamlit as st
import sys
import os

# Add the parent directory to the path so we can import from app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from itinerary_generator import ItineraryGenerator, ItineraryDisplay


def render_build_day_page():
    """Render the build a day around hike page content."""
    st.header("🏔️ Build A Day Around My Hike")
    st.markdown("Generate a personalized daily itinerary for your perfect hiking adventure!")
    
    # Check if we have hike data from scraping
    if 'hike_data' not in st.session_state:
        st.warning("⚠️ No hike data found!")
        st.markdown("""
        To generate a personalized itinerary, you need to:
        
        1. **Go to the Home page** and enter an AllTrails hike URL
        2. **Navigate to the Hike Scraper page** and scrape the hike data
        3. **Return here** to generate your perfect day itinerary
        
        The itinerary will be customized based on your hike's details like difficulty, 
        length, location, and your personal preferences.
        """)
        return
    
    # Display the hike we're planning around
    hike_data = st.session_state['hike_data']
    st.success(f"🎯 Planning around: **{hike_data.get('name', 'Unknown Trail')}**")
    
    # Show hike summary
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Location:** {hike_data.get('location', 'Unknown')}")
        st.write(f"**Difficulty:** {hike_data.get('difficulty', 'Unknown')}")
        st.write(f"**Length:** {hike_data.get('length', 'Unknown')}")
    
    with col2:
        st.write(f"**Elevation Gain:** {hike_data.get('elevation_gain', 'Unknown')}")
        st.write(f"**Rating:** {hike_data.get('rating', 'Unknown')}")
        st.write(f"**Features:** {', '.join(hike_data.get('features', []))}")
    
    st.markdown("---")
    
    # Check for OpenAI API key
    api_key = st.secrets.get("OPENAI_API_KEY", None)
    if not api_key:
        st.error("⚠️ OpenAI API key not configured!")
        st.markdown("""
        To use the itinerary generator, you need to configure your OpenAI API key.
        
        **For development/testing:**
        - Create a `.streamlit/secrets.toml` file in your project root
        - Add: `OPENAI_API_KEY = "your-api-key-here"`
        
        **For production:**
        - Set the `OPENAI_API_KEY` environment variable
        """)
        return
    
    # Render the itinerary form
    user_preferences = ItineraryDisplay.render_itinerary_form(hike_data)
    
    # Generate itinerary if form was submitted
    if user_preferences is not None:
        with st.spinner("🤖 AI is crafting your perfect day..."):
            generator = ItineraryGenerator(api_key)
            itinerary = generator.generate_itinerary(hike_data, user_preferences)
            
            if itinerary:
                # Store the itinerary in session state
                st.session_state['generated_itinerary'] = itinerary
                ItineraryDisplay.render_itinerary(itinerary)
            else:
                st.error("Failed to generate itinerary. Please try again.")
    
    # Display previously generated itinerary if available
    elif 'generated_itinerary' in st.session_state:
        st.markdown("### 📋 Previously Generated Itinerary")
        ItineraryDisplay.render_itinerary(st.session_state['generated_itinerary'])


# Main page content
render_build_day_page() 