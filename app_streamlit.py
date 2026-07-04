import streamlit as st
import requests
from datetime import datetime
import os

# ============ GET GOOGLE SCRIPT URL ============
# Try to get from Streamlit secrets first (cloud)
try:
    GOOGLE_SCRIPT_URL = st.secrets.get('GOOGLE_SCRIPT_URL', '')
except:
    GOOGLE_SCRIPT_URL = ''

# Fallback to .env (local development)
if not GOOGLE_SCRIPT_URL:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        GOOGLE_SCRIPT_URL = os.getenv('GOOGLE_SCRIPT_URL', '')
    except:
        pass

# Final fallback (not recommended)
if not GOOGLE_SCRIPT_URL:
    GOOGLE_SCRIPT_URL = "YOUR_GOOGLE_SCRIPT_URL_HERE"

st.set_page_config(
    page_title="CS2 Coaching Management",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #ff4b4b;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #ff6b6b;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .stButton button {
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #e63946;
    }
    .success-text {
        color: #4CAF50;
        padding: 10px;
        background: #1e3a1e;
        border-radius: 5px;
        border-left: 4px solid #4CAF50;
    }
    .error-text {
        color: #ff6b6b;
        padding: 10px;
        background: #3a1e1e;
        border-radius: 5px;
        border-left: 4px solid #ff6b6b;
    }
    .info-text {
        color: #ffd93d;
        padding: 10px;
        background: #3a3a1e;
        border-radius: 5px;
        border-left: 4px solid #ffd93d;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🎯 CS2 Coaching Management</h1>', unsafe_allow_html=True)
    
    if not GOOGLE_SCRIPT_URL:
        st.error("❌ Google Script URL not configured!")
        st.info("Please add GOOGLE_SCRIPT_URL to your secrets or .env file")
        return
    
    with st.form("coaching_form", clear_on_submit=True):
        # Client Information
        st.markdown('<p class="sub-header">👤 Client Information</p>', unsafe_allow_html=True)
        name = st.text_input("Name/Nickname *", placeholder="Enter client's name or nickname")
        
        # Contact Information
        st.markdown('<p class="sub-header">📱 Contact Information <span style="color:#8892b0;font-weight:400;font-size:12px;">(at least one required)</span></p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("Email", placeholder="client@email.com")
            steam = st.text_input("Steam", placeholder="Steam ID or profile URL")
        with col2:
            telegram = st.text_input("Telegram", placeholder="@username")
            discord = st.text_input("Discord", placeholder="username#1234")
        
        whatsapp = st.text_input("WhatsApp", placeholder="+1234567890")
        
        # Faceit Profile
        st.markdown('<p class="sub-header">🎮 Faceit Profile</p>', unsafe_allow_html=True)
        faceit = st.text_input("Faceit Profile URL", placeholder="https://www.faceit.com/en/players/username", value="-")
        st.caption("Enter '-' if you don't have a Faceit profile")
        
        # ELO Information
        st.markdown('<p class="sub-header">📊 ELO Information</p>', unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            current_elo = st.number_input("Current ELO", min_value=0, max_value=10000, value=1000, step=50)
        with col4:
            max_elo = st.number_input("MAX ELO", min_value=0, max_value=10000, value=1000, step=50)
        
        # Preferred Maps
        st.markdown('<p class="sub-header">🗺️ Preferred Maps</p>', unsafe_allow_html=True)
        maps = st.multiselect(
            "Select maps",
            ["Dust II", "Mirage", "Inferno", "Nuke", "Overpass", "Vertigo", "Ancient", "Anubis", "All Maps"],
            placeholder="Select preferred maps"
        )
        
        # Problems to Fix
        st.markdown('<p class="sub-header">🎯 Problems to Fix</p>', unsafe_allow_html=True)
        problems = st.multiselect(
            "Select areas to improve",
            ["Aim", "Movement", "Positioning", "Disadvantage", "Entry frager (Opening)", 
             "Defending", "Lurking/flanking", "Support (Utility knowledge)", "Game maker", 
             "Active Player", "Pressure", "Element of surprise"],
            placeholder="Select problems to fix"
        )
        
        # Availability
        st.markdown('<p class="sub-header">📅 Availability</p>', unsafe_allow_html=True)
        col5, col6 = st.columns(2)
        with col5:
            hours = st.number_input("Hours per Session", min_value=0.5, max_value=6.0, value=1.5, step=0.5)
        with col6:
            days = st.multiselect(
                "Available Days",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                placeholder="Select available days"
            )
        
        # Additional Notes
        st.markdown('<p class="sub-header">📝 Additional Notes</p>', unsafe_allow_html=True)
        notes = st.text_area("Any additional information or special requirements", placeholder="Add any relevant notes here...", height=100)
        
        # Submit button
        submitted = st.form_submit_button("📤 Submit Client Profile")
        
        if submitted:
            # Validation
            errors = []
            if not name:
                errors.append("Name is required")
            
            contacts = [email, telegram, steam, discord, whatsapp]
            if not any(contact.strip() for contact in contacts):
                errors.append("At least one contact method is required")
            
            if not maps:
                errors.append("Please select at least one map")
            
            if not problems:
                errors.append("Please select at least one problem")
            
            if not days:
                errors.append("Please select at least one available day")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Prepare data
                data = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "name": name,
                    "email": email,
                    "telegram": telegram,
                    "steam": steam,
                    "discord": discord,
                    "whatsapp": whatsapp,
                    "faceit": faceit if faceit else "-",
                    "current_elo": current_elo,
                    "max_elo": max_elo,
                    "maps": ", ".join(maps),
                    "problems": ", ".join(problems),
                    "hours_per_session": hours,
                    "days": ", ".join(days),
                    "additional_notes": notes
                }
                
                try:
                    with st.spinner("Sending data to Google Sheets..."):
                        response = requests.post(GOOGLE_SCRIPT_URL, json=data, timeout=30)
                    
                    if response.status_code == 200:
                        st.success("✅ Client profile submitted successfully!")
                        st.balloons()
                    else:
                        st.error(f"❌ Error: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Connection error: {str(e)}")

if __name__ == "__main__":
    main()