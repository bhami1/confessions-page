import streamlit as st
from database import get_confessions

st.title("👀 View Confessions")
st.caption("Browse the latest anonymous whispers.")

confessions = get_confessions(limit=100)

if not confessions:
    st.info("No confessions have been submitted yet.")
else:
    for confession in confessions:
        st.markdown(
            f"""
            <div style="
                padding: 18px;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                margin-bottom: 14px;
            ">
                <div style="font-size: 1.05rem;">
                    {confession["content"]}
                </div>
                <div style="color:#9ca3af; margin-top:10px; font-size:0.85rem;">
                    Anonymous · {confession["created_at"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
