import random
import sys
from pathlib import Path

# Ensure root directory is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from database import add_confession
from styles import apply_custom_styles, CATEGORIES, render_cet_header

st.set_page_config(
    page_title="Submit Whisper — College of Engineering Trivandrum",
    layout="centered",
)

PROMPTS = [
    "I have had a secret crush on someone from the architecture block since Dhwani...",
    "To whoever was studying late in the CET Central Library on the second floor yesterday...",
    "The biggest thing I've learned during my time at College of Engineering Trivandrum is...",
    "To the person sitting across from me at the canteen who smiled back...",
    "My honest feeling about this semester's lab evaluations is...",
    "I still feel grateful to the senior who helped me navigate CET on my first week...",
    "If I could tell my first-year self one piece of advice before entering CET...",
]

# Track selected category to enable dynamic ambience shifting
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = "Romance & Crush"

topic_options = [c for c in CATEGORIES if c != "All Topics"]

# Radio/selector for category placed before form to trigger dynamic background instantly
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 12px;">
        <span class="cet-badge">College of Engineering Trivandrum • Anonymous Submission</span>
    </div>
    """,
    unsafe_allow_html=True,
)

current_mood = st.session_state.selected_topic
apply_custom_styles(mood=current_mood)

render_cet_header(subtitle="Compose your anonymous reflection. The background ambience adapts to your chosen mood.")

# Ambience Selector
selected_category = st.selectbox(
    "Select Topic / Ambience",
    options=topic_options,
    index=topic_options.index(st.session_state.selected_topic) if st.session_state.selected_topic in topic_options else 0,
    help="Selecting 'Romance & Crush' activates the rose twilight ambience.",
)

# Update session state if changed to trigger dynamic background
if selected_category != st.session_state.selected_topic:
    st.session_state.selected_topic = selected_category
    st.rerun()

# Interactive Inspiration Prompt
if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""

prompt_col1, prompt_col2 = st.columns([3, 1])
with prompt_col1:
    st.markdown(
        f"""
        <div style="
            background: rgba(255, 255, 255, 0.04);
            border: 1px dashed rgba(255, 255, 255, 0.15);
            border-radius: 10px;
            padding: 10px 16px;
            font-size: 0.88rem;
            color: #cbd5e1;
            min-height: 44px;
            display: flex;
            align-items: center;
        ">
            Prompt: <em>{st.session_state.current_prompt or 'Need inspiration? Click Generate Prompt to load a suggestion.'}</em>
        </div>
        """,
        unsafe_allow_html=True,
    )

with prompt_col2:
    if st.button("Generate Prompt", use_container_width=True):
        st.session_state.current_prompt = random.choice(PROMPTS)
        st.rerun()

st.write("")

with st.form("confession_form"):
    confession = st.text_area(
        "Your Confession",
        placeholder=st.session_state.current_prompt or "Write your thought here. Submissions are strictly anonymous...",
        height=190,
        max_chars=2000,
    )

    char_count = len(confession) if confession else 0
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; font-size: 0.78rem; color: #94a3b8; margin-top: -8px; margin-bottom: 12px;">
            <span>Strictly Anonymous • Salted SHA-256 Hashing</span>
            <span>{char_count} / 2000 characters</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    submitted = st.form_submit_button(
        "Release Whisper Anonymously",
        use_container_width=True,
    )

if submitted:
    if not confession.strip():
        st.error("Please enter your thoughts before submitting.")
    else:
        success = add_confession(
            content=confession,
            category=selected_category,
            ip_address="placeholder-client",
        )

        if success:
            st.success("Your confession has been published anonymously to the CET wall.")
            st.session_state.current_prompt = ""
            col_a, col_b = st.columns(2)
            with col_a:
                st.page_link("pages/2_View_Confessions.py", label="Browse Confessions Wall", use_container_width=True)
            with col_b:
                st.page_link("app.py", label="Return to Home", use_container_width=True)
        else:
            st.error("An error occurred while publishing. Please try again.")

# Confidentiality card
st.markdown(
    """
    <div style="
        margin-top: 26px;
        background: rgba(19, 27, 46, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
        padding: 16px 20px;
        font-size: 0.82rem;
        color: #94a3b8;
        line-height: 1.6;
    ">
        <strong style="color: #f1f5f9;">CET Privacy Policy:</strong>
        Whispers operates on zero-identity logging. No user credentials or raw network addresses are bound to submissions.
        Please keep all confessions respectful and abide by campus community standards.
    </div>
    """,
    unsafe_allow_html=True,
)
