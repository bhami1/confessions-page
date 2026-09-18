import sys
from pathlib import Path

# Ensure root directory is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from auth import is_logged_in, login, register, logout_user
from database import get_confession_stats
from styles import apply_custom_styles, render_cet_header

st.set_page_config(
    page_title="Member Portal — College of Engineering Trivandrum",
    layout="centered",
)

apply_custom_styles(mood="default")
render_cet_header(subtitle="College of Engineering Trivandrum • Member Authentication & Privileges")

if is_logged_in():
    stats = get_confession_stats()
    st.markdown(
        f"""
        <div style="
            background: rgba(19, 27, 46, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 28px 24px;
            text-align: center;
            backdrop-filter: blur(16px);
            margin-bottom: 20px;
        ">
            <span class="cet-badge" style="margin-bottom: 12px;">Verified CET Member</span>
            <h2 style="font-size: 1.85rem; margin: 10px 0 6px 0;">{st.session_state.username}</h2>
            <p style="color: #94a3b8; font-size: 0.92rem; max-width: 460px; margin: 0 auto 20px auto; line-height: 1.6;">
                You are authenticated. Your member account unlocks the <strong>CET Assistant Chatbot</strong>, while ensuring your confession submissions remain strictly anonymous.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Unlocked Feature Card
    st.markdown(
        """
        <div style="
            background: rgba(16, 185, 129, 0.08);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 24px;
        ">
            <div style="font-weight: 700; color: #6ee7b7; font-size: 1.1rem; margin-bottom: 6px;">
                Feature Unlocked: CET Assistant Chatbot
            </div>
            <div style="color: #94a3b8; font-size: 0.88rem; line-height: 1.5; margin-bottom: 14px;">
                Ask the automated assistant about confession rules, privacy guarantees, campus spots, or portal themes.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.page_link("pages/4_CET_Assistant.py", label="Open CET Assistant Chatbot", use_container_width=True)
    with col2:
        if st.button("Sign Out of Session", use_container_width=True):
            logout_user()
            st.rerun()

else:
    # Benefits Card
    st.markdown(
        """
        <div style="
            background: rgba(19, 27, 46, 0.55);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 18px 22px;
            margin-bottom: 24px;
            font-size: 0.88rem;
            color: #cbd5e1;
            line-height: 1.6;
        ">
            <strong style="color: #ffffff;">Why Create a Member Account?</strong>
            <ul style="margin: 8px 0 0 0; padding-left: 20px; color: #94a3b8;">
                <li><strong>Unlock CET Assistant:</strong> Direct access to the intelligent campus helper chatbot.</li>
                <li><strong>Verified Participation:</strong> Engage with the community while confession postings remain 100% anonymous.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    login_tab, register_tab = st.tabs(["Sign In", "Create Account"])

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Sign In to Account", use_container_width=True)

        if submitted:
            if not username.strip() or not password:
                st.error("Please enter both username and password.")
            elif login(username.strip(), password):
                st.success("Authentication successful. Redirecting...")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with register_tab:
        with st.form("register_form"):
            new_username = st.text_input("Choose Username", placeholder="e.g. cetian_student")
            new_password = st.text_input("Choose Password", type="password", placeholder="At least 6 characters")
            submitted = st.form_submit_button("Register New Account", use_container_width=True)

        if submitted:
            if not new_username.strip() or not new_password:
                st.error("Username and password are required.")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters.")
            elif register(new_username.strip(), new_password):
                st.success("Account created successfully. You may now sign in.")
            else:
                st.error("Username already taken. Please choose another.")
