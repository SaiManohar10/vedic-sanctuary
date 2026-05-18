import streamlit as st
import datetime
import requests
from groq import Groq

# 1. SECURE KEY CONFIGURATION (Looks into Streamlit Secrets Vault)
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
elif "groq_api_key" in st.session_state:
    GROQ_API_KEY = st.session_state["groq_api_key"]
else:
    GROQ_API_KEY = ""

# Connect cleanly to the free Groq client if key is available
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# 2. DESIGN THE SACRED SPACE (THEME & STYLING)
st.set_page_config(page_title="The Vedic Sanctuary", page_icon="🔱", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background-color: #FAF9F6; }
    h1 { color: #E65C00; font-family: 'Georgia', serif; text-align: center; font-size: 3rem; }
    .stButton>button { background-color: #E65C00; color: white; border-radius: 25px; font-weight: bold; }
    .stTextInput>div>div>input { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔱 The Vedic Sanctuary")
st.markdown("<p style='text-align: center; color: #666;'>Speak with your personal Guru. Receive timeless cosmic counsel.</p>", unsafe_allow_html=True)
st.write("---")

# 3. SIDEBAR: THE DATA COLLECTION PANEL
st.sidebar.header("📜 Your Sacred Birth Details")
seeker_name = st.sidebar.text_input("Your Name", value="Manohar")
dob = st.sidebar.date_input("Date of Birth", datetime.date(1998, 6, 10))
tob = st.sidebar.time_input("Exact Time of Birth")
pob = st.sidebar.text_input("Place of Birth", value="Hyderabad, India")
life_goal = st.sidebar.selectbox("Your Core Focus", ["Career & Abundance Growth", "Inner Peace & Stability", "Harmonizing Relationships", "Health & Vitality"])

# Backup fallback slot in sidebar if secrets aren't deployed yet
if not GROQ_API_KEY:
    st.sidebar.warning("⚠️ Key Needed Below:")
    input_key = st.sidebar.text_input("Enter Groq API Key", type="password")
    if input_key:
        st.session_state["groq_api_key"] = input_key
        st.rerun()

st.sidebar.write("---")
st.sidebar.header("💞 Divine Union Sync (Partner)")
has_partner = st.sidebar.checkbox("Link Partner's Profile")
partner_name = "None"
if has_partner:
    partner_name = st.sidebar.text_input("Partner's Name", value="Beloved")

# 4. FETCH COSMIC DATA
@st.cache_data(ttl=3600)
def fetch_sandbox_astrology():
    try:
        res = requests.get("https://api.vedika.io/sandbox/v2/astrology/prediction/daily?sign=aries")
        if res.status_code == 200:
            return {
                "rashi": "Mesha (Aries)", "nakshatra": "Bharani",
                "good_time": "11:45 AM to 12:33 PM (Abhijit Muhurtham)",
                "color": "Saffron (Deep Orange)", "number": "9"
            }
    except:
        pass
    return {
        "rashi": "Mesha (Aries)", "nakshatra": "Ashwini",
        "good_time": "11:42 AM to 12:30 PM", "color": "Saffron & Royal Gold", "number": "3"
    }

cosmic_data = fetch_sandbox_astrology()

# 5. THE BRAIN: CHAT GENERATION ENGINE
def get_guru_response(user_message):
    if not client:
        return "⚠️ **System Update Needed:** Please add your valid Groq API key in the sidebar dashboard to activate your Guru."

    system_instruction = (
        "You are an ancient, omniscient Vedic Rishi and a deeply compassionate divine guru. "
        "You speak with serene authority, immense warmth, and absolute cosmic wisdom. "
        "Never mention software, computer code, prompts, parameters, or APIs. Speak directly to the soul.\n\n"
        "Rules:\n"
        "1. Address the user intimately as 'My child' or 'Dear seeker'.\n"
        "2. Weave their personal life goal, current planetary energies, and daily anchors seamlessly into your advice.\n"
        "3. If they discuss friction, a birthday, or their partner, offer a soul-aligning Sanskrit chant or practical ritual.\n"
        "4. Format your output beautifully with emojis and line breaks."
    )

    context_package = (
        f"--- COSMIC PROFILE FOR TODAY ---\n"
        f"Seeker's Name: {seeker_name}\n"
        f"Primary Goal: {life_goal}\n"
        f"Partner's Name: {partner_name}\n"
        f"Today's Transiting Moon: {cosmic_data['rashi']}\n"
        f"Peak Good Hour: {cosmic_data['good_time']}\n"
        f"Auspicious Color: {cosmic_data['color']}\n"
        f"Lucky Number: {cosmic_data['number']}\n"
        f"---------------------------------\n"
        f"User Message: {user_message}"
    )

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": context_package}
            ],
            temperature=0.6,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"🪐 Cosmic connection error: {str(e)}"

# 6. INTERACTIVE CHAT CORE LOOP
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display history
for chat in st.session_state.chat_history:
    avatar_icon = "✨" if chat["role"] == "assistant" else "👤"
    with st.chat_message(chat["role"], avatar=avatar_icon):
        st.markdown(chat["content"])

# Catch User Input
if user_query := st.chat_input("Ask your Guru about your day, career paths, or guidance..."):
    # Append user question
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_query)
        
    # Generate Guru Answer dynamically
    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Reflecting on the cosmic paths..."):
            guru_reply = get_guru_response(user_query)
            st.markdown(guru_reply)
            st.session_state.chat_history.append({"role": "assistant", "content": guru_reply})
