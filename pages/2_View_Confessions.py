import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from database import get_confessions, get_confession_stats, like_confession, dislike_confession
from styles import apply_custom_styles, render_top_header, CATEGORIES

st.set_page_config(
    page_title="Confessions Wall — College of Engineering Trivandrum",
    layout="wide",
)

if "wall_category" not in st.session_state:
    st.session_state.wall_category = "All Topics"

active_mood = st.session_state.wall_category if st.session_state.wall_category != "All Topics" else "default"
apply_custom_styles(mood=active_mood)

render_top_header()

# Search and Filter Toolbar
col_search, col_sort = st.columns([3, 2])
with col_search:
    search_query = st.text_input(
        "Search whispers",
        placeholder="Search whispers by keyword...",
        label_visibility="collapsed",
    )

with col_sort:
    sort_option = st.selectbox(
        "Sort Order",
        options=["Newest First", "Most Appreciated"],
        label_visibility="collapsed",
    )

selected_category = st.radio(
    "Filter by Category",
    options=CATEGORIES,
    index=CATEGORIES.index(st.session_state.wall_category) if st.session_state.wall_category in CATEGORIES else 0,
    horizontal=True,
    label_visibility="collapsed",
)

if selected_category != st.session_state.wall_category:
    st.session_state.wall_category = selected_category
    st.rerun()

st.write("")

# Query confessions
sort_key = "popular" if "Most Appreciated" in sort_option else "latest"
confessions = get_confessions(
    limit=50,
    category=selected_category if selected_category != "All Topics" else None,
    search_query=search_query,
    sort_by=sort_key,
)

if not confessions:
    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 40px 20px;
            background: rgba(19, 27, 46, 0.4);
            border: 1px dashed rgba(255, 255, 255, 0.12);
            border-radius: 14px;
            margin-top: 15px;
        ">
            <h3 style="color: #f1f5f9; font-size: 1.2rem; margin-bottom: 6px;">No Confessions Found</h3>
            <p style="color: #94a3b8; font-size: 0.9rem; max-width: 420px; margin: 0 auto 16px auto;">
                There are currently no confessions recorded under this topic filter.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.page_link("pages/1_Submit_Confession.py", label="Write the First Whisper", use_container_width=True)
else:
    for c in confessions:
        st.markdown(
            f"""
            <div class="taped-card-container">
                <div class="tape-tr"></div>
                <div class="tape-bl"></div>
                <div class="taped-card-text">
                    {c['content']}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #94a3b8;">
                    <span>Confession #{c['id']}</span>
                    <span class="action-badge" style="margin-bottom: 0;">{c.get('category', 'CET Campus Life')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        b1, b2, b_pad = st.columns([1, 1, 8])
        with b1:
            if st.button(f"👍 {c.get('likes', 0)}", key=f"wall_like_{c['id']}"):
                like_confession(c["id"])
                st.rerun()
        with b2:
            if st.button(f"👎 {c.get('dislikes', 0)}", key=f"wall_dislike_{c['id']}"):
                dislike_confession(c["id"])
                st.rerun()
        st.write("")
