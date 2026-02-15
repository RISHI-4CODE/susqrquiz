import streamlit as st
import random
import time
import base64

st.set_page_config(page_title="Eco Reward", layout="centered")

# ---------- Load Background ----------
def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

bg_image = get_base64_image("new.jpg")

# ---------- Premium Styling ----------
st.markdown(f"""
<style>

[data-testid="stAppViewContainer"] {{
    background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.75)),
                url("data:image/jpg;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

html, body {{
    font-family: 'Inter', sans-serif;
}}

.card {{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(25px);
    padding: 50px;
    border-radius: 22px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
    animation: fadeIn 1.2s ease-in-out;
}}

.title {{
    text-align:center;
    font-size:34px;
    font-weight:600;
    color:white;
}}

.subtitle {{
    text-align:center;
    color:#d0d0d0;
    margin-bottom:30px;
}}

.riddle {{
    color:white;
    font-size:18px;
    margin-bottom:20px;
}}

.pattern {{
    text-align:center;
    font-size:32px;
    letter-spacing:12px;
    margin-bottom:30px;
}}

.reward {{
    text-align:center;
    font-size:28px;
    font-weight:600;
    color:#00ff9d;
    animation: reveal 1.5s ease forwards;
}}

@keyframes fadeIn {{
    from {{opacity:0; transform:translateY(40px);}}
    to {{opacity:1; transform:translateY(0);}}
}}

@keyframes reveal {{
    from {{opacity:0; letter-spacing:8px;}}
    to {{opacity:1; letter-spacing:2px;}}
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

# ---------- Session Setup ----------
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

# ---------- UI ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown('<div class="title">Unlock Your Eco Reward</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Solve the riddle using the letter clues below.</div>', unsafe_allow_html=True)

st.markdown(f'<div class="riddle">{st.session_state.riddle["question"]}</div>', unsafe_allow_html=True)

# Hidden Input
user_input = st.text_input("Answer", label_visibility="collapsed")

# Build Pattern Display
display = ""
typed_index = 0

for i, letter in enumerate(answer_word):
    if i in revealed_indices:
        display += f"<span style='color:#90caf9'>{letter.upper()}</span> "
    else:
        if typed_index < len(user_input):
            display += f"<span style='color:white'>{user_input[typed_index].upper()}</span> "
            typed_index += 1
        else:
            display += "<span style='color:white; opacity:0.4;'>_</span> "

st.markdown(f"<div class='pattern'>{display}</div>", unsafe_allow_html=True)

# ---------- Submit Logic ----------
if st.button("Submit"):

    if st.session_state.attempts >= 3:
        st.error("Maximum attempts reached.")
    else:
        if user_input.lower().strip() == answer_word:
            st.session_state.unlocked = True
        else:
            st.session_state.attempts += 1
            st.warning(f"Incorrect. Attempts remaining: {3 - st.session_state.attempts}")

# ---------- Reward ----------
if st.session_state.unlocked:
    with st.spinner("Verifying response..."):
        time.sleep(2)

    st.markdown('<div class="reward">GREENEARTH20</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
