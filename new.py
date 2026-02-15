import streamlit as st
import random
import time
import os
import base64

st.set_page_config(
    page_title="Eco Reward",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- REMOVE ALL STREAMLIT DEFAULT SPACING ----------------
st.markdown("""
<style>

/* Remove EVERYTHING above app */
header {display: none !important;}
footer {display: none !important;}
[data-testid="stToolbar"] {display: none !important;}
[data-testid="stHeader"] {display: none !important;}

/* Remove top app wrapper spacing */
html, body, [data-testid="stAppViewContainer"] {
    margin: 0 !important;
    padding: 0 !important;
}

/* Remove main container padding */
.block-container {
    padding: 0 !important;
    margin: 0 !important;
}

/* Remove internal wrapper spacing */
[data-testid="stAppViewContainer"] > .main {
    padding: 0 !important;
    margin: 0 !important;
}

/* Remove first empty vertical block */
[data-testid="stVerticalBlock"] > div:first-child {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* Force card to stick to top */
.card {
    margin-top: 0 !important;
    width: 600px;
    max-width: 92%;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(25px);
    padding: 60px;
    border-radius: 24px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.7);
}

/* Title Styling */
.title {
    text-align:center;
    font-size:28px;
    font-weight:500;
    color:white;
    margin-top: 0 !important;
    margin-bottom:20px;
}

.riddle {
    color:white;
    font-size:18px;
    margin-bottom:25px;
    text-align:center;
}

.puzzle {
    text-align:center;
    font-size:34px;
    letter-spacing:14px;
    color:white;
    margin-bottom:30px;
}

</style>
""", unsafe_allow_html=True)



# ---------------- BASE64 BACKGROUND ----------------
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
        background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.85)),
                    url("data:image/jpg;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)


# ---------------- RIDDLES ----------------
riddles = [
    {"question": "I turn waste into something new. I am one of the three R's. What am I?", "answer": "recycle"},
    {"question": "Two wheels, no fuel, I move without smoke. What am I?", "answer": "bicycle"},
    {"question": "I shine above and power homes without fire. What am I?", "answer": "sunlight"},
    {"question": "I fall from the sky and can be stored for sustainability. What am I?", "answer": "rainwater"},
]


# ---------------- SESSION STATE ----------------
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


# ---------------- PUZZLE DISPLAY ----------------
display_word = ""
for i, letter in enumerate(answer_word):
    if i in revealed_indices:
        display_word += letter.upper() + " "
    else:
        display_word += "_ "


# ---------------- UI ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown('<div class="title">Unlock Your Eco Reward</div>', unsafe_allow_html=True)
st.markdown(f'<div class="riddle">{st.session_state.riddle["question"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="puzzle">{display_word}</div>', unsafe_allow_html=True)


# ---------------- INPUT ----------------
if not st.session_state.unlocked and st.session_state.attempts < 3:
    user_input = st.text_input("", placeholder="Enter your answer").strip().lower()

    if st.button("Submit"):
        if user_input == answer_word:
            st.session_state.unlocked = True
        else:
            st.session_state.attempts += 1
            st.warning(f"Incorrect. Attempts remaining: {3 - st.session_state.attempts}")

if st.session_state.attempts >= 3 and not st.session_state.unlocked:
    st.error("Maximum attempts reached.")


# ---------------- REWARD ----------------
if st.session_state.unlocked:
    with st.spinner("Verifying response..."):
        time.sleep(1.2)

    st.success("Congratulations! You unlocked your reward.")
    st.markdown("### This is your coupon code for ₹100 flat on all products at **ashvanta.in**")
    st.code("GREENEARTH20", language=None)

st.markdown('</div>', unsafe_allow_html=True)
