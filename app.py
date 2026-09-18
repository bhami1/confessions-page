import streamlit as st
from database import (
    initialize_database,
    seed_demo_data,
    get_confessions,
    get_confession_stats,
    like_confession,
    dislike_confession,
)
from auth import is_logged_in, logout_user
from styles import apply_custom_styles, render_cet_header

st.set_page_config(
    page_title="Whispers — College of Engineering Trivandrum",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_database()
seed_demo_data()

# Check ambience preference
if "app_mood" not in st.session_state:
    st.session_state.app_mood = "default"

# ---------- Sidebar ----------
with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand-box">
            <span style="
                background: #112d26;
                color: #34d399;
                padding: 3px 10px;
                border-radius: 6px;
                font-size: 0.7rem;
                font-weight: 700;
                letter-spacing: 0.05em;
            ">
                ESTD. 1939
            </span>
            <div style="margin-top: 14px; position: relative;">
                <svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="1.6" style="opacity: 0.85;">
                    <path d="M12 22v-9"></path>
                    <path d="M9 13a3 3 0 0 1-3-3c0-1.7 1.3-3 3-3 .3 0 .7.1 1 .2C10.5 5.4 12 4 14 4c2.2 0 4 1.8 4 4 0 .3 0 .7-.1 1 1.7.5 3 2 3 3.8 0 2.3-1.9 4.2-4.2 4.2H9z"></path>
                </svg>
                <h2 style="font-size: 1.45rem; font-weight: 700; margin: 8px 0 2px 0; color: #ffffff;">
                    CET Whispers
                </h2>
                <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.06em;">
                    College of Engineering Trivandrum
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='margin-top: 18px; font-size: 0.8rem; color: #94a3b8;'>Campus Ambience:</div>", unsafe_allow_html=True)
    ambience_options = [
        "Default Twilight",
        "Romance & Crush",
        "CET Campus Life",
        "Deep Reflections",
        "Campus Humor",
        "Life & Advice",
    ]
    curr_idx = 0
    if st.session_state.app_mood in ambience_options:
        curr_idx = ambience_options.index(st.session_state.app_mood)

    ambience_choice = st.selectbox(
        "Ambience",
        options=ambience_options,
        index=curr_idx,
        label_visibility="collapsed",
    )
    new_mood = "default" if ambience_choice == "Default Twilight" else ambience_choice
    if new_mood != st.session_state.app_mood:
        st.session_state.app_mood = new_mood
        st.rerun()

    st.write("")
    st.write("")

    # Authenticated Member section
    current_user = st.session_state.get("username")
    st.markdown(
        f"""
        <div style="
            background: rgba(14, 30, 24, 0.7);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 12px;
        ">
            <div style="font-size: 0.72rem; color: #34d399; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em;">
                AUTHENTICATED MEMBER
            </div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 2px;">
                @{current_user}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.page_link("pages/4_CET_Assistant.py", label="Open CET Assistant")

    st.markdown(
        """
        <div style="margin-top: 28px; padding-top: 14px; border-top: 1px solid rgba(255,255,255,0.06);">
            <div style="display: flex; align-items: center; gap: 8px;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5">
                    <path d="M12 22v-9"></path>
                    <path d="M9 13a3 3 0 0 1-3-3c0-1.7 1.3-3 3-3 .3 0 .7.1 1 .2C10.5 5.4 12 4 14 4c2.2 0 4 1.8 4 4 0 .3 0 .7-.1 1 1.7.5 3 2 3 3.8 0 2.3-1.9 4.2-4.2 4.2H9z"></path>
                </svg>
                <span style="font-size: 0.84rem; font-weight: 700; color: #cbd5e1;">CET Whispers</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Apply dynamic styles based on ambient mood
apply_custom_styles(mood=st.session_state.app_mood)

# ---------- Top Header ----------
render_cet_header()

# Centered Content Layout
col_left_pad, col_center, col_right_pad = st.columns([0.15, 0.7, 0.15])

with col_center:
    # 1. Taped Confession Card
    featured_confessions = get_confessions(limit=1, sort_by="popular")
    if not featured_confessions:
        featured_c = {
            "id": 1234,
            "content": "Found a forgotten Rs 100 note in my old lab coat during practicals. Treat time at the canteen! 🤫 #SmallJoys #CETLife",
            "likes": 48,
            "dislikes": 2,
        }
    else:
        featured_c = featured_confessions[0]

    # HTML Card with diagonal washi/scotch tape
    st.markdown(
        f"""
        <div class="taped-card-container">
            <div class="tape-tr"></div>
            <div class="tape-bl"></div>
            <div class="taped-card-text">
                {featured_c['content']}
            </div>
            <div class="taped-card-sub">
                Confession #{featured_c['id']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Action buttons row right below card
    btn_col1, btn_col2, btn_col3, btn_col_pad = st.columns([1, 1, 1.5, 4])
    with btn_col1:
        if st.button(f"👍 {featured_c.get('likes', 0)}", key=f"like_{featured_c['id']}", help="Like"):
            like_confession(featured_c["id"])
            st.rerun()
    with btn_col2:
        if st.button(f"👎 {featured_c.get('dislikes', 0)}", key=f"dislike_{featured_c['id']}", help="Dislike"):
            dislike_confession(featured_c["id"])
            st.rerun()
    with btn_col3:
        if st.button("💬 Comment", key=f"comment_{featured_c['id']}"):
            st.session_state.show_comment_box = not st.session_state.get("show_comment_box", False)

    if st.session_state.get("show_comment_box", False):
        c_input = st.text_input("Add a supportive reply:", key="comm_input", placeholder="Share your reply...")
        if st.button("Post Reply", key="btn_post_reply"):
            if c_input.strip():
                st.success("Reply recorded.")
                st.session_state.show_comment_box = False
                st.rerun()

    st.write("")
    st.write("")

    # 2. Metrics Row
    stats = get_confession_stats()
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown(
            f"""
            <div class="metric-card-mockup">
                <div class="val">{stats['total_confessions']}</div>
                <div class="lbl">WHISPERS POSTED</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m_col2:
        st.markdown(
            f"""
            <div class="metric-card-mockup">
                <div class="val">{stats['total_likes']}</div>
                <div class="lbl">APPRECIATIONS</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m_col3:
        st.markdown(
            f"""
            <div class="metric-card-mockup">
                <div class="val">{stats['total_users']}</div>
                <div class="lbl">ACTIVE MEMBER</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.write("")

    # 3. Action Cards Row
    act1, act2, act3 = st.columns(3)
    with act1:
        st.markdown(
            """
            <div class="action-card-mockup">
                <div>
                    <span class="action-badge">SUBMISSIONS</span>
                    <div class="action-title">Submit a Whisper</div>
                    <div class="action-desc">
                        Share your campus memory, crush, or secret with dynamic ambient mood lighting.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link("pages/1_Submit_Confession.py", label="Write Confession", use_container_width=True)

    with act2:
        st.markdown(
            """
            <div class="action-card-mockup">
                <div>
                    <span class="action-badge">WALL FEED</span>
                    <div class="action-title">Confessions Wall</div>
                    <div class="action-desc">
                        Explore echoes, search keywords, filter by romance or campus life, and give appreciations.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link("pages/2_View_Confessions.py", label="Browse Wall", use_container_width=True)

    with act3:
        st.markdown(
            """
            <div class="action-card-mockup">
                <div>
                    <span class="action-badge">MEMBER ACCESS</span>
                    <div class="action-title">Member Portal</div>
                    <div class="action-desc">
                        Sign in to participate, access the campus assistant, and manage your account.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link("pages/3_Login.py", label="Open Account", use_container_width=True)
