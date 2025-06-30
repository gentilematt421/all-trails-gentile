# AllTrails Adventure Planner 🥾🌲

A Streamlit app for hiking enthusiasts and adventure planners! Scrape hike data from AllTrails, generate a personalized daily itinerary with AI, and visualize your adventure on an interactive map.

---

## 🚀 What is this app?
This app helps you:
- **Scrape hike details** from any AllTrails hike URL
- **Generate a perfect day itinerary** around your hike using ChatGPT
- **Visualize your hike and recommended places** on an interactive map
- **Download your itinerary** as Markdown or PDF

Built for the AllTrails Senior Product Analyst project, but useful for anyone who loves the outdoors!

---

## 🗺️ User Flow
1. **Home Page**
   - Enter an AllTrails hike URL
   - This URL is shared across all pages using session state
2. **Hike Scraper Page**
   - Scrape hike details (name, location, difficulty, length, elevation, features, etc.)
   - Review the hike data before planning your day
3. **Build A Day Around My Hike Page**
   - Add your preferences (e.g., "I love coffee shops", "Prefer easy hikes", etc.)
   - Generate a detailed, realistic itinerary using ChatGPT
   - The itinerary includes a "Places Mentioned" section with addresses for mapping
   - Download your itinerary as Markdown or PDF
4. **Daily Map Page**
   - See your hike and all recommended places on an interactive map
   - Each place is numbered to match the "Places Mentioned" list
   - Click pins for details

---

## 📄 Page-by-Page Overview

### 1. Home Page
- **Purpose:** Start here! Enter your AllTrails hike URL.
- **How to use:** Paste a valid AllTrails hike link. The app will remember it as you move between pages.

### 2. 🌲 Hike Scraper
- **Purpose:** Scrape and review hike details from AllTrails.
- **How to use:**
  - Click "Scrape Hike Data" to extract info from the URL you entered.
  - See trail name, location, stats, description, and features.
  - If scraping fails (403 error), try a different URL or wait a few minutes.

### 3. 🏔️ Build A Day Around My Hike
- **Purpose:** Generate a personalized itinerary for your hiking day.
- **How to use:**
  - Add any preferences (food, activities, timing, etc.)
  - Click "Generate My Perfect Day"
  - Review your AI-generated itinerary, including a "Places Mentioned" section
  - Download as Markdown or PDF

### 4. 🗺️ Daily Map
- **Purpose:** Visualize your hike and all recommended places on a map.
- **How to use:**
  - See your trail and all "Places Mentioned" as numbered pins
  - Click pins for names and addresses
  - Use the map to plan your route and stops

---

## 👤 Who is this for?
- Hikers, outdoor lovers, and trip planners
- Anyone who wants a smart, AI-powered day plan around a hike
- AllTrails team (as a product/portfolio demo)

---

## 🛠️ How to Use (Quick Start)
1. **Clone the repo:**
   ```bash
   git clone https://github.com/gentilematt421/all-trails-gentile.git
   cd all-trails-gentile
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Add your OpenAI API key:**
   - Create `.streamlit/secrets.toml` and add:
     ```toml
     OPENAI_API_KEY = "sk-your-api-key"
     ```
4. **Run the app:**
   ```bash
   streamlit run app/main.py
   ```
5. **Or deploy to Streamlit Cloud!**

---

## ⚠️ Notes & Troubleshooting
- **403 Errors:** AllTrails may block scraping. Try a different URL, wait, or enter data manually.
- **API Key:** Never share your OpenAI key. Use secrets for deployment.
- **Session State:** URL and hike data are shared across pages for a smooth experience.

---

## 💡 Features
- Modular, multi-page Streamlit app
- Robust AllTrails scraper with anti-blocking measures
- AI-powered itinerary generation (OpenAI GPT)
- Interactive map with numbered pins for all places
- Downloadable itineraries (Markdown, PDF)
- Clean, user-friendly UI

---

## 📬 Feedback
Questions, ideas, or want to collaborate? [Open an issue](https://github.com/gentilematt421/all-trails-gentile/issues) or reach out!
