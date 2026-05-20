import streamlit as st
import datetime
from zoneinfo import ZoneInfo
import requests
from groq import Groq
import json

# 1. ENGINE & PRODUCTION CREDENTIAL SECURITY
PRODUCTION_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=PRODUCTION_KEY)

# 2. DESIGN TRADITIONAL MODERN SANCTUARY THEME (MOBILE RESPONSIVE)
st.set_page_config(page_title="The Vedic Sanctuary", page_icon="🔱", layout="wide")

st.markdown("""
    <style>
    /* Global Container & Fonts Tuning */
    .reportview-container { background-color: #FAF9F6; }
    h1 { color: #E65C00; font-family: 'Georgia', serif; text-align: center; font-size: 2.5rem; margin-bottom: 5px; font-weight: bold;}
    .sub-header { text-align: center; color: #555; font-style: italic; margin-bottom: 25px; font-size: 1.05rem; padding: 0 10px; }
    .section-title { color: #A04000; font-family: 'Georgia', serif; font-size: 1.5rem; margin-top: 25px; margin-bottom: 15px; border-bottom: 2px solid #FFD3BC; padding-bottom: 8px; font-weight: bold; }
    
    /* Premium Profile Banner Layout */
    .premium-profile-banner { background: linear-gradient(135deg, #FFFDF9 0%, #FFF5ED 100%); border: 1px solid #FFD3BC; border-radius: 16px; padding: 22px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(230,92,0,0.06); }
    .profile-header { color: #E65C00; font-size: 1.4rem; font-family: 'Georgia', serif; font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid #FFD3BC; padding-bottom: 10px; }
    
    /* Responsive Grid Structure */
    .anchor-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px; }
    .anchor-item { background: #FFFFFF; padding: 15px; border-radius: 10px; border-top: 4px solid #E65C00; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }
    .anchor-label { font-size: 0.8rem; color: #777; text-transform: uppercase; font-weight: bold; margin-bottom: 5px; display: block; }
    .anchor-value { font-size: 1rem; color: #222; font-weight: 600; }
    
    /* Standard Layout Objects */
    .card { background-color: #FFFFFF; padding: 18px; border-radius: 12px; border-left: 5px solid #E65C00; margin-bottom: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.04); }
    .panchangam-title { color: #E65C00; font-weight: bold; font-size: 1rem; display: block; margin-bottom: 6px; }
    .time-alert { background-color: #FFF5F0; padding: 14px; border-radius: 10px; border: 1px solid #FFD3BC; margin-bottom: 15px; }
    .badge-premium { background-color: #E65C00; color: white; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: bold; display: inline-block; }
    
    /* TARGETED BRANDING REMOVAL WITHOUT BREAKING THE NAVIGATION CORE */
    [data-testid="stToolbar"] { display: none !important; }
    footer { visibility: hidden !important; }
    .stDecoration { display: none !important; }
    
    /* Premium Saffron Sidebar Button Engine */
    button[data-testid="stSidebarCollapseButton"] { background-color: #FFF5ED !important; border: 1px solid #FFD3BC !important; border-radius: 50% !important; color: #E65C00 !important; font-weight: bold !important; box-shadow: 0 4px 10px rgba(230,92,0,0.18) !important; visibility: visible !important; display: inline-flex !important; }
    
    /* Upgraded Saffron Interactive Action Button Layout */
    .stButton>button, .stFormSubmitButton>button { background-color: #E65C00; color: white; border-radius: 25px; font-weight: bold; padding: 12px 30px; border: none; width: 100% !important; font-size: 1.05rem; box-shadow: 0 4px 10px rgba(230,92,0,0.2); transition: all 0.3s ease; }
    .stButton>button:hover, .stFormSubmitButton>button:hover { background-color: #C65000; transform: translateY(-1px); box-shadow: 0 6px 15px rgba(230,92,0,0.3); }
    
    /* Fixed Responsive Mobile Layout Settings */
    @media only screen and (max-width: 768px) {
        h1 { font-size: 1.85rem !important; }
        .sub-header { font-size: 0.95rem !important; margin-bottom: 20px; }
        .section-title { font-size: 1.3rem !important; }
        .premium-profile-banner { padding: 15px !important; }
        .profile-header { font-size: 1.15rem !important; text-align: center; }
        .anchor-grid { grid-template-columns: 1fr !important; gap: 12px !important; }
        .card { padding: 15px !important; margin-bottom: 12px !important; }
        .time-alert { padding: 12px !important; }
        [data-testid="stMainBlockContainer"] [data-testid="column"] { width: 100% !important; flex: 1 1 auto !important; padding: 0 !important; margin-bottom: 12px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALIZE STATE VARIABLE TRACKERS
if "registered" not in st.session_state:
    st.session_state.registered = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}
if "sync_required" not in st.session_state:
    st.session_state.sync_required = False

# ==========================================
# BROWSER LOCAL STORAGE RECOVERY ENGINE
# ==========================================
if not st.session_state.registered:
    query_params = st.query_params
    if "recovered_profile" in query_params:
        try:
            raw_json = query_params["recovered_profile"]
            parsed_profile = json.loads(raw_json)
            st.session_state.user_profile = parsed_profile
            st.session_state.registered = True
            st.query_params.clear()
            st.rerun()
        except:
            pass
    else:
        st.components.v1.html("""
            <script>
                try {
                    const localData = window.parent.localStorage.getItem("vedic_seeker_profile");
                    if (localData && localData.trim() !== "") {
                        const currentUrl = new URL(window.parent.location.href);
                        if (!currentUrl.searchParams.has("recovered_profile")) {
                            currentUrl.searchParams.set("recovered_profile", localData);
                            window.parent.location.href = currentUrl.toString();
                        }
                    }
                } catch(e) {}
            </script>
        """, height=0, width=0)

# 4. TIMEZONE ENGINE: FORCED INDIAN STANDARD TIME (IST) CALCULATION
def calculate_live_panchangam():
    ist_zone = ZoneInfo("Asia/Kolkata")
    now_ist = datetime.datetime.now(ist_zone)
    day_of_week = now_ist.strftime("%A")
    
    timing_matrix = {
        "Monday":    {"rahu": "07:30 AM to 09:00 AM", "yama": "10:30 AM to 12:00 PM", "dur": "12:45 PM to 01:35 PM", "color": "Pure White & Silver"},
        "Tuesday":   {"rahu": "03:32 PM to 05:11 PM", "yama": "09:03 AM to 10:42 AM", "dur": "08:32 AM to 09:24 AM", "color": "Deep Saffron & Coral Red"},
        "Wednesday": {"rahu": "12:00 PM to 01:30 PM", "yama": "07:30 AM to 09:00 AM", "dur": "11:50 AM to 12:40 PM", "color": "Bud Green & Emerald"},
        "Thursday":  {"rahu": "01:30 PM to 03:00 PM", "yama": "06:00 AM to 07:30 AM", "dur": "10:10 AM to 11:00 AM", "color": "Golden Yellow & Turmeric"},
        "Friday":    {"rahu": "10:30 AM to 12:00 PM", "yama": "03:00 PM to 04:30 PM", "dur": "08:30 AM to 09:20 AM", "color": "Ocean Cyan & Cream"},
        "Saturday":  {"rahu": "09:00 AM to 10:30 AM", "yama": "01:30 PM to 03:00 PM", "dur": "05:45 AM to 06:35 AM", "color": "Dark Indigo & Blue-Black"},
        "Sunday":    {"rahu": "04:30 PM to 06:00 PM", "yama": "12:00 PM to 01:30 PM", "dur": "04:15 PM to 05:05 PM", "color": "Bright Ruby Red & Gold"}
    }
    
    current_planets = timing_matrix.get(day_of_week, timing_matrix["Tuesday"])
    lunar_thithi = "Shukla Paksha Dvitiya" if now_ist.day % 2 == 0 else "Shukla Paksha Tritiya"
    lunar_nakshatra = "Rohini / Mrigashira Transit" if now_ist.day % 2 == 0 else "Ardra / Punarvasu Sequence"
    
    return {
        "english_date": now_ist.strftime("%B %d, %Y"),
        "english_time": now_ist.strftime("%I:%M %p (IST)"),
        "samvatsaram": "Krodhi Nama Samvatsaram (Uttarayanam)",
        "maasam_paksham": "Vaisakha Maasam Cycle",
        "thithi": f"{lunar_thithi}",
        "vaaram": f"{day_of_week} (Vasara)",
        "nakshatram": f"{lunar_nakshatra}",
        "yogam": "Siddha / Sukarma Planetary Conjunction",
        "karanam": "Taitila Sequence",
        "rahukaalam": current_planets["rahu"],
        "yamagandam": current_planets["yama"],
        "durmuhurtham": current_planets["dur"],
        "abhijit_muhurtham": "11:51 AM to 12:43 PM",
        "amrita_kaalam": "04:15 PM to 05:45 PM",
        "lucky_color": current_planets["color"]
    }

cal = calculate_live_panchangam()

def compute_user_frequencies(focus_area):
    matrix = {
        "Career & Abundance Growth": {
            "good_time": cal["abhijit_muhurtham"] + " (Abhijit Window)", "color": f"{cal['lucky_color']} accented with Gold", "number": "9",
            "direction": "North-East (Ishaanya) for career expansions", "mantra": "Om Shreem Hreem Kleem Kamale Kamatalaaye Praseed Praseed"
        },
        "Inner Peace & Stability": {
            "good_time": cal["amrita_kaalam"] + " (Amrita Window)", "color": "Pure Milky White & Pastel Cream", "number": "2",
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
# MODULE 1: SEEKER ONBOARDING GATED FORM
# ==========================================
if not st.session_state.registered:
    st.markdown("<h1>🔱 The Vedic Sanctuary</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Establish your birth alignment coordinates to enter the sacred space</p>", unsafe_allow_html=True)
    
    st.subheader("📜 Comprehensive Astro Onboarding Engine")
    st.write("Provide your core milestones. Optional parameters can be left blank to run standard calculations:")
    
    with st.form("gated_registration_form"):
        st.markdown("<b style='color:#E65C00; font-size:1.1rem;'>1. Core Birth Coordinates (Required)</b>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value="", placeholder="Enter your full name")
            dob = st.date_input("Date of Birth", value=datetime.date(1998, 6, 10))
            gender = st.selectbox("Gender Association", ["Select Gender", "Male", "Female", "Non-Binary"])
        with col2:
            pob = st.text_input("Birth Location / City", value="", placeholder="e.g. Hyderabad, India")
            tob = st.text_input("Exact Time of Birth (Optional)", value="", placeholder="e.g. 10:10 AM or 22:45")
            core_focus = st.selectbox("Select Your Core Focus Timeline", ["Select Focus", "Career & Abundance Growth", "Inner Peace & Stability", "Harmonizing Relationships", "Health & Vitality"])
            
        st.write("---")
        st.markdown("<b style='color:#A04000; font-size:1.1rem;'>2. Traditional Horoscope Parameters (Optional Expansion)</b>", unsafe_allow_html=True)
        col3, col4, col5 = st.columns(3)
        with col3:
            gotram = st.text_input("Gotram Lineage", value="", placeholder="e.g. Bharadwaja, Kasyapa")
        with col4:
            known_star = st.text_input("Known Janma Nakshatram", value="", placeholder="e.g. Krittika, Hasta")
        with col5:
            current_dasha = st.selectbox("Current Active Maha Dasha Period", ["Not Known / Auto-Calculate", "Rahu Dasha", "Guru Dasha (Jupiter)", "Shani Dasha (Saturn)", "Budha Dasha (Mercury)", "Ketu Dasha", "Sukra Dasha (Venus)", "Surya Dasha (Sun)", "Chandra Dasha (Moon)", "Kujava Dasha (Mars)"])
            
        submit_btn = st.form_submit_button("🔱 Compute My Regional Panchangam & Dashboard")
        
        if submit_btn:
            if name.strip() == "" or pob.strip() == "" or gender == "Select Gender" or core_focus == "Select Focus":
                st.error("❌ Form Error: Please specify your name, birth location, gender, and core focus to compute elements.")
            else:
                val_tob = tob.strip() if tob.strip() != "" else "Not Specified"
                val_gotram = gotram.strip() if gotram.strip() != "" else "Not Specified"
                val_star = known_star.strip() if known_star.strip() != "" else "Not Specified"
                val_dasha = current_dasha if current_dasha != "Not Known / Auto-Calculate" else "Not Specified"
                
                st.session_state.user_profile = {
                    "name": name, "dob": str(dob), "gender": gender, "pob": pob, "tob": val_tob, "focus": core_focus,
                    "gotram": val_gotram, "known_star": val_star, "current_dasha": val_dasha
                }
                st.session_state.registered = True
                st.session_state.sync_required = True
                st.rerun()

# ==========================================
# MODULE 2: REVEALED CONTENT CANVAS
# ==========================================
else:
    # BUG FIX: Write data to browser's native storage *after* successfully swapping views
    if st.session_state.sync_required:
        json_payload = json.dumps(st.session_state.user_profile)
        st.components.v1.html(f"""
            <script>
                try {{
                    window.parent.localStorage.setItem("vedic_seeker_profile", `{json_payload}`);
                }} catch(e) {{}}
            </script>
        """, height=0, width=0)
        st.session_state.sync_required = False

    # Dedicated Sidebar Profile Card Badge
    st.sidebar.markdown(f"""
        <div style='text-align: center; padding: 15px; background-color: #FFFDF9; border-radius: 12px; border: 1px solid #FFD3BC; margin-bottom: 20px;'>
            <span style='font-size: 2.5rem;'>👤</span><br/>
            <b style='color:#E65C00; font-size:1.1rem;'>Seeker: {st.session_state.user_profile['name']}</b><br/>
            <small style='color:#777;'>Gotram: {st.session_state.user_profile['gotram']}</small>
        </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.header("🔱 Navigation Hub")
    app_mode = st.sidebar.radio("Go to Module:", ["📜 Sacred Dashboard", "💬 Rishi Chat Engine", "⚙️ Edit Profile Data"])
    
    u = st.session_state.user_profile
    freq = compute_user_frequencies(u["focus"])
    
    # MODULE 2A: SACRED DASHBOARD VIEW
    if app_mode == "📜 Sacred Dashboard":
        st.markdown("<h1>🔱 The Vedic Sanctuary</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-header'>Your daily alignment portal anchored in ancient cosmic calculations</p>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="background-color: #FFF9F3; border: 1px solid #FFD3BC; border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 25px;">
                <span style="color: #666; font-size: 0.95rem; font-weight: bold; text-transform: uppercase;">📅 Current Local Alignment</span><br/>
                <span style="color: #E65C00; font-size: 1.8rem; font-weight: bold; font-family: 'Georgia', serif;">{cal['english_date']} | {cal['english_time']}</span><br/>
                <span style="color: #A04000; font-size: 1.1rem; font-weight: 500;">✨ {cal['samvatsaram']} — {cal['maasam_paksham']}</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class='premium-profile-banner'>
                <div class='profile-header'>🙏 Seeker Profile: {u['name']} &nbsp;|&nbsp; <span style='font-size:1.0rem; color:#666;'>Timeline: {u['focus']}</span></div>
                <div class='anchor-grid'>
                    <div class='anchor-item'>
                        <span class='anchor-label'>🟢 Prime Muhurtham</span>
                        <span class='anchor-value' style='color:#2E7D32;'>{freq['good_time']}</span>
                    </div>
                    <div class='anchor-item'>
                        <span class='anchor-label'>🎨 Color Vibration</span>
                        <div style='margin-top:5px;'><span class='badge-premium'>{freq['color']}</span></div>
                    </div>
                    <div class='anchor-item'>
                        <span class='anchor-label'>🔢 Lucky Frequency</span>
                        <span class='anchor-value' style='font-size:1.3rem; color:#E65C00;'>{freq['number']}</span>
                    </div>
                    <div class='anchor-item'>
                        <span class='anchor-label'>Compass Direction</span>
                        <span class='anchor-value'>{freq['direction']}</span>
                    </div>
                </div>
                <div style='margin-top: 20px; padding-top: 15px; border-top: 1px dashed #FFD3BC;'>
                    <span class='anchor-label'>🕉️ Your Daily Core Anchor Mantra</span>
                    <span style='font-size: 1.2rem; font-family: "Georgia", serif; color: #A04000; font-weight: bold;'>"{freq['mantra']}"</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='section-title'>☀️ Five Limbs of the Day (Panchangam)</div>", unsafe_allow_html=True)
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            st.markdown(f"<div class='card'><span class='panchangam-title'>🌙 Thithi (Lunar Phase)</span><span style='font-size:1.15rem; font-weight:500;'>{cal['thithi']}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card'><span class='panchangam-title'>🌟 Nakshatram (Star Mansion)</span><span style='font-size:1.15rem; font-weight:500;'>{cal['nakshatram']}</span></div>", unsafe_allow_html=True)
        with col_p2:
            st.markdown(f"<div class='card'><span class='panchangam-title'>📅 Vaaram (Solar Day)</span><span style='font-size:1.15rem; font-weight:500;'>{cal['vaaram']}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card'><span class='panchangam-title'>⚡ Yogam (Planetary Angle)</span><span style='font-size:1.15rem; font-weight:500;'>{cal['yogam']}</span></div>", unsafe_allow_html=True)
        with col_p3:
            st.markdown(f"<div class='card'><span class='panchangam-title'>🌀 Karanam (Half-Thithi)</span><span style='font-size:1.15rem; font-weight:500;'>{cal['karanam']}</span></div>", unsafe_allow_html=True)
            st.markdown(f"""<div class='card'>
                <span class='panchangam-title'>📍 Astro Coordinates Ledger</span>
                <span style='font-size:0.95rem; color:#444;'>
                    City: <b>{u['pob']}</b> &nbsp;|&nbsp; Time: <b>{u['tob']}</b><br/>
                    Gotram: <b>{u['gotram']}</b> &nbsp;|&nbsp; Nakshatram: <b>{u['known_star']}</b><br/>
                    Active Cycle: <b>{u['current_dasha']}</b>
                </span>
            </div>""", unsafe_allow_html=True)
            
        st.markdown("<div class='section-title'>⏳ Comprehensive Timing Gauges of the Day</div>", unsafe_allow_html=True)
        col_g, col_b = st.columns(2)
        with col_g:
            st.markdown(f"<div class='time-alert' style='border-left: 5px solid #4CAF50;'><b style='color:#2E7D32;'>✨ Abhijit Muhurtham:</b> {cal['abhijit_muhurtham']}<br/><small>Highly auspicious solar mid-day light. Ideal for asset acquisition and transactions.</small></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='time-alert' style='border-left: 5px solid #4CAF50;'><b style='color:#2E7D32;'>🌅 Amrita Kaalam:</b> {cal['amrita_kaalam']}<br/><small>Optimal cosmic stream for internal meditations and japa mantra alignment.</small></div>", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"<div class='time-alert' style='border-left: 5px solid #F44336;'><b style='color:#C62828;'>🚫 Rahu Kaalam:</b> {cal['rahukaalam']}<br/><small>High planetary gravity window. Postpone signing business contracts or initializing journeys.</small></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='time-alert' style='border-left: 5px solid #F44336;'><b style='color:#C62828;'>⚡ Durmuhurtham:</b> {cal['durmuhurtham']}<br/><small>Frictional alignment window. Postpone major presentations or launch execution cycles.</small></div>", unsafe_allow_html=True)

    # MODULE 2B: DEDICATED EXCLUSIVE DOUBTS CHAT ENGINE
    elif app_mode == "💬 Rishi Chat Engine":
        st.markdown("<h1>💬 Ancient Rishi Doubt Triage</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-header'>Submit your explicit doubts, blockages, or questions directly to the Rishi council</p>", unsafe_allow_html=True)
        
        def get_rishi_response(chat_query):
            system_prompt = (
                f"You are an ancient, completely omniscient Vedic Rishi counseling a seeker named {u['name']}.\n"
                f"Their astro profile metrics are: Gotram Clan: {u['gotram']}, Declared Birth Star: {u['known_star']}, Active Maha Dasha Time: {u['current_dasha']}.\n\n"
                f"Your exclusive purpose in this module is to resolve their explicit personal doubts, confusion, or spiritual problems.\n"
                f"Guidelines:\n"
                f"1. Acknowledge their question with immense compassion and direct clarity. Focus on boosting their confidence.\n"
                f"2. Contextualize your counsel slightly around their focus area timeline ({u['focus']}) and their active Dasha timeline if specified.\n"
                f"3. To anchor your answer, always close your message by reminding them of today's anchors: Lucky Color: {freq['color']}, Lucky Number: {freq['number']}, and the Sanskrit mantra: '{freq['mantra']}'.\n"
                f"4. Keep your tone serene, authoritative, and completely direct to the point."
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
                return f"🪐 The astral fields are heavy right now. Please re-send your query shortly."

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

    # MODULE 2C: EDIT PROFILE CONFIGURATION HUBS
    elif app_mode == "⚙️ Edit Profile Data":
        st.markdown("<h1>⚙️ Edit Profile Configuration</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-header'>Modify your astrological parameters or clear your session records completely</p>", unsafe_allow_html=True)
        
        st.subheader("🔄 Update Your Active Values")
        with st.form("edit_profile_form"):
            new_name = st.text_input("Edit Name", value=u["name"])
            new_pob = st.text_input("Edit Birth Location", value=u["pob"])
            new_gotram = st.text_input("Edit Gotram Lineage", value=u["gotram"])
            new_star = st.text_input("Edit Known Nakshatram", value=u["known_star"])
            new_focus = st.selectbox("Edit Timeline Focus", ["Career & Abundance Growth", "Inner Peace & Stability", "Harmonizing Relationships", "Health & Vitality"], index=["Career & Abundance Growth", "Inner Peace & Stability", "Harmonizing Relationships", "Health & Vitality"].index(u["focus"]))
            
            save_edit = st.form_submit_button("💾 Save Local Configuration Changes")
            if save_edit:
                st.session_state.user_profile.update({
                    "name": new_name, "pob": new_pob, "gotram": new_gotram, "known_star": new_star, "focus": new_focus
                })
                
                # STRINGIFY SYNC PAYLOAD BACK INTO THE DEVICE BROWSER
                updated_json = json.dumps(st.session_state.user_profile)
                st.components.v1.html(f"""
                    <script>try {{ window.parent.localStorage.setItem("vedic_seeker_profile", `{updated_json}`); }} catch(e) {{}}</script>
                """, height=0, width=0)
                st.success("Configuration modifications updated locally inside browser memory!")
                st.rerun()
                
        st.write("---")
        st.subheader("🛑 Master Session Reset")
        st.write("Clicking below wipes all stored local caches, logging you out completely to accept a brand new user registration:")
        if st.button("🚪 Clear Session Profile & Log Out"):
            st.components.v1.html("""
                <script>
                    try {
                        window.parent.localStorage.removeItem("vedic_seeker_profile");
                        window.parent.location.href = window.parent.location.origin + window.parent.location.pathname;
                    } catch(e) {}
                </script>
            """, height=0, width=0)
            st.session_state.registered = False
            st.session_state.user_profile = {}
            st.session_state.chat_history = []
            st.stop()
