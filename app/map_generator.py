"""
Map Generator Module

This module handles the creation of interactive maps showing trail locations
and places mentioned in the itinerary.
"""

import streamlit as st
import folium
from folium import Popup, Marker, Icon
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import re
from typing import Dict, List, Optional, Tuple
import time


class MapGenerator:
    """Handles generation of interactive maps for hikes and itineraries."""
    
    def __init__(self):
        """Initialize the map generator with geocoder."""
        self.geolocator = Nominatim(user_agent="alltrails_mapper")
    
    def create_daily_map(self, hike_data: Dict, itinerary_text: str) -> Optional[folium.Map]:
        """
        Create an interactive map showing the trail and itinerary places.
        
        Args:
            hike_data: Dictionary containing hike information
            itinerary_text: The generated itinerary text
            
        Returns:
            Folium map object or None if creation fails
        """
        try:
            # Get trail coordinates
            trail_location = self._get_trail_coordinates(hike_data)
            if not trail_location:
                st.error("Could not find coordinates for the trail location.")
                return None
            
            # Create the base map centered on the trail
            map_obj = folium.Map(
                location=trail_location,
                zoom_start=12,
                tiles='OpenStreetMap'
            )
            
            # Add trail marker
            self._add_trail_marker(map_obj, hike_data, trail_location)
            
            # Extract and add places from itinerary
            places = self._extract_places_from_itinerary(itinerary_text)
            self._add_place_markers(map_obj, places)
            
            return map_obj
            
        except Exception as e:
            st.error(f"Error creating map: {str(e)}")
            return None
    
    def _get_trail_coordinates(self, hike_data: Dict) -> Optional[Tuple[float, float]]:
        """Get coordinates for the trail location."""
        location = hike_data.get('location', '')
        if not location:
            return None
        
        try:
            # Try to geocode the location
            location_obj = self.geolocator.geocode(location, timeout=10)
            if location_obj:
                return (location_obj.latitude, location_obj.longitude)
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            st.warning(f"Geocoding service unavailable: {str(e)}")
        
        return None
    
    def _add_trail_marker(self, map_obj: folium.Map, hike_data: Dict, coordinates: Tuple[float, float]):
        """Add the trail marker to the map."""
        hike_name = hike_data.get('name', 'Unknown Trail')
        location = hike_data.get('location', 'Unknown Location')
        difficulty = hike_data.get('difficulty', 'Unknown')
        length = hike_data.get('length', 'Unknown')
        
        # Create popup content
        popup_content = f"""
        <div style="width: 250px;">
            <h4>🥾 {hike_name}</h4>
            <p><strong>Location:</strong> {location}</p>
            <p><strong>Difficulty:</strong> {difficulty}</p>
            <p><strong>Length:</strong> {length}</p>
        </div>
        """
        
        # Add trail marker with hiking icon
        folium.Marker(
            coordinates,
            popup=Popup(popup_content, max_width=300),
            icon=Icon(color='green', icon='tree', prefix='fa'),
            tooltip=f"🥾 {hike_name}"
        ).add_to(map_obj)
    
    def _extract_places_from_itinerary(self, itinerary_text: str) -> List[Dict]:
        """Extract places and addresses from the itinerary text."""
        places = []
        
        # Look for "Places Mentioned" section
        if "Places Mentioned" in itinerary_text:
            # Find the start of the Places Mentioned section
            start_index = itinerary_text.find("Places Mentioned")
            if start_index != -1:
                # Get the text from "Places Mentioned" onwards
                places_section = itinerary_text[start_index:]
                
                # Split into lines and look for bulleted items
                lines = places_section.split('\n')
                
                for line in lines:
                    line = line.strip()
                    # Look for lines that start with bullet points and contain a dash
                    if (line.startswith('•') or line.startswith('-') or line.startswith('*')) and ' - ' in line:
                        # Split on the first " - " to separate place name from address
                        parts = line.split(' - ', 1)
                        if len(parts) == 2:
                            place_name = parts[0].strip()
                            address = parts[1].strip()
                            
                            # Clean up the place name (remove bullet points)
                            place_name = re.sub(r'^[\s•\-\*→▶▸▹▻▪▫◦‣⁃]+', '', place_name)
                            place_name = place_name.strip()
                            
                            # Clean up the address
                            address = address.strip()
                            
                            # Validate that we have meaningful content
                            if (place_name and address and 
                                len(place_name) > 2 and len(address) > 10 and
                                not place_name.lower() in ['none', 'unknown', 'n/a']):
                                
                                places.append({
                                    'name': place_name,
                                    'address': address
                                })
        
        return places
    
    def _add_place_markers(self, map_obj: folium.Map, places: List[Dict]):
        """Add markers for all places mentioned in the itinerary."""
        for i, place in enumerate(places):
            try:
                # Geocode the address
                location_obj = self.geolocator.geocode(place['address'], timeout=10)
                if location_obj:
                    coordinates = (location_obj.latitude, location_obj.longitude)
                    
                    # Create popup content
                    popup_content = f"""
                    <div style="width: 200px;">
                        <h5>📍 {place['name']}</h5>
                        <p><strong>Address:</strong><br>{place['address']}</p>
                    </div>
                    """
                    
                    # Add marker with consistent icon
                    folium.Marker(
                        coordinates,
                        popup=Popup(popup_content, max_width=250),
                        icon=Icon(color='blue', icon='map-marker', prefix='fa'),
                        tooltip=f"📍 {place['name']}"
                    ).add_to(map_obj)
                    
                    # Add small delay to avoid overwhelming the geocoding service
                    time.sleep(0.1)
                    
            except (GeocoderTimedOut, GeocoderUnavailable) as e:
                st.warning(f"Could not geocode address for {place['name']}: {str(e)}")
            except Exception as e:
                st.warning(f"Error adding marker for {place['name']}: {str(e)}")


class MapDisplay:
    """Handles the display of maps in the Streamlit interface."""
    
    @staticmethod
    def render_map_page(hike_data: Optional[Dict] = None, itinerary_text: Optional[str] = None):
        """Render the map page content."""
        st.header("🗺️ Daily Map")
        st.markdown("Interactive map showing your hike location and all places mentioned in your itinerary.")
        
        if not hike_data:
            st.warning("⚠️ No hike data found!")
            st.markdown("""
            To view the daily map, you need to:
            
            1. **Go to the Home page** and enter an AllTrails hike URL
            2. **Navigate to the Hike Scraper page** and scrape the hike data
            3. **Generate an itinerary** on the Build A Day Around My Hike page
            4. **Return here** to see the interactive map
            
            The map will show your trail location and all the places mentioned in your itinerary.
            """)
            return
        
        if not itinerary_text:
            st.warning("⚠️ No itinerary found!")
            st.markdown("""
            To view the daily map, you need to generate an itinerary first.
            
            Go to the **🏔️ Build A Day Around My Hike** page and generate your perfect day itinerary.
            """)
            return
        
        # Show hike summary
        st.success(f"🗺️ Mapping: **{hike_data.get('name', 'Unknown Trail')}**")
        
        # Extract places and show them
        map_generator = MapGenerator()
        places = map_generator._extract_places_from_itinerary(itinerary_text)
        
        # Display Places Mentioned section
        if places:
            st.subheader("📍 Places Mentioned in Your Itinerary")
            st.markdown("These are the places we found in your itinerary that will be shown on the map:")
            
            for i, place in enumerate(places, 1):
                st.markdown(f"**{i}.** **{place['name']}** - {place['address']}")
            
            st.markdown("---")
        else:
            st.warning("⚠️ No specific places with addresses were found in your itinerary.")
            st.markdown("The map will show your hike location, but no additional places were detected.")
            st.markdown("---")
        
        # Create and display the map
        with st.spinner("🗺️ Generating your interactive map..."):
            map_obj = map_generator.create_daily_map(hike_data, itinerary_text)
            
            if map_obj:
                # Display the map
                st.components.v1.html(map_obj._repr_html_(), height=600)
                
                st.info("💡 **Tip:** Click on any marker to see details about that location!")
            else:
                st.error("Failed to generate map. Please try again.") 