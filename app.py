import streamlit as st
import requests
import json
import sqlite3
import hashlib
from datetime import datetime
from mood_detector import detect_mood, MOODS
from tmdb_client import TMDBClient
import os

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Irfan Cinematic Universe",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Royal Gold & White CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Montserrat:wght@300;400;500;600&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
    background-color: #0a0a0a;
    color: #f5f0e8;
}

/* ── Royal Header ── */
.royal-header {
    text-align: center;
    padding: 2.5rem 1rem 1rem;
    background: linear-gradient(180deg, #1a1200 0%, #0a0a0a 100%);
    border-bottom: 2px solid #c9a84c;
    margin-bottom: 2rem;
}
.royal-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #c9a84c, #ffe08a, #c9a84c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 0;
}
.royal-subtitle {
    color: #a08030;
    font-size: 0.85rem;
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-top: 6px;
}
.gold-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #c9a84c, transparent);
    margin: 1rem auto;
    width: 60%;
}

/* ── Login Box ── */
.login-box {
    background: linear-gradient(145deg, #111100, #1c1700);
    border: 1px solid #c9a84c44;
    border-radius: 16px;
    padding: 2rem;
    max-width: 420px;
    margin: 0 auto;
    box-shadow: 0 0 40px #c9a84c22;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background-color: #111100 !important;
    color: #f5f0e8 !important;
    border: 1px solid #c9a84c55 !important;
    border-radius: 8px !important;
    font-family: 'Montserrat', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #c9a84c !important;
    box-shadow: 0 0 10px #c9a84c33 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #c9a84c, #a07830);
    color: #0a0a0a;
    border: none;
    border-radius: 30px;
    padding: 0.6rem 2rem;
    font-family: 'Montserrat', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    width: 100%;
}
.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 25px #c9a84c55;
}

/* ── Mood Badge ── */
.mood-badge {
    display: inline-block;
    background: linear-gradient(135deg, #c9a84c22, #c9a84c44);
    border: 1px solid #c9a84c;
    color: #ffe08a;
    padding: 6px 20px;
    border-radius: 30px;
    font-size: 0.9rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* ── Movie Card ── */
.movie-card {
    background: linear-gradient(145deg, #111100, #1a1500);
    border: 1px solid #c9a84c33;
    border-radius: 14px;
    padding: 0;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    height: 100%;
}
.movie-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 40px #c9a84c33;
    border-color: #c9a84c88;
}
.movie-poster {
    width: 100%;
    height: 280px;
    object-fit: cover;
    display: block;
}
.movie-info {
    padding: 1rem;
}
.movie-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #ffe08a;
    margin-bottom: 4px;
}
.movie-meta {
    color: #a08030;
    font-size: 0.78rem;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.movie-rating {
    color: #c9a84c;
    font-size: 0.85rem;
    margin-bottom: 6px;
}
.movie-overview {
    color: #ccbf9a;
    font-size: 0.8rem;
    line-height: 1.5;
    margin-bottom: 8px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.cast-list {
    color: #a08030;
    font-size: 0.75rem;
    font-style: italic;
    margin-bottom: 8px;
}

/* ── OTT Play Button ── */
.ott-btn {
    display: inline-block;
    background: linear-gradient(135deg, #c9a84c, #a07830);
    color: #0a0a0a !important;
    font-weight: 700;
    font-size: 0.78rem;
    letter-spacing: 1px;
    padding: 6px 14px;
    border-radius: 20px;
    text-decoration: none !important;
    margin: 3px 3px 0 0;
    transition: all 0.2s ease;
}
.ott-btn:hover {
    box-shadow: 0 0 14px #c9a84c99;
    transform: scale(1.04);
}

/* ── Admin Panel ── */
.admin-table {
    background: #111100;
    border: 1px solid #c9a84c33;
    border-radius: 10px;
    padding: 1rem;
}

/* ── Section Title ── */
.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.8rem;
    color: #c9a84c;
    letter-spacing: 2px;
    margin-bottom: 1rem;
    border-bottom: 1px solid #c9a84c33;
    padding-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Database Setup ────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("icu_users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS login_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            login_time TEXT,
            mood TEXT,
            language TEXT
        )
    """)
    # Create default admin
    admin_pw = hashlib.sha256("admin123".encode()).hexdigest()
    try:
        c.execute("INSERT INTO users (username, password, role, created_at) VALUES (?, ?, 'admin', ?)",
                  ("admin", admin_pw, datetime.now().isoformat()))
    except sqlite3.IntegrityError:
        pass
    conn.commit()
    conn.close()

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def register_user(username, password):
    conn = sqlite3.connect("icu_users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role, created_at) VALUES (?, ?, 'user', ?)",
                  (username, hash_pw(password), datetime.now().isoformat()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect("icu_users.db")
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, hash_pw(password)))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def log_login(username, mood="", language=""):
    conn = sqlite3.connect("icu_users.db")
    c = conn.cursor()
    c.execute("INSERT INTO login_history (username, login_time, mood, language) VALUES (?, ?, ?, ?)",
              (username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), mood, language))
    conn.commit()
    conn.close()

def get_login_history():
    conn = sqlite3.connect("icu_users.db")
    c = conn.cursor()
    c.execute("SELECT username, login_time, mood, language FROM login_history ORDER BY login_time DESC LIMIT 100")
    rows = c.fetchall()
    conn.close()
    return rows

# ── OTT Platform Links ────────────────────────────────────────────────────────
OTT_LINKS = {
    "Netflix": "https://www.netflix.com/search?q=",
    "Amazon Prime Video": "https://www.amazon.com/s?k=",
    "Disney+": "https://www.disneyplus.com/search/",
    "Apple TV+": "https://tv.apple.com/search?term=",
    "Hulu": "https://www.hulu.com/search?q=",
    "HBO Max": "https://play.max.com/search?q=",
    "Hotstar": "https://www.hotstar.com/in/search?q=",
    "ZEE5": "https://www.zee5.com/search?q=",
    "SonyLIV": "https://www.sonyliv.com/search?searchString=",
    "JioCinema": "https://www.jiocinema.com/search/",
    "Mubi": "https://mubi.com/en/search?q=",
    "YouTube": "https://www.youtube.com/results?search_query=",
}

def get_ott_buttons(providers, movie_title):
    html = ""
    for p in providers:
        for name, base_url in OTT_LINKS.items():
            if name.lower() in p.lower():
                url = base_url + movie_title.replace(" ", "+")
                html += f'<a class="ott-btn" href="{url}" target="_blank">▶ {name}</a>'
                break
    if not html:
        url = f"https://www.justwatch.com/in/search?q={movie_title.replace(' ', '+')}"
        html += f'<a class="ott-btn" href="{url}" target="_blank">🔍 Find on JustWatch</a>'
    return html

# ── Init ──────────────────────────────────────────────────────────────────────
init_db()
tmdb = TMDBClient(api_key=st.secrets.get("TMDB_API_KEY", os.getenv("TMDB_API_KEY", "")))

# ── Session State ─────────────────────────────────────────────────────────────
for k, v in {"logged_in": False, "username": "", "role": "", "page": "login"}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Royal Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="royal-header">
    <div class="royal-title">✦ Irfan Cinematic Universe ✦</div>
    <div class="gold-divider"></div>
    <div class="royal-subtitle">Mood · Cinema · Experience</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN / REGISTER PAGE
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        with tab1:
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            uname = st.text_input("Username", key="login_user")
            pwd = st.text_input("Password", type="password", key="login_pwd")
            if st.button("Enter the Universe", key="btn_login"):
                role = login_user(uname, pwd)
                if role:
                    st.session_state.logged_in = True
                    st.session_state.username = uname
                    st.session_state.role = role
                    log_login(uname)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials.")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            new_user = st.text_input("Choose Username", key="reg_user")
            new_pwd = st.text_input("Choose Password", type="password", key="reg_pwd")
            if st.button("Create Account", key="btn_reg"):
                if len(new_user) < 3 or len(new_pwd) < 4:
                    st.warning("Username ≥ 3 chars, Password ≥ 4 chars.")
                elif register_user(new_user, new_pwd):
                    st.success("✅ Account created! Please login.")
                else:
                    st.error("Username already taken.")
            st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN APP (Logged In)
# ══════════════════════════════════════════════════════════════════════════════
# ── Top Nav ───────────────────────────────────────────────────────────────────
nav_cols = st.columns([4, 1, 1])
with nav_cols[1]:
    if st.session_state.role == "admin":
        if st.button("👑 Admin Panel"):
            st.session_state.page = "admin" if st.session_state.page != "admin" else "home"
with nav_cols[2]:
    if st.button("🚪 Logout"):
        for k in ["logged_in", "username", "role"]:
            st.session_state[k] = False if k == "logged_in" else ""
        st.session_state.page = "login"
        st.rerun()

st.markdown(f"<p style='color:#a08030; font-size:0.82rem; margin-bottom:1rem;'>Welcome, <b style='color:#c9a84c'>{st.session_state.username}</b></p>", unsafe_allow_html=True)

# ── Admin Panel ───────────────────────────────────────────────────────────────
if st.session_state.page == "admin":
    st.markdown('<div class="section-title">👑 Admin — Login History</div>', unsafe_allow_html=True)
    history = get_login_history()
    if history:
        import pandas as pd
        df = pd.DataFrame(history, columns=["Username", "Login Time", "Mood", "Language"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No login history yet.")
    st.stop()

# ── Recommendation UI ─────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🎭 How are you feeling?</div>', unsafe_allow_html=True)

LANGUAGES = [
    "English", "Hindi", "Tamil", "Telugu", "Malayalam", "Kannada",
    "Bengali", "Marathi", "Punjabi", "Gujarati", "Urdu",
    "Korean", "Japanese", "French", "Spanish", "Italian",
    "German", "Turkish", "Arabic", "Portuguese", "Chinese (Mandarin)"
]

col_mood, col_lang = st.columns([2, 1])
with col_mood:
    mood_text = st.text_area(
        "Describe your mood or feeling...",
        placeholder="e.g. I feel nostalgic and want something emotional...",
        height=100
    )
with col_lang:
    language = st.selectbox("🌐 Language", LANGUAGES)

# Manual mood override
all_moods = list(MOODS.keys())
selected_mood = st.selectbox("Or pick a mood directly:", ["— Auto Detect —"] + all_moods)

if st.button("✦ Discover Movies ✦"):
    if not mood_text.strip() and selected_mood == "— Auto Detect —":
        st.warning("Please describe your mood or select one.")
    else:
        mood = selected_mood if selected_mood != "— Auto Detect —" else detect_mood(mood_text)
        log_login(st.session_state.username, mood, language)

        st.markdown(f'<div class="mood-badge">✦ Mood Detected: {mood.upper()} ✦</div>', unsafe_allow_html=True)

        with st.spinner("Curating your royal selection..."):
            movies = tmdb.get_movies_by_mood(mood, language=language)

        if not movies:
            st.error("No movies found. Check your TMDB API key or try a different mood.")
        else:
            st.markdown(f'<div class="section-title">🎬 Recommended for You</div>', unsafe_allow_html=True)
            cols = st.columns(4)
            for i, movie in enumerate(movies[:12]):
                with cols[i % 4]:
                    poster_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path','')}" if movie.get('poster_path') else "https://via.placeholder.com/300x450?text=No+Poster"
                    cast_str = ", ".join(movie.get("cast", [])[:4]) or "N/A"
                    providers = movie.get("providers", [])
                    ott_html = get_ott_buttons(providers, movie.get("title", ""))
                    rating = movie.get("vote_average", 0)
                    stars = "★" * int(rating / 2) + "☆" * (5 - int(rating / 2))

                    st.markdown(f"""
                    <div class="movie-card">
                        <img class="movie-poster" src="{poster_url}" alt="{movie.get('title','')}">
                        <div class="movie-info">
                            <div class="movie-title">{movie.get('title','Unknown')}</div>
                            <div class="movie-meta">{movie.get('release_date','')[:4] if movie.get('release_date') else 'N/A'} &nbsp;|&nbsp; {movie.get('original_language','').upper()}</div>
                            <div class="movie-rating">{stars} {rating:.1f}/10</div>
                            <div class="movie-overview">{movie.get('overview','No description available.')}</div>
                            <div class="cast-list">🎭 {cast_str}</div>
                            <div>{ott_html}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
