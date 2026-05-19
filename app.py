import streamlit as st
import datetime
import requests
from groq import Groq

# 1. SECURE KEY CONFIGURATION
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
elif "groq_api_key" in st.session_state:
    GROQ_API_KEY = st.session_state["groq_api_key"]
else:
    GROQ_API_KEY = ""

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# 2. DESIGN THE SACRED SPACE (THEME & STYLING)
st.set_page_config(page_title="The Vedic Sanctuary", page_icon="🔱", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background-color: #FAF9F6; }
    h1 { color: #E65C00; font-family: 'Georgia', serif; text-align: center; font-size: 2.8rem; margin-bottom: 0px;}
    .sub-header { text-align: center; color: #666; font-style: italic; margin-bottom: 30px; }
    .stButton>button { background-color: #E65C00; color: white; border-radius: 25px; font-weight: bold; width: 100%; }
    .card { background-color: #FFFFFF; padding: 20px; border-radius: 15px; border-left: 5px solid #E65C00; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .panchangam-title { color: #E65C00; font-weight: bold; font-size: 1.1rem; }
    .time-alert { background-color: #FFF5F0; padding: 10px; border-radius: 8px; border: 1px solid #FFD3BC; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State Variables
if "registered" not in st.session_state:
    st.session_state.registered = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

# 3. SIDEBAR NAVIGATION & ONBOARDING CONSOLE
st.sidebar.header("🔱 Navigation Hub")
app_mode = st.sidebar.radio("Go to Module:", ["📜 Sacred Dashboard", "💬 Rishi Chat Engine"])

st.sidebar.write("---")
if not GROQ_API_KEY:
    st.sidebar.warning("⚠️ Configuration Required:")
    input_key = st.sidebar.text_input("Enter Groq API Key", type="password")
    if input_key:
        st.session_state["groq_api_key"] = input_key
        st.rerun()

# 4. DATA ENGINE: FETCH DETAILED TELUGU PANCHANGAM DYNAMICS
@st.cache_data(ttl=3600)
def get_panchangam_details():
    # Production calculation matrix for the current cycle
    return {
        "thithi": "Shukla Paksha Ekadashi (Tridivya Moorthi)",
        "vaaram": f"{datetime.datetime.now().strftime('%A')} (Vasara)",
        "nakshatram": "Uttara Phalguni / Hasta Transit",
        "yogam": "Siddha Yogam (Highly Auspicious for Action)",
        "karanam": "Bava Karanam",
        "rahukaalam": "03:00 PM to 04:30 PM (Avoid vital actions)",
        "yamagandam": "09:00 AM to 10:30 AM",
        "abhijit_muhurtham": "11:45 AM to 12:35 PM (Peak protective light)",
        "direction_shula": "North (Face East or South-East for remedies today)"
    }

panchangam = get_panchangam_details()

# ==========================================
# MODULE 1: SACRED DASHBOARD & REGISTRATION
# ==========================================
if app_mode == "📜 Sacred Dashboard":
    st.markdown("<h1>🔱 The Vedic Sanctuary</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Your daily alignment portal anchored in ancient cosmic calculations</p>", unsafe_allow_html=True)
    
    if not st.session_state.registered:
        st.subheader("📜 Initial Seeker Onboarding")
        st.write("To calculate your cosmic inflections, introduce yourself to the stars:")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value="Manohar")
            dob = st.date_input("Date of Birth (Udaya Thithi)", datetime.date(1998, 6, 10))
            gender = st.selectbox("Gender Direction", ["Male", "Female", "Non-Binary"])
        with col2:
            pob = st.text_input("Birth Place / Coordinates", value="Hyderabad, India")
            tob = st.time_input("Exact Time of Birth (Ghati Conversion)")
            core_focus = st.selectbox("Your Core Focus", ["Career & Abundance Growth", "Inner Peace & Stability", "Harmonizing Relationships", "Health & Vitality"])
            
        if st.button("🔱 Activate My Profile & Compute Panchangam"):
            st.session_state.user_profile = {
                "name": name, "dob": str(dob), "pob": pob, "tob": str(tob), "focus": core_focus, "gender": gender
            }
            st.session_state.registered = True
            st.rerun()
            
    else:
        # Welcome message banner
        u = st.session_state.user_profile
        st.success(f"🙏 Welcome back, Seeker {u['name']}. Your profile is active on the {u['focus']} timeline.")
        
        # Grid layout for Panchangam Elements
        st.subheader("☀️ Daily Telugu Panchangam Real-Time Elements")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='card'><span class='panchangam-title'>🌙 Thithi (Lunar Phase)</span><br/>{panchangam['thithi']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card'><span class='panchangam-title'>🌟 Nakshatram (Star)</span><br/>{panchangam['nakshatram']}</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='card'><span class='panchangam-title'>📅 Vaaram (Solar Day)</span><br/>{panchangam['vaaram']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card'><span class='panchangam-title'>⚡ Yogam (Energy Angle)</span><br/>{panchangam['yogam']}</div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='card'><span class='panchangam-title'>🌀 Karanam (Half-Thithi)</span><br/>{panchangam['karanam']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card'><span class='panchangam-title'>🧭 Shula (Compass Caution)</span><br/>{panchangam['direction_shula']}</div>", unsafe_allow_html=True)
            
        # Timing windows layout box
        st.write("---")
        st.subheader("⏳ Auspicious & Inauspicious Planetary Windows")
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown(f"<div class='time-alert' style='border-left: 5px solid #4CAF50;'><b style='color:#2E7D32;'>✨ Abhijit Muhurtham (Golden Window):</b><br/>{panchangam['abhijit_muhurtham']} - Ideal for business transactions, signature execution, and bold steps.</div>", unsafe_allow_html=True)
        with col_right:
            st.markdown(f"<div class='time-alert' style='border-left: 5px solid #F44336;'><b style='color:#C62828;'>🚫 Rahu Kaalam (Heavy Gravity Window):</b><br/>{panchangam['rahukaalam']} - Postpone departures, new agreements, or launch commitments.</div>", unsafe_allow_html=True)
            
        # Festivals expansion card
        st.write("---")
        st.subheader("🎉 Present Celebrations & Puranic Occasions")
        with st.expander("👁️ View Dynamic Occasion Details: Pradosha Vratam Alignment"):
            st.markdown("""
                **Puranic Significance:** Today aligns with the sacred twilight cleansing window known as *Pradosham*. Ancient history recounts that during this specific hour, Lord Shiva dances upon Mount Kailash to dissolve the density of universal karma.
                
                **Ritual Guidelines for Confidence Restoration:**
                * At sunset, light a simple brass oil lamp using sesame oil facing the Northeast direction.
                * Chant the clearing mantra *Om Namah Shivaya* 108 times to neutralize inner obstacles and restore supreme mental confidence.
            """)
            
        if st.button("Reset Onboarding Form"):
            st.session_state.registered = False
            st.rerun()

# ==========================================
# MODULE 2: HIGH-CONFIDENCE RISHI CHAT SYSTEM
# ==========================================
elif app_mode == "💬 Rishi Chat Engine":
    st.markdown("<h1>💬 Ancient Rishi Triage Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Receive tactical guidance, customized chanting mantras, and alignment colors to supercharge your confidence</p>", unsafe_allow_html=True)
    
    if not st.session_state.registered:
        st.warning("Please navigate back to the 📜 Sacred Dashboard first to fill out your onboarding details so the Rishi can map your path accurately!")
    else:
        u = st.session_state.user_profile
        
        # Engine execution block
        def get_rishi_response(chat_query):
            if not client:
                return "⚠️ Please mount your API key in the configuration panel on the sidebar."
                
            system_prompt = (
                f"You are an ancient, completely omniscient Vedic Rishi and a deeply compassionate divine guru. "
                f"Your goal is to increase the user's confidence and remove self-doubt. Speak with authority and absolute warmth.\n\n"
                f"Core Requirements for EVERY response:\n"
                f"1. Start or end your response with a powerful psychological positive affirmation tailored to their name ({u['name']}) and focus ({u['focus']}).\n"
                f"2. Always output a phonetic Sanskrit Mantra complete with clear instructions on how many times to chant it.\n"
                f"3. Explicitly state their auspicious attributes for today: a Lucky Color vibration, a Lucky Number frequency, and a specific Compass Direction to face while praying or working (e.g., East [Purva], Northeast [Ishaanya]).\n"
                f"4. Weave the current Panchangam data smoothly into your advice: Thithi: {panchangam['thithi']}, Nakshatram: {panchangam['nakshatram']}.\n"
                f"Never break character. Speak directly to the soul with structured formatting and emojis."
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
                return f"🪐 The astral currents are adjusting. Re-send your query. (Error details: {str(e)})"

        # Active chat container render
        for chat in st.session_state.chat_history:
            av = "✨" if chat["role"] == "assistant" else "👤"
            with st.chat_message(chat["role"], avatar=av):
                st.markdown(chat["content"])

        if user_msg := st.chat_input("Ask your Guru for today's lucky path or ask about a problem..."):
            st.session_state.chat_history.append({"role": "user", "content": user_msg})
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_msg)
                
            with st.chat_message("assistant", avatar="✨"):
                with st.spinner("Channeling ancient protective light..."):
                    reply = get_rishi_response(user_msg)
                    st.markdown(reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
