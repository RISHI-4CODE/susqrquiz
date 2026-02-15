import streamlit as st
import random
import time
import base64

st.set_page_config(page_title="Eco Reward", layout="centered")

# ---------- Image Loader ----------
def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

bg_image = get_base64_image("new.jpg")

# ---------- Styling ----------
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.85)),
                url("data:image/jpg;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.card {{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(25px);
    padding: 50px;
    border-radius: 22px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.6);
}}

.title {{
    text-align:center;
    font-size:30px;
    font-weight:600;
    color:white;
    margin-bottom:20px;
}}

.riddle {{
    color:white;
    font-size:18px;
    margin-bottom:20px;
}}

.puzzle {{
    text-align:center;
    font-size:32px;
    letter-spacing:12px;
    color:white;
    margin-bottom:25px;
}}

.reward {{
    text-align:center;
    font-size:28px;
    font-weight:600;
    color:#00ff9d;
}}
</style>
""", unsafe_allow_html=True)

# ---------- Riddles ----------
riddles = [
    {"question": "I turn waste into something new. I am one of the three R's. What am I?", "answer": "recycle"},
    {"question": "Two wheels, no fuel, I move without smoke. What am I?", "answer": "bicycle"},
    {"question": "I shine above and power homes without fire. What am I?", "answer": "sunlight"},
    {"question": "I fall from the sky and can be stored for sustainability. What am I?", "answer": "rainwater"},
]

# ---------- Session ----------
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

# ---------- Generate Puzzle ----------
display_word = ""
for i, letter in enumerate(answer_word):
    if i in revealed_indices:
        display_word += letter.upper() + " "
    else:
        display_word += "_ "

# ---------- UI ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="title">Unlock Your Eco Reward</div>', unsafe_allow_html=True)
st.markdown(f'<div class="riddle">{st.session_state.riddle["question"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="puzzle">{display_word}</div>', unsafe_allow_html=True)

# ---------- Input ----------
if not st.session_state.unlocked and st.session_state.attempts < 3:
    user_input = st.text_input("Enter your answer:").strip().lower()

    if st.button("Submit"):
        if user_input == answer_word:
            st.session_state.unlocked = True
        else:
            st.session_state.attempts += 1
            st.warning(f"Incorrect. Attempts remaining: {3 - st.session_state.attempts}")

# ---------- Attempts Exhausted ----------
if st.session_state.attempts >= 3 and not st.session_state.unlocked:
    st.error("Maximum attempts reached.")

# ---------- Reward ----------
if st.session_state.unlocked:
    with st.spinner("Verifying response..."):
        time.sleep(1.2)
    st.markdown('<div class="reward">GREENEARTH20</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
