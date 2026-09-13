import streamlit as st
from auth import is_logged_in, login, register

st.title("🔐 Account")

if is_logged_in():
    st.success(f"You are logged in as **{st.session_state.username}**.")
    st.info("Authentication is included as a placeholder for future features.")
else:
    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            if login(username.strip(), password):
                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with register_tab:
        with st.form("register_form"):
            new_username = st.text_input("Choose a username")
            new_password = st.text_input("Choose a password", type="password")
            submitted = st.form_submit_button(
                "Create account",
                use_container_width=True,
            )

        if submitted:
            if not new_username.strip() or not new_password:
                st.error("Username and password are required.")
            elif len(new_password) < 6:
                st.error("Password must contain at least 6 characters.")
            elif register(new_username.strip(), new_password):
                st.success("Account created. You can now log in.")
            else:
                st.error("That username already exists.")
