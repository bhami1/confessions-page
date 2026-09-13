import streamlit as st
from database import initialize_database, get_confessions
from auth import is_logged_in, logout_user

st.set_page_config(
    page_title="Whispers",
    page_icon="🤫",
    layout="centered",
    initial_sidebar_state="expanded",
)

initialize_database()

# ---------- Styling ----------
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .confession-card {
        padding: 1.2rem;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        margin-bottom: 1rem;
        background: #ffffff;
    }
    .confession-meta {
        color: #9ca3af;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🤫 Whispers")
    st.caption("Anonymous confession portal")
    st.divider()

    if is_logged_in():
        st.success(f"Logged in as **{st.session_state.username}**")
        if st.button("Log out", use_container_width=True):
            logout_user()
            st.rerun()

# ---------- Home ----------
st.markdown('<div class="main-title">Whispers</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">A simple place to share thoughts anonymously.</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_Submit_Confession.py", label="✍️ Submit Confession")

with col2:
    st.page_link("pages/2_View_Confessions.py", label="👀 View Confessions")

st.divider()

st.subheader("Recent whispers")

confessions = get_confessions(limit=3)

if not confessions:
    st.info("No confessions yet. Be the first to share one.")
else:
    for confession in confessions:
        st.markdown(
            f"""
            <div class="confession-card">
                <div>{confession["content"]}</div>
                <div class="confession-meta">
                    Anonymous · {confession["created_at"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
