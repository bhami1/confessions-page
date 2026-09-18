"""
chatbot_helper.py — Gemini-backed version.

Setup:
  pip install google-genai
  Add GEMINI_API_KEY to .streamlit/secrets.toml (local) or your app's
  Secrets settings (Streamlit Community Cloud).

Get a free Gemini API key at: https://aistudio.google.com/apikey
"""

import streamlit as st
from google import genai

MODEL = "gemini-3.6-flash"

SYSTEM_PROMPT = (
    "You are the CET Whispers Assistant, a friendly helper for students using "
    "the College of Engineering Trivandrum (CET) anonymous confession portal. "
    "Answer questions helpfully and concisely. Keep replies short and warm."
)


def _get_client() -> genai.Client:
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Add it to .streamlit/secrets.toml locally, "
            "or to your app's Secrets in Streamlit Community Cloud settings."
        )
    return genai.Client(api_key=api_key)


def get_chatbot_response(user_message: str, history: list | None = None) -> str:
    """
    Send a message (with optional prior turns) and return the reply text.

    history, if given, should be a list of {"role": "user"/"assistant", "content": str}
    dicts (same shape used elsewhere in this app).
    """
    client = _get_client()

    # Convert this app's {"role": "user"/"assistant", "content": ...} history
    # into Gemini's expected format ("assistant" -> "model") without
    # re-calling the API for each past turn.
    gemini_history = []
    if history:
        for msg in history:
            role = "model" if msg["role"] == "assistant" else "user"
            gemini_history.append({"role": role, "parts": [{"text": msg["content"]}]})

    chat = client.chats.create(
        model=MODEL,
        config={"system_instruction": SYSTEM_PROMPT},
        history=gemini_history,
    )

    response = chat.send_message(user_message)
    return response.text.strip()