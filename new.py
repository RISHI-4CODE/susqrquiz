import streamlit as st
import random
import time

st.set_page_config(page_title="Eco Reward", layout="centered")

# ---------- Custom CSS (Premium Styling + Animations) ----------
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.main-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    animation: fadeIn 1.2s ease-in-out;
}

.title {
    text-align: center;
    font-size: 32px;
    font-weight: 600;
    color: white;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #cfd8dc;
    margin-bottom: 30px;
}

.riddle {
    color: white;
    font-size: 18px;
    margin-bottom: 20px;
}

.reward {
    text-align: center;
    font-size: 26px;
    font-weight: 600;
    color: #00e676;
    animation: reveal 1.5s ease forwards;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(30px);}
    to {opacity: 1; transform: translateY(0);}
}

@keyframes reveal {
    from {opacity: 0; letter-spacing: 5px;}
    to {opacity: 1; letter-spacing: 1px;}
}
</style>
""", unsafe_allow_html=True)

# ---------- Riddles ----------
riddles = [
    {"question": "I turn waste into something new. I am one of the three R's. What am I?", "answer": "recycle"},
    {"question": "Two wheels, no fuel, I move without smoke. What am I?", "answer": "bicycle"},
    {"question": "I shine above and power homes without fire. What am I?", "answer": "sun"},
    {"question": "Turn me off when unused to reduce consumption. What am I?", "answer": "light"},
    {"question": "I fall from the sky and can be stored for sustainability. What am I?", "answer": "rain"},
]

# ---------- Session Control ----------
if "riddle" not in st.session_state:
    st.session_state.riddle = random.choice(riddles)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

# ---------- UI ----------
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.markdown('<div class="title">Unlock Your Eco Reward</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Solve one sustainability riddle to reveal your exclusive benefit.</div>', unsafe_allow_html=True)

st.markdown(f'<div class="riddle">{st.session_state.riddle["question"]}</div>', unsafe_allow_html=True)

answer = st.text_input("Your Answer")

if st.button("Submit"):

    if st.session_state.attempts >= 3:
        st.error("Maximum attempts reached.")
    else:
        if answer.lower().strip() == st.session_state.riddle["answer"]:
            st.session_state.unlocked = True
        else:
            st.session_state.attempts += 1
            st.warning(f"Incorrect. Attempts remaining: {3 - st.session_state.attempts}")

# ---------- Reward ----------
if st.session_state.unlocked:
    with st.spinner("Verifying response..."):
        time.sleep(2.5)

    st.markdown('<div class="reward">GREENEARTH20</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
