import streamlit as st
import random
import time
import os
import base64

# Set page config first
st.set_page_config(
    page_title="Eco Reward",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- PATCHED CSS ----------------
st.markdown("""
<style>
/* 1. Eliminate all Streamlit default headers and footers */
header, footer, .stDeployButton, [data-testid="stToolbar"], [data-testid="stHeader"] {
    display: none !important;
    visibility: hidden !important;
}

/* 2. Reset the main container spacing */
.main .block-container {
    padding-top: 2rem !important; /* Small top padding for balance */
    padding-bottom: 2rem !important;
    max-width: 600px;
}

/* 3. Remove the specific ghost block / empty divs at the top */
[data-testid="stVerticalBlock"] > div:first-child {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* 4. The Glass Card Styling */
.card {
    background: rgba(255, 255, 255, 0.07);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    margin-top: 0px;
    text-align: center;
}

/* 5. Typography and Elements */
.title {
    font-size: 32px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 15px;
}

.riddle {
    font-size: 18px;
    color: #e0e0e0;
    margin-bottom: 30px;
    line-height: 1.5;
}

.puzzle {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: 12px;
    color: #00ff9d;
    margin-bottom: 40px;
    text-transform: uppercase;
}

/* Fix input field styling to match dark theme */
div[data-baseweb="input"] {
    background-color: rgba(255,255,255,0.05) !important;
    border-radius: 10px !important;
}

input {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------- BACKGROUND IMAGE HANDLER ----------------
def load_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

bg_base64 = load_base64("new.jpg")

if bg_base64:
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.85)),
                    url("data:image/jpg;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)


# ---------------- GAME LOGIC & SESSION STATE ----------------
riddles = [
    {"question": "I turn waste into something new. I am one of the three R's. What am I?", "answer": "recycle"},
    {"question": "Two wheels, no fuel, I move without smoke. What am I?", "answer": "bicycle"},
    {"question": "I shine above and power homes without fire. What am I?", "answer": "sunlight"},
    {"question": "I fall from the sky and can be stored for sustainability. What am I?", "answer": "rainwater"},
]

if "riddle" not in st.session_state:
    st.session_state.riddle = random.choice(riddles)

if "revealed" not in st.session_state:
    word_len = len(st.session_state.riddle["answer"])
    st.session_state.revealed = random.sample(range(word_len), min(3, word_len))

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

answer_word = st.session_state.riddle["answer"]
revealed_indices = st.session_state.revealed

# Prepare the underscores
display_word = "".join([
    (letter.upper() if i in revealed_indices else "_") + " " 
    for i, letter in enumerate(answer_word)
])


# ---------------- MAIN UI RENDERING ----------------
# Wrap everything in the card div
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown(f'<div class="title">Unlock Your Eco Reward</div>', unsafe_allow_html=True)
st.markdown(f'<div class="riddle">{st.session_state.riddle["question"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="puzzle">{display_word}</div>', unsafe_allow_html=True)

# Input logic
if not st.session_state.unlocked and st.session_state.attempts < 3:
    # Use label_visibility="collapsed" to prevent extra vertical space
    user_input = st.text_input("Answer", label_visibility="collapsed", placeholder="Type your answer here...").strip().lower()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Submit Answer", use_container_width=True):
            if user_input == answer_word:
                st.session_state.unlocked = True
                st.rerun()
            else:
                st.session_state.attempts += 1
                if st.session_state.attempts < 3:
                    st.toast(f"Incorrect! {3 - st.session_state.attempts} tries left.", icon="⚠️")

if st.session_state.attempts >= 3 and not st.session_state.unlocked:
    st.error(f"Game Over! The answer was: {answer_word.upper()}")
    if st.button("Try a New Riddle"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Reward Display
if st.session_state.unlocked:
    st.balloons()
    st.success("Correct! You've earned a reward.")
    st.markdown("### Your Coupon Code:")
    st.code("GREENEARTH20", language=None)
    st.markdown("Flat ₹100 OFF at **ashvanta.in**")
    
    if st.button("Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)