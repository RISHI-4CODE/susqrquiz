import streamlit as st
import random
import time
import base64
import streamlit.components.v1 as components

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
    animation: fadeIn 1.2s ease-in-out;
}}

.title {{
    text-align:center;
    font-size:30px;
    font-weight:600;
    color:white;
    margin-bottom:10px;
}}

.subtitle {{
    text-align:center;
    color:#cccccc;
    margin-bottom:25px;
}}

.riddle {{
    color:white;
    font-size:18px;
    margin-bottom:20px;
}}

.reward {{
    text-align:center;
    font-size:28px;
    font-weight:600;
    color:#00ff9d;
    animation: reveal 1.2s ease forwards;
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

# ---------- Card ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown('<div class="title">Unlock Your Eco Reward</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Solve the riddle using the letter clues below.</div>', unsafe_allow_html=True)
st.markdown(f'<div class="riddle">{st.session_state.riddle["question"]}</div>', unsafe_allow_html=True)

# ---------- Puzzle Component ----------
typed_value = components.html(f"""
<script src="https://unpkg.com/streamlit-component-lib/dist/index.js"></script>

<style>
.puzzle-container {{
    text-align:center;
    font-size:32px;
    letter-spacing:14px;
    color:white;
    margin-bottom:30px;
}}

.letter {{
    border-bottom:2px solid white;
    display:inline-block;
    width:32px;
    text-align:center;
}}

.revealed {{
    color:#90caf9;
    border-bottom:none;
}}

.hidden-input {{
    position:absolute;
    opacity:0;
}}
button {{
    margin-top:20px;
    padding:10px 25px;
    background:#111;
    color:white;
    border:none;
    border-radius:6px;
    cursor:pointer;
}}
</style>

<div class="puzzle-container" id="puzzle"></div>
<input type="text" id="hiddenInput" class="hidden-input" autofocus />
<button onclick="submitAnswer()">Submit</button>

<script>
const answer = "{answer_word}";
const revealed = {revealed_indices};
let userInput = "";

const puzzle = document.getElementById("puzzle");
const hiddenInput = document.getElementById("hiddenInput");

function render() {{
    puzzle.innerHTML = "";
    let typedIndex = 0;

    for (let i = 0; i < answer.length; i++) {{
        let span = document.createElement("span");
        span.classList.add("letter");

        if (revealed.includes(i)) {{
            span.textContent = answer[i].toUpperCase();
            span.classList.add("revealed");
        }} else {{
            if (typedIndex < userInput.length) {{
                span.textContent = userInput[typedIndex].toUpperCase();
                typedIndex++;
            }} else {{
                span.textContent = "";
            }}
        }}
        puzzle.appendChild(span);
    }}
}}

hiddenInput.addEventListener("input", function(e) {{
    userInput = e.target.value.replace(/[^a-zA-Z]/g, "");
    render();
}});

hiddenInput.addEventListener("keydown", function(e) {{
    if (e.key === "Enter") {{
        submitAnswer();
    }}
}});

function submitAnswer() {{
    Streamlit.setComponentValue(userInput);
}}

render();
</script>
""", height=240)

# ---------- Validate Answer ----------
if typed_value:
    if st.session_state.attempts >= 3:
        st.error("Maximum attempts reached.")
    else:
        if typed_value.lower().strip() == answer_word:
            st.session_state.unlocked = True
        else:
            st.session_state.attempts += 1
            st.warning(f"Incorrect. Attempts remaining: {3 - st.session_state.attempts}")

# ---------- Reward ----------
if st.session_state.unlocked:
    with st.spinner("Verifying response..."):
        time.sleep(1.5)
    st.markdown('<div class="reward">GREENEARTH20</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
