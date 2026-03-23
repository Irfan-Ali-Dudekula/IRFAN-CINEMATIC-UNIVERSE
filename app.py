import streamlit as st
from tmdbv3api import TMDb, Movie, Discover, Search

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="IRFAN CINEMATIC UNIVERSE", layout="wide")

tmdb = TMDb()
tmdb.api_key = 'a3ce43541791ff5e752a8e62ce0fcde2'
tmdb.language = 'en'

movie_api, discover_api, search_api = Movie(), Discover(), Search()

# --- 2. DATA FETCHING (Ensuring Plots are Not Empty) ---
@st.cache_data(ttl=3600)
def get_movie_data(m_id):
    try:
        res = movie_api.details(m_id)
        return {
            "plot": getattr(res, 'overview', "Plot information is currently restricted to the vault."),
            "rating": getattr(res, 'vote_average', 0.0)
        }
    except:
        return {"plot": "Plot summary unavailable.", "rating": 0.0}

# --- 3. ROYAL UI & BACKGROUND ---
def apply_styles():
    # High-quality theater background
    bg_img = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070"
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Poppins:wght@300;400;600&display=swap');

        .stApp {{ 
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{bg_img}"); 
            background-size: cover; background-attachment: fixed; 
            font-family: 'Poppins', sans-serif;
        }}

        @keyframes shimmer {{
            0% {{ background-position: -200% center; }}
            100% {{ background-position: 200% center; }}
        }}

        .royal-title {{
            font-family: 'Playfair Display', serif;
            font-size: 60px !important;
            text-align: center;
            background: linear-gradient(to right, #BF953F 20%, #FCF6BA 40%, #ffffff 50%, #FCF6BA 60%, #BF953F 80%);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shimmer 5s linear infinite;
            text-shadow: 2px 4px 10px rgba(0,0,0,0.5);
            margin-bottom: 20px;
        }}

        .movie-card {{
            background-color: rgba(0, 0, 0, 0.85);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #BF953F;
            text-align: center;
            margin-bottom: 25px;
            min-height: 750px;
        }}

        h3 {{ color: #FCF6BA !important; font-size: 20px; margin-bottom: 10px; }}
        .plot-text {{ color: #ffffff !important; font-size: 14px; text-align: justify; padding: 10px; }}
        .rating-badge {{ background: #BF953F; color: black; padding: 5px 10px; border-radius: 5px; font-weight: bold; }}
        
        [data-testid="stSidebar"] {{ background-color: #000000 !important; border-right: 1px solid #BF953F; }}
        </style>
    """, unsafe_allow_html=True)

apply_styles()

# --- 4. SESSION FLOW ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<h1 class="royal-title">IRFAN CINEMATIC UNIVERSE</h1>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        u_name = st.text_input("ENTER ACCESS NAME")
        if st.button("UNLOCK THE VAULT 💎") and u_name:
            st.session_state.logged_in = True
            st.rerun()
else:
    st.markdown('<h1 class="royal-title">IRFAN CINEMATIC UNIVERSE</h1>', unsafe_allow_html=True)
    
    # Algorithm Logic
    mood_map = {
        "Happy / Laughter": "35", "Sad / Emotional": "18", "Thrill / Fear": "53,27",
        "Mystery": "9648", "Action / Bravery": "28", "Romantic": "10749",
        "Sci-Fi": "878", "War": "10752", "Family": "10751", "Crime": "80"
    }
    lang_map = {
        "Telugu": "te", "Hindi": "hi", "Tamil": "ta", "English": "en",
        "Malayalam": "ml", "Kannada": "kn"
    }

    st.sidebar.markdown("<h2 style='color:#BF953F;'>Vault Controls</h2>", unsafe_allow_html=True)
    sel_mood = st.sidebar.selectbox("EMOTION", list(mood_map.keys()))
    sel_lang = st.sidebar.selectbox("LANGUAGE", list(lang_map.keys()))
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- 5. THE DATA ENGINE ---
    with st.spinner("Fetching Royal Data..."):
        movies = discover_api.discover_movies({
            'with_genres': mood_map[sel_mood],
            'with_original_language': lang_map[sel_lang],
            'sort_by': 'popularity.desc'
        })
        movies_list = list(movies) if movies else []

    # --- 6. DISPLAY GRID (3 COLUMNS FOR READABILITY) ---
    if movies_list:
        cols = st.columns(3)
        for i, m in enumerate(movies_list[:12]):
            m_data = get_movie_data(m.id)
            with cols[i % 3]:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                poster = f"https://image.tmdb.org/t/p/w500{m.poster_path}" if m.poster_path else "https://via.placeholder.com/500x750"
                st.image(poster, use_container_width=True)
                st.markdown(f"<h3>{m.title}</h3>", unsafe_allow_html=True)
                st.markdown(f"<span class='rating-badge'>⭐ {m_data['rating']}</span>", unsafe_allow_html=True)
                st.markdown(f'<p class="plot-text"><b>STORY:</b> {m_data["plot"]}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("The vault is searching for your selection...")
