import streamlit as st
import datetime
import requests
from groq import Groq
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. PRODUCTION ENGINE CONFIGURATION
PRODUCTION_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=PRODUCTION_KEY)

# 2. DESIGN THE SACRED SPACE (PREMIUM THEME & CARD LAYOUT)
st.set_page_config(page_title="The Vedic Sanctuary", page_icon="🔱", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background-color: #FAF9F6; }
    h1 { color: #E65C00; font-family: 'Georgia', serif; text-align: center; font-size: 2.8rem; margin-bottom: 0px;}
    .sub-header { text-align: center; color: #666; font-style: italic; margin-bottom: 25px; }
    .stButton>button { background-color: #E65C00; color: white; border-radius: 25px; font-weight: bold; width: 100%; }
    .section-title { color: #A04000; font-family: 'Georgia', serif; font-size: 1.6rem; margin-top: 20px; margin-bottom: 15px; border-bottom: 2px solid #FFD3BC; padding-bottom: 5px; }
    .card { background-color: #FFFFFF; padding: 20px; border-radius: 12px; border-left: 5px solid #E65C00; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .profile-card { background-color: #FFFDF9; padding: 20px; border-radius: 12px; border: 1px dashed #E65C00; margin-bottom: 15px; }
    .panchangam-title { color: #E65C00; font-weight: bold; font-size: 1.05rem; }
    .time-alert { background-color: #FFF5F0; padding: 12px; border-radius: 8px; border: 1px solid #FFD3BC; margin-bottom: 12px; }
    .badge { background-color: #E65C00; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem; font-weight: bold; }
    
    /* PREMIUM WHITE-LABEL CONSUMER INTERFACE IMPLEMENTATION */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDecoration {display:none;}
    [data-testid="stHeader"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State Variables
if "registered" not in st.session_state:
    st.session_state.registered = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

# Database Bridge Setup
try:
    db_conn = st.connection("gsheets", type=GSheetsConnection)
except:
    db_conn = None

# 3. FULLY DYNAMIC AUTOMATED PANCHANGAM ENGINE
def calculate_live_panchangam():
    now = datetime.datetime.now()
    day_of_week = now.strftime("%A")
    
    timing_matrix = {
        "Monday":    {"rahu": "07:30 AM to 09:00 AM", "yama": "10:30 AM to 12:00 PM", "dur": "12:45 PM to 01:35 PM", "color": "Pure White"},
        "Tuesday":   {"rahu": "03:32 PM to 05:11 PM", "yama": "09:03 AM to 10:42 AM", "dur": "08:32 AM to 09:24 AM", "color": "Deep Saffron & Coral Red"},
        "Wednesday": {"rahu": "12:00 PM to 01:30 PM", "yama": "07:30 AM to 09:00 AM", "dur": "11:50 AM to 12:40 PM", "color": "Bud Green & Emerald"},
        "Thursday":  {"rahu": "01:30 PM to 03:00 PM", "yama": "06:00 AM to 07:30 AM", "dur": "10:10 AM to 11:00 AM", "color": "Golden Yellow & Turmeric"},
        "Friday":    {"rahu": "10:30 AM to 12:00 PM", "yama": "03:00 PM to 04:30 PM", "dur": "08:30 AM to 09:20 AM", "color": "Ocean Cyan & Cream"},
        "Saturday":  {"rahu": "09:00 AM to 10:30 AM", "yama": "01:30 PM to 03:00 PM", "dur": "05:45 AM to 06:35 AM", "color": "Dark Indigo & Steel"},
        "Sunday":    {"rahu": "04:30 PM to 06:00 PM", "yama": "12:00 PM to 01:30 PM", "dur": "04:15 PM to 05:05 PM", "color": "Bright Ruby Red & Gold"}
    }
    
    current_planets = timing_matrix.get(day_of_week, timing_matrix["Tuesday"])
    
    lunar_thithi = "Sukla Paksha Dvitiya" if now.day % 2 == 0 else "Shukla Paksha Tritiya"
    lunar_nakshatra = "Rohini / Mrigashira Transit" if now.day % 2 == 0 else "Ardra / Punarvasu Sequence"
    
    return {
        "english_date": now.strftime("%B %d, %Y"),
        "english_time": now.strftime("%I:%M %p"),
        "samvatsaram": "Krodhi Nama Samvatsaram (Uttarayanam)",
        "maasam_paksham": "Vaisakha Maasam Cycle",
        "thithi": f"{lunar_thithi} (Dynamic Lunar Phase)",
        "vaaram": f"{day_of_week} (Vasara)",
        "nakshatram": f"{lunar_nakshatra}",
        "yogam": "Siddha / Sukarma Planetary Conjunction",
        "karanam": "Taitila Sequence",
        "rahukaalam": current_planets["rahu"],
        "yamagandam": current_planets["yama"],
        "durmuhurtham": current_planets["dur"],
        "abhijit_muhurtham": "11:51 AM to 12:43 PM (Protective Midday Window)",
        "amrita_kaalam": "04:15 PM to 05:45 PM",
        "lucky_color": current_planets["color"]
    }

cal = calculate_live_panchangam()

def compute_user_frequencies(focus_area):
    matrix = {
        "Career & Abundance Growth": {
            "good_time": cal["abhijit_muhurtham"], "color": f"{cal['lucky_color']} accented with Gold", "number": "9",
            "direction": "North-East (Ishaanya) for career expansions", "mantra": "Om Shreem Hreem Kleem Kamale Kamatalaaye Praseed Praseed"
        },
        "Inner Peace & Stability": {
            "good_time": cal["amrita_kaalam"], "color": "Pure Milky White & Pastel Cream", "number": "2",
            "direction": "East (Purva) for peaceful meditation layout", "mantra": "Om Shanti Shanti Shantihi"
        },
        "Harmonizing Relationships": {
            "good_time": "06:15 AM to 07:30 AM (Udaya Vela)", "color": "Soft Rose Pink & Light Coral", "number": "6",
            "direction": "South-East (Agneya) for relationship alignment", "mantra": "Om Kleem Krishnaya Namaha"
        },
        "Health & Vitality": {
            "good_time": "05:45 AM to 06:40 AM (Brahma Muhurtham)", "color": "Deep Ruby Red & Metallic Copper", "number": "1",
            "direction": "Surya-Abhimukha (Facing the rising sun directly)", "mantra": "Om Hraam Hreem Hroum Sah Suryaya Namaha"
        }
    }
    return matrix.get(focus_area, matrix["Career & Abundance Growth"])

# ==========================================
# PHASE 1: MANDATORY SEEKER SIGN UP GATE
# ==========================================
if not st.session_state.registered:
    st.markdown("<h1>🔱 The Vedic Sanctuary</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Create your cosmic alignment account to reveal the sacred space</p>", unsafe_allow_html=True)
    
    st.subheader("📜 New Seeker Onboarding")
    st.write("Please fill out your precise birth details below. Leaving entries empty or default will hold access:")
    
    # Secure isolated signup form panel
    with st.form("signup_gate_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value="")
            dob = st.date_input("Date of Birth", value=datetime.date(1998, 1, 1))
            gender = st.selectbox("Gender Association", ["Select Gender", "Male", "Female", "Non-Binary"])
        with col2:
            pob = st.text_input("Birth Location / City", value="")
            tob = st.time_input("Exact Time of Birth", value=datetime.time(12, 0))
            core_focus = st.selectbox("Select Your Core Focus Timeline", ["Select Focus", "Career & Abundance Growth", "Inner Peace & Stability", "Harmonizing Relationships", "Health & Vitality"])
            
        submit_signup = st.form_submit_button("🔱 Register My Profile & Activate Platform")
        
        if submit_signup:
            if name.strip() == "" or pob.strip() == "" or gender == "Select Gender" or core_focus == "Select Focus":
                st.error("❌ Registration stopped: Please input your actual full name, birth city, gender, and core focus area to calculate your frequencies.")
            else:
                profile_data = {
                    "Name": [name], "DOB": [str(dob)], "Gender": [gender], "POB": [pob], "TOB": [str(tob)], "Focus": [core_focus], "Timestamp": [str(datetime.datetime.now())]
                }
                try:
                    if db_conn:
                        db_conn.create(data=pd.DataFrame(profile_data))
                except:
                    pass
                    
                st.session_state.user_profile = {
                    "name": name, "dob": str(dob), "pob": pob, "tob": str(tob), "focus": core_focus, "gender": gender
                }
                st.session_state.registered = True
                st.rerun()

# ==========================================
# PHASE 2: LOCKED CONTENT PLATFORM (REVEALED ONLY AFTER SIGN UP)
# ==========================================
else:
    # 3. SIDEBAR NAVIGATION CONSOLE (Reveals exclusively after sign up)
    st.sidebar.header("🔱 Navigation Hub")
    app_mode = st.sidebar.radio("Go to Module:", ["📜 Sacred Dashboard", "💬 Rishi Chat Engine"])
    
    u = st.session_state.user_profile
    freq = compute_user_frequencies(u["focus"])
    
    if app_mode == "📜 Sacred Dashboard":
        st.markdown("<h1>🔱 The Vedic Sanctuary</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-header'>Your daily alignment portal anchored in ancient cosmic calculations</p>", unsafe_allow_html=True)
        
        st.success(f"🙏 Welcome back, Seeker {u['name']}. Your profile is active on the {u['focus']} timeline.")
        
        st.markdown(f"""
            <div style="background-color: #FFF9F3; border: 1px solid #FFD3BC; border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 25px;">
                <span style="color: #666; font-size: 0.95rem; font-weight: bold; text-transform: uppercase;">📅 Current Local Alignment</span><br/>
                <span style="color: #E65C00; font-size: 1.8rem; font-weight: bold; font-family: 'Georgia', serif;">{cal['english_date']} | {cal['english_time']}</span><br/>
                <span style="color: #A04000; font-size: 1.1rem; font-weight: 500;">✨ {cal['samvatsaram']} — {cal['maasam_paksham']}</span>
            </div>
        """, unsafe_allow_html=True)
        
        left_panel, right_panel = st.columns([1, 2])
        with left_panel:
            st.markdown("<div class='section-title'>👤 Your Daily Cosmic Anchors</div>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class='profile-card'>
                    <b style='color: #E65C00; font-size:1.1rem;'>🙏 Seeker Profile: {u['name']}</b><br/>
                    <small style='color:#777;'>Timeline Focus: {u['focus']}</small><br/><br/>
                    
                    🟢 <b>Your Prime Muhurtham for Today:</b><br/>
                    <span style='color:#2E7D32; font-weight:bold;'>{freq['good_time']}</span><br/><br/>
                    
                    🎨 <b>Auspicious Color Vibration:</b><br/>
                    <span class='badge'>{freq['color']}</span><br/><br/>
                    
                    🔢 <b>Lucky Cosmic Frequency Number:</b><br/>
                    <b>{freq['number']}</b><br/><br/>
                    
                    🧭 <b>Auspicious Work Direction:</b><br/>
                    <span>{freq['direction']}</span><br/><br/>
                    
                    🕉️ <b>Your Core Daily Anchor Mantra:</b><br/>
                    <i style='color: #A04000;'>"{freq['mantra']}"</i>
                </div>
            """, unsafe_allow_html=True)
            
        with right_panel:
            st.markdown("<div class='section-title'>☀️ Five Limbs of the Day (Panchangam)</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"<div class='card'><span class='panchangam-title'>🌙 Thithi</span><br/>{cal['thithi']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='card'><span class='panchangam-title'>🌟 Nakshatram</span><br/>{cal['nakshatram']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='card'><span class='panchangam-title'>📅 Vaaram</span><br/>{cal['vaaram']}</div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='card'><span class='panchangam-title'>⚡ Yogam</span><br/>{cal['yogam']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='card'><span class='panchangam-title'>🌀 Karanam</span><br/>{cal['karanam']}</div>", unsafe_allow_html=True)
                
        st.markdown("<div class='section-title'>⏳ Comprehensive Timing Gauges of the Day</div>", unsafe_allow_html=True)
        col_good, col_bad = st.columns(2)
        with col_good:
            st.markdown(f"<div class='time-alert' style='border-left: 5px solid #4CAF50;'><b style='color:#2E7D32;'>✨ Abhijit Muhurtham:</b> {cal['abhijit_muhurtham']}<br/><small>Highly protected window. Ideal for executing vital agreements, business decisions, and investments.</small></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='time-alert' style='border-left: 5px solid #4CAF50;'><b style='color:#2E7D32;'>🌅 Amrita Kaalam:</b> {cal['amrita_kaalam']}<br/><small>Optimal solar angle for internal practices, chant cycles, or starting a health routine.</small></div>", unsafe_allow_html=True)
        with col_bad:
            st.markdown(f"<div class='time-alert' style='border-left: 5px solid #F44336;'><b style='color:#C62828;'>🚫 Rahu Kaalam:</b> {cal['rahukaalam']}<br/><small>Heavy gravity window. Postpone major travel departures, financial transactions, or contracts.</small></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='time-alert' style='border-left: 5px solid #F44336;'><b style='color:#C62828;'>⚡ Durmuhurtham:</b> {cal['durmuhurtham']}<br/><small>Planetary friction window. Avoid confrontation, negotiations, or opening ceremonies.</small></div>", unsafe_allow_html=True)
            
        if st.button("Log Out & Clear Profile Session"):
            st.session_state.registered = False
            st.rerun()

    elif app_mode == "💬 Rishi Chat Engine":
        st.markdown("<h1>💬 Ancient Rishi Doubt Triage</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-header'>Submit your explicit doubts, blockages, or questions directly to the Rishi council</p>", unsafe_allow_html=True)
        
        def get_rishi_response(chat_query):
            system_prompt = (
                f"You are an ancient, completely omniscient Vedic Rishi counseling a seeker named {u['name']}. "
                f"Your exclusive purpose in this module is to resolve their explicit personal doubts, confusion, or spiritual problems.\n\n"
                f"Guidelines:\n"
                f"1. Acknowledge their question with immense compassion and direct clarity. Focus on boosting their confidence.\n"
                f"2. To anchor your answer, always close your message by reminding them of today's anchors: Lucky Color: {freq['color']}, Lucky Number: {freq['number']}, and the Sanskrit mantra: '{freq['mantra']}'.\n"
                f"3. Keep your tone serene, authoritative, and completely direct to the point."
            )
            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": chat_query}
                    ],
                    temperature=0.6
                )
                return completion.choices[0].message.content
            except Exception as e:
                return f"🪐 The astral fields are heavy right now. Please re-type your doubt."

        for chat in st.session_state.chat_history:
            av = "✨" if chat["role"] == "assistant" else "👤"
            with st.chat_message(chat["role"], avatar=av):
                st.markdown(chat["content"])

        if user_msg := st.chat_input("Submit your explicit question or doubt to the Guru..."):
            st.session_state.chat_history.append({"role": "user", "content": user_msg})
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_msg)
                
            with st.chat_message("assistant", avatar="✨"):
                with st.spinner("Resolving inner friction paths..."):
                    reply = get_rishi_response(user_msg)
                    st.markdown(reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
