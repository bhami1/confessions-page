# Whispers — Streamlit Placeholder Portal

A clean starter/placeholder implementation of an anonymous confession portal.

## Architecture

```text
User
 │
 ├── Submit Confession ──> Streamlit ──> database.py ──> SQLite
 │
 └── View Confessions <── Streamlit <── database.py <── SQLite
```

Authentication is separated into `auth.py`.

## Project structure

```text
whispers_streamlit_placeholder/
├── app.py
├── auth.py
├── database.py
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml
├── pages/
│   ├── 1_Submit_Confession.py
│   ├── 2_View_Confessions.py
│   └── 3_Login.py
└── data/
    └── whispers.db   # created automatically
```

## Run locally

### 1. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Streamlit

```bash
streamlit run app.py
```

The browser should open the portal automatically.

## Demo data

Run this once if you want placeholder confessions:

```bash
python -c "from database import initialize_database, seed_demo_data; initialize_database(); seed_demo_data()"
```

## Important

This is a learning/placeholder implementation, not a production-ready anonymous platform.

Before production, review:
- authentication and password hashing
- CSRF/session security
- input sanitization
- moderation
- rate limiting
- abuse prevention
- privacy policy and IP handling
- database credentials/secrets
- MySQL migration
