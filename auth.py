"""Small authentication/session helper for the placeholder portal."""

import streamlit as st
from database import create_user, verify_user


def is_logged_in() -> bool:
    return bool(st.session_state.get("authenticated", False))


def login(username: str, password: str) -> bool:
    if verify_user(username, password):
        st.session_state.authenticated = True
        st.session_state.username = username
        return True
    return False


def register(username: str, password: str) -> bool:
    return create_user(username, password)


def logout_user():
    st.session_state.authenticated = False
    st.session_state.pop("username", None)
