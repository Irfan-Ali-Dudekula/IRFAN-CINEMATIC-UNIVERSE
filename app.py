import streamlit as st
from tmdbv3api import TMDb, Movie, Discover, Search

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="IRFAN CINEMATIC UNIVERSE", layout="wide")

tmdb = TMDb()
# Hard-coded for immediate success
tmdb.api_key = 'a3ce43541791ff5e752a8e62ce0fcde2'
tmdb.language = 'en'

movie_api, discover_api, search_api = Movie(), Discover(), Search()

# --- 2. OLD UI STYLES (Clean & Classic) ---
def apply_classic_styles():
    st.markdown("""
        <style>
        .main { background-color: #0e1117; color: white; }
        .stApp { background: #000000; }
        .title-text { 
            text-align: center; color: #FFD700; 
            font-size: 50px; font-weight: bold; 
            text-shadow: 2px 2px 4px #444; 
        }
        .movie-card {
            background-color: #1c1c1c;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #FFD700;
            margin-bottom: 20px;
            text-align: center;
        }
        h3 { color: #FFD700 !important; font-size: 18px; }
        p { color: #cccccc !important; font-size: 14px; }
        </style>
    """, unsafe_allow_html=True)

apply_classic_styles()

# --- 3. THE EXPANDED ALGORITHM ---
# Mapping friendly names to TMDB Genre IDs
mood_map = {
    "Happy / Laughter": "35",
    "Sad / Emotional": "18",
    "Thrill / Fear": "53,27",
    "Mystery / Suspense": "9648",
    "Action / Bravery": "28,12",
    "Romantic / Love": "10749",
    "Sci-Fi / Future": "878",
    "War / History": "10752,36",
    "Family / Animation": "10751,16",
    "Crime / Dark": "80"
}

lang_map = {
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "English": "en",
    "Malayalam": "ml",
    "Kannada": "kn",
    "Punjabi": "pa"
}

# --- 4. LOGIN & SIDEBAR ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<h1 class="title-text">IRFAN CINEMATIC UNIVERSE</h1>', unsafe_allow_html=True)
    name = st.text_input("Enter Access Name:")
    if st.button("Access Vault") and name:
        st.session_state.logged_in = True
        st.rerun()
else:
    st.markdown('<h1 class="title-text">IRFAN CINEMATIC UNIVERSE</h1>', unsafe_allow_html=True)
    
    st.sidebar.header("Filter the Vault")
    sel_mood = st.sidebar.selectbox("Select Emotion", list(mood_map.keys()))
    sel_lang = st.sidebar.selectbox("Select Language", list(lang_map.keys()))
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- 5. THE SEARCH & DISCOVERY ENGINE ---
    with st.spinner("Searching the Universe..."):
        # Discovery Logic
        movies = discover_api.discover_movies({
            'with_genres': mood_map[sel_mood],
            'with_original_language': lang_map[sel_lang],
            'sort_by': 'popularity.desc'
        })
        
        # Force conversion to list to prevent "NoneType" errors
        movies_list = list(movies) if movies else []

    # --- 6. DISPLAY GRID ---
    if movies_list:
        cols = st.columns(4) # 4 movies per row for the old UI look
        for i, m in enumerate(movies_list[:16]):
            with cols[i % 4]:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                # Fallback for missing posters
                p_url = f"https://image.tmdb.org/t/p/w500{m.poster_path}" if getattr(m, 'poster_path', None) else "https://via.placeholder.com/500x750?text=No+Poster"
                st.image(p_url, use_container_width=True)
                st.markdown(f"<h3>{getattr(m, 'title', 'Unknown Title')}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p>⭐ {getattr(m, 'vote_average', 0.0)}</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("No movies found for this combination. Please try a different Emotion or Language.")
