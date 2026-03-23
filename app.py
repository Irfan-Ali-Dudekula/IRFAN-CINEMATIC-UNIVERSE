import streamlit as st
from tmdbv3api import TMDb, Movie, Discover, Search

# --- 1. CONFIG (Using Secrets for 100% Success) ---
st.set_page_config(page_title="IRFAN CINEMATIC UNIVERSE", layout="wide")

tmdb = TMDb()
# This looks for the secret you just saved in Streamlit Settings
try:
    tmdb.api_key = st.secrets["TMDB_API_KEY"]
except:
    tmdb.api_key = 'a3ce43541791ff5e752a8e62ce0fcde2' # Fallback

movie_api, discover_api, search_api = Movie(), Discover(), Search()

# --- 2. SESSION & STYLES ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

def apply_royal_styles():
    bg_img = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070"
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Poppins:wght@400&display=swap');
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("{bg_img}"); background-size: cover; background-attachment: fixed; }}
        .royal-title {{ font-family: 'Playfair Display', serif; font-size: 60px; text-align: center; color: #FCF6BA; text-shadow: 2px 4px 10px #000; }}
        .movie-card {{ background: rgba(0,0,0,0.8); padding: 20px; border-radius: 15px; border: 1px solid #BF953F; text-align: center; margin-bottom: 20px; }}
        [data-testid="stSidebar"] {{ background: #000 !important; border-right: 2px solid #BF953F; }}
        h3, p, span {{ color: white !important; }}
        </style>
    """, unsafe_allow_html=True)

apply_royal_styles()

# --- 3. LOGIN GATE ---
if not st.session_state.logged_in:
    st.markdown('<h1 class="royal-title">IRFAN CINEMATIC UNIVERSE</h1>', unsafe_allow_html=True)
    u_name = st.text_input("Enter Access Name")
    if st.button("Access the Vault") and u_name:
        st.session_state.logged_in = True
        st.rerun()
else:
    st.markdown('<h1 class="royal-title">IRFAN CINEMATIC UNIVERSE</h1>', unsafe_allow_html=True)
    
    # Sidebar
    mood_algo = {"Happy": "35", "Sad": "18", "Thrill": "53"}
    lang_map = {"Telugu": "te", "Hindi": "hi", "Tamil": "ta", "English": "en"}
    
    sel_mood = st.sidebar.selectbox("Mood", list(mood_algo.keys()))
    sel_lang = st.sidebar.selectbox("Language", list(lang_map.keys()))
    
    # --- FETCH DATA ---
    with st.spinner("Accessing TMDB Vault..."):
        movies = discover_api.discover_movies({
            'with_genres': mood_algo[sel_mood],
            'with_original_language': lang_map[sel_lang],
            'sort_by': 'popularity.desc'
        })
    
    # --- DISPLAY ---
    if movies:
        cols = st.columns(3)
        for i, m in enumerate(list(movies)[:12]):
            with cols[i % 3]:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                st.image(f"https://image.tmdb.org/t/p/w500{m.poster_path}")
                st.markdown(f"<h3>{m.title}</h3>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("API Connection Error: No movies returned. Please check your Secrets settings.")
