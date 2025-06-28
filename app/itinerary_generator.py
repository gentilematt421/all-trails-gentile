"""
Itinerary Generator Module

This module handles the generation of daily itineraries using ChatGPT
based on hike data and pre-canned prompts.
"""

import openai
import streamlit as st
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ItineraryRequest:
    """Data class for itinerary generation requests."""
    hike_name: str
    location: str
    difficulty: str
    length: str
    elevation_gain: str
    rating: str
    description: str
    features: list
    user_preferences: str = ""


class ItineraryGenerator:
    """Handles itinerary generation using ChatGPT."""
    
    def __init__(self, api_key: str):
        """Initialize the generator with OpenAI API key."""
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate_itinerary(self, hike_data: Dict[str, Any], user_preferences: str = "") -> Optional[str]:
        """
        Generate a daily itinerary based on hike data.
        
        Args:
            hike_data: Dictionary containing hike information
            user_preferences: Optional user preferences for the itinerary
            
        Returns:
            Generated itinerary text or None if generation fails
        """
        try:
            # Create itinerary request
            request = ItineraryRequest(
                hike_name=hike_data.get('name', ''),
                location=hike_data.get('location', ''),
                difficulty=hike_data.get('difficulty', ''),
                length=hike_data.get('length', ''),
                elevation_gain=hike_data.get('elevation_gain', ''),
                rating=hike_data.get('rating', ''),
                description=hike_data.get('description', ''),
                features=hike_data.get('features', []),
                user_preferences=user_preferences
            )
            
            # Generate the prompt
            prompt = self._create_itinerary_prompt(request)
            
            # Call ChatGPT
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error generating itinerary: {str(e)}")
            return None
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for ChatGPT."""
        return """You are an expert outdoor adventure planner and local guide. You specialize in creating 
        perfect day itineraries around hiking trails. You have extensive knowledge of outdoor activities, 
        local attractions, restaurants, and practical planning considerations.
        
        Your responses should be:
        - Well-structured and easy to follow
        - Practical and realistic for the given hike
        - Include timing estimates
        - Consider the hike's difficulty and duration
        - Include local recommendations when possible
        - Focus on creating a memorable outdoor experience
        
        Format your response in a clear, organized way with sections for different parts of the day."""
    
    def _create_itinerary_prompt(self, request: ItineraryRequest) -> str:
        """Create the user prompt for itinerary generation."""
        
        # Build hike information section
        hike_info = f"""
Hike Information:
- Trail Name: {request.hike_name}
- Location: {request.location}
- Difficulty: {request.difficulty}
- Length: {request.length}
- Elevation Gain: {request.elevation_gain}
- Rating: {request.rating}
- Description: {request.description}
- Features: {', '.join(request.features) if request.features else 'None specified'}
"""
        
        # Build the main prompt
        prompt = f"""
Please create a comprehensive daily itinerary for a perfect day centered around this hike:

{hike_info}

{f"Additional Preferences: {request.user_preferences}" if request.user_preferences else ""}

Please include:
1. **Pre-Hike Preparation** (what to bring, when to start, parking info)
2. **Morning Activities** (breakfast, travel to trailhead, any pre-hike activities)
3. **Hike Details** (timing, what to expect, safety considerations)
4. **Post-Hike Activities** (lunch/dinner recommendations, relaxation, local attractions)
5. **Evening Plans** (dinner, accommodation if needed, sunset viewing spots)
6. **Practical Tips** (weather considerations, gear recommendations, local insights)

Make the itinerary realistic based on the hike's difficulty and duration. Consider the location and suggest local favorites when possible. Include timing estimates for each activity.
"""
        
        return prompt


class ItineraryDisplay:
    """Handles the display of generated itineraries."""
    
    @staticmethod
    def render_itinerary_form(hike_data: Optional[Dict[str, Any]] = None):
        """Render the itinerary generation form."""
        st.subheader("🎯 Customize Your Itinerary")
        
        # User preferences input
        user_preferences = st.text_area(
            "Any specific preferences or interests? (optional)",
            placeholder="e.g., I love photography, prefer casual dining, want to see local wildlife, etc.",
            help="Tell us about your interests to personalize your itinerary!"
        )
        
        # Generate button
        if st.button("🚀 Generate My Perfect Day", type="primary"):
            if hike_data:
                return user_preferences
            else:
                st.error("No hike data available. Please scrape a hike first!")
                return None
        
        return None
    
    @staticmethod
    def render_itinerary(itinerary: str):
        """Render the generated itinerary in a beautiful format."""
        st.success("✨ Your Perfect Day Itinerary is Ready!")
        
        # Display the itinerary
        st.markdown("---")
        st.markdown(itinerary)
        
        # Add download option
        st.download_button(
            label="📥 Download Itinerary",
            data=itinerary,
            file_name="hike_itinerary.md",
            mime="text/markdown"
        ) 