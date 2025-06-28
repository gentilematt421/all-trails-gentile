"""
Itinerary Generator Module

This module handles the generation of daily itineraries using ChatGPT
based on hike data and pre-canned prompts.
"""

import openai
import streamlit as st
from typing import Optional, Dict, Any
from dataclasses import dataclass
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import io
import re


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
            system_prompt = self._get_system_prompt()
            
            # Debug: Show the prompts being sent
            with st.expander("🔍 Debug: View Prompts Sent to ChatGPT"):
                st.subheader("System Prompt (AI Persona):")
                st.code(system_prompt, language="text")
                
                st.subheader("User Prompt (Template with Hike Data):")
                st.code(prompt, language="text")
            
            # Call ChatGPT
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
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
4. **Post-Hike Activities** (lunch and dinner recommendations, relaxation, local attractions)
5. **Evening Plans** (post dinner activities local to the area or preferences, sunset viewing spots)
6. **Practical Tips** (weather considerations, gear recommendations, local insights)
7. **Places Mentioned** (list all restaurants, attractions, stores, and locations mentioned in the itinerary with their addresses)

Make the itinerary realistic based on the hike's difficulty and duration. Consider the location and suggest local favorites when possible. Include timing estimates for each activity.
Please give specific locations for suggestions as in actual places instead general suggestions like "a local brewery"
For the "Places Mentioned" section, provide a comprehensive list of all specific places you recommend (restaurants, cafes, stores, attractions, etc.) with their full addresses. If you mention a place in the itinerary, make sure to include it in this section with its address.
"""
        
        return prompt


class PDFGenerator:
    """Handles PDF generation for itineraries."""
    
    @staticmethod
    def create_pdf(itinerary_text: str, hike_name: str = "Hike") -> bytes:
        """
        Create a PDF from the itinerary text.
        
        Args:
            itinerary_text: The itinerary text to convert to PDF
            hike_name: Name of the hike for the filename
            
        Returns:
            PDF file as bytes
        """
        # Create a buffer to store the PDF
        buffer = io.BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#2E8B57'),  # Sea Green
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=HexColor('#4682B4'),  # Steel Blue
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=8,
            leading=16
        )
        
        # Add title
        title = Paragraph(f"Perfect Day Itinerary<br/>for {hike_name}", title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Add subtitle
        subtitle = Paragraph("Generated by AllTrails Adventure Planner", body_style)
        story.append(subtitle)
        story.append(Spacer(1, 30))
        
        # Process the itinerary text
        lines = itinerary_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 8))
                continue
            
            # Check if it's a heading (starts with ** or is numbered)
            if line.startswith('**') and line.endswith('**'):
                # Remove ** and create heading
                heading_text = line[2:-2]
                heading = Paragraph(heading_text, heading_style)
                story.append(heading)
            elif re.match(r'^\d+\.\s+\*\*', line):
                # Numbered heading
                heading_text = line
                heading = Paragraph(heading_text, heading_style)
                story.append(heading)
            elif line.startswith('•') or line.startswith('-'):
                # Bullet point
                bullet_text = f"&nbsp;&nbsp;&nbsp;&nbsp;{line}"
                bullet = Paragraph(bullet_text, body_style)
                story.append(bullet)
            else:
                # Regular text
                paragraph = Paragraph(line, body_style)
                story.append(paragraph)
        
        # Build the PDF
        doc.build(story)
        
        # Get the PDF content
        pdf_content = buffer.getvalue()
        buffer.close()
        
        return pdf_content


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
    def render_itinerary(itinerary: str, hike_name: str = "Hike"):
        """Render the generated itinerary in a beautiful format."""
        st.success("✨ Your Perfect Day Itinerary is Ready!")
        
        # Display the itinerary
        st.markdown("---")
        st.markdown(itinerary)
        
        # Create columns for download buttons
        col1, col2 = st.columns(2)
        
        with col1:
            # Markdown download
            st.download_button(
                label="📄 Download as Markdown",
                data=itinerary,
                file_name="hike_itinerary.md",
                mime="text/markdown"
            )
        
        with col2:
            # PDF download
            try:
                pdf_content = PDFGenerator.create_pdf(itinerary, hike_name)
                st.download_button(
                    label="📕 Download as PDF",
                    data=pdf_content,
                    file_name=f"{hike_name.replace(' ', '_')}_itinerary.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
                st.download_button(
                    label="📄 Download as Markdown",
                    data=itinerary,
                    file_name="hike_itinerary.md",
                    mime="text/markdown"
                ) 