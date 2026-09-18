# Whispers — Streamlit Anonymous Confession Portal

A modern, visually stunning anonymous confession portal built with Streamlit and SQLite. Designed with an ambient dark-twilight aurora theme, glassmorphic cards, custom typography, reaction hearts, category filters, and live search.

## Features

- 🌌 **Ambient Twilight Aurora Theme**: Deep dark palette (`#0B0F19`) layered with multi-point glowing radial gradients.
- 🪟 **Glassmorphism UI**: Semi-transparent frosted cards with luminous border accents, smooth hover elevations, and responsive typography (`Outfit` and `Plus Jakarta Sans`).
- 🏷️ **Categorized Whispers**: Filter and tag confessions across vibrant topics (💜 Secret, 💖 Crush & Love, 🎓 College Life, 💡 Deep Thoughts, 🎭 Funny & Wild, 🌿 Life & Advice).
- ❤️ **Interactive Reactions**: Live heart/like counters with instant upvotes.
- 🎲 **Spark Inspiration**: Interactive random prompt generator on the submission page.
- 🔍 **Search & Sort**: Filter confessions by keyword or category, and sort by newest or most loved.
- 🔐 **Member Accounts & Safe Space**: Multi-tab authentication system and community guidelines sidebar.

## Architecture

```text
User
 │
 ├── Submit Confession ──> pages/1_Submit_Confession.py ──> database.py ──> SQLite
 │
 ├── View Wall        ──> pages/2_View_Confessions.py   ──> database.py ──> SQLite
 │
 └── Member Account   ──> pages/3_Login.py              ──> auth.py     ──> SQLite
```

## Project Structure

```text
confessions-page/
├── app.py                      # Main landing page & community pulse
├── auth.py                     # Authentication and session helper
├── database.py                 # SQLite database layer with auto-migrations
├── styles.py                   # Centralized CSS, theme, and card components
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── functions_used.html         # Quick reference cheat-sheet
├── .streamlit/
│   └── config.toml             # Streamlit theme & UI configurations
├── pages/
│   ├── 1_Submit_Confession.py  # Submission page with prompt generator
│   ├── 2_View_Confessions.py   # Confession wall with search & filter
│   └── 3_Login.py              # Member sign in & registration
└── data/
    └── whispers.db             # Auto-generated SQLite database
```

## Run Locally

### 1. Create a Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Streamlit

```bash
streamlit run app.py
```

The application will launch at `http://localhost:8501`.

## Important Notes for Production

- IP addresses are salted and hashed with SHA-256 for privacy.
- Passwords are encrypted with SHA-256 (upgrade to bcrypt or Argon2 for production).
- Add rate limiting and content moderation filters before public deployment.
