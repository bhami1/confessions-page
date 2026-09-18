"""
Centralized styling and UI component module for Whispers — College of Engineering Trivandrum (CET).
Features realistic washi/scotch tape confession cards, dynamic ambient backgrounds,
and minimal collegiate typography.
"""

import streamlit as st


CATEGORIES = [
    "All Topics",
    "Romance & Crush",
    "CET Campus Life",
    "Confidential Secret",
    "Deep Reflections",
    "Campus Humor",
    "Life & Advice",
]

MOOD_PRESETS = {
    "default": {
        "bg_color": "#070e17",
        "radial": """
            radial-gradient(circle at 20% 20%, rgba(14, 165, 233, 0.12) 0%, transparent 45%),
            radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.12) 0%, transparent 45%),
            radial-gradient(circle at 50% 85%, rgba(16, 185, 129, 0.08) 0%, transparent 50%),
            #070e17
        """,
        "accent": "#38bdf8",
        "border": "rgba(56, 189, 248, 0.25)",
        "pill_bg": "rgba(56, 189, 248, 0.12)",
        "pill_text": "#7dd3fc",
    },
    "Romance & Crush": {
        "bg_color": "#120812",
        "radial": """
            radial-gradient(circle at 20% 20%, rgba(244, 63, 94, 0.22) 0%, transparent 45%),
            radial-gradient(circle at 80% 20%, rgba(251, 113, 133, 0.16) 0%, transparent 45%),
            radial-gradient(circle at 50% 85%, rgba(219, 39, 119, 0.18) 0%, transparent 50%),
            #120812
        """,
        "accent": "#f43f5e",
        "border": "rgba(244, 63, 94, 0.35)",
        "pill_bg": "rgba(244, 63, 94, 0.15)",
        "pill_text": "#fda4af",
    },
    "CET Campus Life": {
        "bg_color": "#061316",
        "radial": """
            radial-gradient(circle at 20% 20%, rgba(16, 185, 129, 0.20) 0%, transparent 45%),
            radial-gradient(circle at 80% 20%, rgba(14, 165, 233, 0.16) 0%, transparent 45%),
            radial-gradient(circle at 50% 85%, rgba(5, 150, 105, 0.14) 0%, transparent 50%),
            #061316
        """,
        "accent": "#10b981",
        "border": "rgba(16, 185, 129, 0.35)",
        "pill_bg": "rgba(16, 185, 129, 0.15)",
        "pill_text": "#6ee7b7",
    },
    "Confidential Secret": {
        "bg_color": "#0a0815",
        "radial": """
            radial-gradient(circle at 20% 20%, rgba(147, 51, 234, 0.22) 0%, transparent 45%),
            radial-gradient(circle at 80% 20%, rgba(99, 102, 241, 0.18) 0%, transparent 45%),
            radial-gradient(circle at 50% 85%, rgba(88, 28, 135, 0.20) 0%, transparent 50%),
            #0a0815
        """,
        "accent": "#a855f7",
        "border": "rgba(168, 85, 247, 0.35)",
        "pill_bg": "rgba(168, 85, 247, 0.15)",
        "pill_text": "#d8b4fe",
    },
    "Deep Reflections": {
        "bg_color": "#060b17",
        "radial": """
            radial-gradient(circle at 20% 20%, rgba(59, 130, 246, 0.20) 0%, transparent 45%),
            radial-gradient(circle at 80% 20%, rgba(99, 102, 241, 0.18) 0%, transparent 45%),
            radial-gradient(circle at 50% 85%, rgba(30, 58, 138, 0.22) 0%, transparent 50%),
            #060b17
        """,
        "accent": "#60a5fa",
        "border": "rgba(96, 165, 250, 0.35)",
        "pill_bg": "rgba(59, 130, 246, 0.15)",
        "pill_text": "#93c5fd",
    },
    "Campus Humor": {
        "bg_color": "#140e06",
        "radial": """
            radial-gradient(circle at 20% 20%, rgba(245, 158, 11, 0.20) 0%, transparent 45%),
            radial-gradient(circle at 80% 20%, rgba(217, 119, 6, 0.16) 0%, transparent 45%),
            radial-gradient(circle at 50% 85%, rgba(180, 83, 9, 0.14) 0%, transparent 50%),
            #140e06
        """,
        "accent": "#f59e0b",
        "border": "rgba(245, 158, 11, 0.35)",
        "pill_bg": "rgba(245, 158, 11, 0.15)",
        "pill_text": "#fcd34d",
    },
    "Life & Advice": {
        "bg_color": "#061314",
        "radial": """
            radial-gradient(circle at 20% 20%, rgba(20, 184, 166, 0.20) 0%, transparent 45%),
            radial-gradient(circle at 80% 20%, rgba(6, 182, 212, 0.16) 0%, transparent 45%),
            radial-gradient(circle at 50% 85%, rgba(15, 118, 110, 0.14) 0%, transparent 50%),
            #061314
        """,
        "accent": "#14b8a6",
        "border": "rgba(20, 184, 166, 0.35)",
        "pill_bg": "rgba(20, 184, 166, 0.15)",
        "pill_text": "#5eead4",
    },
}


def get_mood_preset(category_name):
    if not category_name:
        return MOOD_PRESETS["default"]
    for key, preset in MOOD_PRESETS.items():
        if key.lower() in category_name.lower():
            return preset
    return MOOD_PRESETS["default"]


def apply_custom_styles(mood="default"):
    preset = get_mood_preset(mood)

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

        /* App Background */
        .stApp {{
            background-color: {preset['bg_color']} !important;
            background-image: {preset['radial']} !important;
            background-attachment: fixed !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            color: #e2e8f0;
        }}

        header[data-testid="stHeader"] {{
            background: transparent !important;
        }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background-color: #070d18 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }}

        /* Native Sidebar Navigation Links */
        div[data-testid="stSidebarNav"] {{
            padding-top: 6px !important;
            padding-bottom: 8px !important;
        }}
        div[data-testid="stSidebarNav"] ul {{
            gap: 2px !important;
        }}
        div[data-testid="stSidebarNav"] li a {{
            border-radius: 8px !important;
            padding: 8px 14px !important;
            color: #94a3b8 !important;
            font-size: 0.92rem !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }}
        div[data-testid="stSidebarNav"] li a:hover {{
            background-color: rgba(255, 255, 255, 0.05) !important;
            color: #ffffff !important;
        }}
        div[data-testid="stSidebarNav"] li a[aria-current="page"] {{
            background-color: #182232 !important;
            color: #ffffff !important;
            font-weight: 600 !important;
        }}

        /* Headings */
        h1, h2, h3, h4 {{
            font-family: 'Outfit', sans-serif !important;
            color: #ffffff;
            letter-spacing: -0.02em;
        }}

        /* Taped Confession Card (Washi/Scotch Tape Effect) */
        .taped-card-container {{
            position: relative;
            background: rgba(18, 26, 42, 0.75);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 12px;
            padding: 24px 28px;
            margin: 18px 0 24px 0;
            box-shadow: 0 14px 32px -8px rgba(0, 0, 0, 0.5);
        }}

        .tape-tr {{
            position: absolute;
            top: -12px;
            right: -15px;
            width: 65px;
            height: 22px;
            background: rgba(220, 226, 238, 0.28);
            border: 1px solid rgba(255, 255, 255, 0.18);
            transform: rotate(36deg);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35);
            backdrop-filter: blur(2px);
            pointer-events: none;
            z-index: 5;
        }}

        .tape-bl {{
            position: absolute;
            bottom: -12px;
            left: -15px;
            width: 65px;
            height: 22px;
            background: rgba(220, 226, 238, 0.28);
            border: 1px solid rgba(255, 255, 255, 0.18);
            transform: rotate(36deg);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35);
            backdrop-filter: blur(2px);
            pointer-events: none;
            z-index: 5;
        }}

        .taped-card-text {{
            font-size: 1.05rem;
            line-height: 1.6;
            color: #f1f5f9;
            margin-bottom: 12px;
        }}

        .taped-card-sub {{
            font-size: 0.8rem;
            color: #94a3b8;
            margin-bottom: 14px;
        }}

        /* Metrics Display */
        .metric-card-mockup {{
            background: rgba(14, 21, 34, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 16px 12px;
            text-align: center;
        }}

        .metric-card-mockup .val {{
            font-family: 'Outfit', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 2px;
        }}

        .metric-card-mockup .lbl {{
            font-size: 0.72rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 600;
        }}

        /* Action Nav Cards */
        .action-card-mockup {{
            background: rgba(14, 21, 34, 0.65);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 18px 16px;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .action-badge {{
            display: inline-block;
            background: #1e2038;
            color: #a5b4fc;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 0.68rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 10px;
        }}

        .action-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 6px;
        }}

        .action-desc {{
            font-size: 0.8rem;
            color: #94a3b8;
            line-height: 1.5;
            margin-bottom: 16px;
        }}

        /* Buttons */
        .stButton > button {{
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 8px !important;
            color: #f1f5f9 !important;
            font-weight: 500 !important;
            font-size: 0.86rem !important;
        }}

        .stButton > button:hover {{
            background: rgba(255, 255, 255, 0.1) !important;
            border-color: rgba(255, 255, 255, 0.3) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_cet_header(
    subtitle="An anonymous reflection space for the College of Engineering Trivandrum student community. Share unspoken thoughts, campus echoes, and reflections freely.",
):
    """Renders the collegiate top header matching the mockup."""
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 4px; margin-bottom: 22px;">
            <div style="display: inline-flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <span style="
                    background: #153232;
                    color: #5eead4;
                    padding: 3px 12px;
                    border-radius: 6px;
                    font-size: 0.74rem;
                    font-weight: 700;
                    letter-spacing: 0.05em;
                ">
                    CET TVM • ESTD. 1939
                </span>
                <span style="font-size: 0.76rem; color: #94a3b8; letter-spacing: 0.06em; text-transform: uppercase; font-weight: 600;">
                    College of Engineering Trivandrum
                </span>
            </div>
            <h1 style="font-size: 3.2rem; font-weight: 800; margin: 0 0 6px 0; letter-spacing: -0.03em; color: #ffffff;">
                Whispers
            </h1>
            <p style="color: #94a3b8; font-size: 0.98rem; max-width: 640px; margin: 0 auto; line-height: 1.55;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Alias for backward compatibility
render_top_header = render_cet_header
