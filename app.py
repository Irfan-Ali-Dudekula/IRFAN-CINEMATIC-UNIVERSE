import streamlit as st
from tmdbv3api import TMDb, Movie, Discover, Search

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="IRFAN CINEMATIC UNIVERSE", layout="wide")

tmdb = TMDb()
tmdb.api_key = 'a3ce43541791ff5e752a8e62ce0fcde2'
tmdb.language = 'en'

movie_api, discover_api, search_api = Movie(), Discover(), Search()

# --- 2. THE ROYAL GOLD UI (Classic 4-Column Grid) ---
def apply_royal_classic_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Poppins:wght@400&display=swap');

        /* Background: Deep Black Cinema */
        .stApp { background-color: #000000; font-family: 'Poppins', sans-serif; }

        /* ROYAL SHIMMER HEADING: Gold & Silver */
        @keyframes shimmer {
            0% { background-position: -200% center; }
            100% { background-position: 200% center; }
        }

        .royal-title {
            font-family: 'Playfair Display', serif;
            font-size: 60px !important;
            font-weight: 900 !important;
            text-align: center;
            background: linear-gradient(to right, #BF953F 20%, #FCF6BA 40%, #ffffff 50%, #FCF6BA 60%, #BF953F 80%);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shimmer 5s linear infinite;
            text-shadow: 2px 4px 10px rgba(0,0,0,0.5);
            margin-bottom: 30px;
        }

        /* MOVIE CARDS: Classic Gold Border */
        .movie-card {
            background-color: #111111;
            padding: 15px;
            border-radius: 12px;
            border: 1px solid #BF953F;
            text-align: center;
            margin-bottom: 25px;
            transition: 0.3s;
        }
        .movie-card:hover {
            transform: scale(1.03);
            border-color: #FCF6BA;
            box-shadow: 0 0 15px rgba(191, 149, 63, 0.4);
        }

        h3 { color: #FCF6BA !important; font-size: 18px; margin-top: 10px; }
        p { color: #ffffff !important; font-size: 14px; font-weight: bold; }
        
        [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #BF953F; }
        label { color: #FCF6BA !important; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

apply_royal_classic_styles()

# --- 3. EXPANDED ALGORITHM DATA ---
mood_map = {
    "Happy / Laughter": "35,16",
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

# --- 4. SESSION FLOW ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<h1 class="royal-title">IRFAN CINEMATIC UNIVERSE</h1>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        u_name = st.text_input("ENTER ACCESS NAME")
        if st.button("UNLOCK THE VAULT 💎") and u_name:
            st.session_state.logged_in = True
            st.rerun()
else:
    st.markdown('<h1 class="royal-title">IRFAN CINEMATIC UNIVERSE</h1>', unsafe_allow_html=True)
    
    # Sidebar Filters
    st.sidebar.markdown("<h2 style='color:#BF953F;'>Vault Filters</h2>", unsafe_allow_html=True)
    sel_mood = st.sidebar.selectbox("EMOTION", list(mood_map.keys()))
    sel_lang = st.sidebar.selectbox("LANGUAGE", list(lang_map.keys()))
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- 5. THE DATA ENGINE ---
    with st.spinner("Accessing Royal Records..."):
        movies = discover_api.discover_movies({
            'with_genres': mood_map[sel_mood],
            'with_original_language': lang_map[sel_lang],
            'sort_by': 'popularity.desc'
        })
        movies_list = list(movies) if movies else []

    # --- 6. DISPLAY GRID (4 COLUMNS) ---
    if movies_list:
        cols = st.columns(4)
        for i, m in enumerate(movies_list[:16]):
            with cols[i % 4]:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                # Handle poster images
                poster = f"https://image.tmdb.org/t/p/w500{m.poster_path}" if getattr(m, 'poster_path', None) else "https://via.placeholder.com/500x750?text=No+Poster"
                st.image(poster, use_container_width=True)
                st.markdown(f"<h3>{getattr(m, 'title', 'Unknown')}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p>⭐ {getattr(m, 'vote_average', 0.0)}</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("The vault is empty for this selection. Try another mood!")
