import sys
from pathlib import Path

# Ensure root directory is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from auth import is_logged_in
from chatbot_helper import get_chatbot_response
from styles import apply_custom_styles, render_cet_header

st.set_page_config(
    page_title="CET Assistant — Whispers",
    layout="centered",
)

apply_custom_styles(mood="CET Campus Life")

render_cet_header(subtitle="College of Engineering Trivandrum • Interactive Campus Assistant")

if not is_logged_in():
    st.markdown(
        """
        <div style="
            background: rgba(19, 27, 46, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 14px;
            padding: 32px 28px;
            text-align: center;
            backdrop-filter: blur(16px);
            margin-top: 15px;
        ">
            <span class="cet-badge" style="margin-bottom: 12px;">Member Privilege</span>
            <h2 style="font-size: 1.8rem; margin: 12px 0 8px 0;">Sign in to Access the CET Assistant</h2>
            <p style="color: #94a3b8; font-size: 0.98rem; max-width: 480px; margin: 0 auto 24px auto; line-height: 1.6;">
                The interactive CET Assistant is an exclusive feature reserved for registered members. 
                Creating an account takes seconds, and your confession submissions remain strictly anonymous.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.page_link("pages/3_Login.py", label="Go to Member Sign In / Register", use_container_width=True)

else:
    st.markdown(
        f"""
        <div style="
            background: rgba(16, 185, 129, 0.08);
            border: 1px solid rgba(16, 185, 129, 0.25);
            border-radius: 12px;
            padding: 12px 18px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        ">
            <span style="font-size: 0.88rem; color: #6ee7b7;">
                Authenticated Session: <strong>{st.session_state.username}</strong>
            </span>
            <span class="tag-pill" style="background: rgba(16, 185, 129, 0.2); color: #a7f3d0; border-color: rgba(16, 185, 129, 0.4);">
                Assistant Unlocked
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize chat history
    if "cet_chat_messages" not in st.session_state:
        st.session_state.cet_chat_messages = [
            {
                "role": "assistant",
                "content": "Hello! I am your CET Whispers Assistant. Ask me about submitting confessions, anonymity policies, campus spots like OAT and Central Library, or portal features."
            }
        ]

    # Quick prompt buttons
    st.caption("Suggested Questions:")
    q_col1, q_col2, q_col3 = st.columns(3)
    with q_col1:
        if st.button("How is anonymity secured?", use_container_width=True):
            st.session_state.pending_prompt = "How is my anonymity protected?"
    with q_col2:
        if st.button("Tell me about CET spots", use_container_width=True):
            st.session_state.pending_prompt = "What are the popular spots in CET?"
    with q_col3:
        if st.button("Romantic confessions theme", use_container_width=True):
            st.session_state.pending_prompt = "Tell me about romantic confessions and the rose twilight theme"

    # Display chat history
    for msg in st.session_state.cet_chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Handle input
    prompt = st.chat_input("Type your question here...")
    if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
        prompt = st.session_state.pop("pending_prompt")

    if prompt:
        st.session_state.cet_chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        response = get_chatbot_response(prompt)
        st.session_state.cet_chat_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
