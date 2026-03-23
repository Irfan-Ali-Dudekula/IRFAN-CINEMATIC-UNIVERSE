import streamlit as st
from tmdbv3api import TMDb, Movie, Discover, Search
import requests

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="IRFAN CINEMATIC UNIVERSE", layout="wide")

tmdb = TMDb()
tmdb.api_key = 'a3ce43541791ff5e752a8e62ce0fcde2'
tmdb.language = 'en'

movie_api, discover_api, search_api = Movie(), Discover(), Search()

# --- 2. SESSION STATE (Stability Logic) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'u_name' not in st.session_state:
    st.session_state.u_name = "Guest"

# --- 3. THE ROYAL FINISH (Custom CSS) ---
def apply_royal_styles():
    bg_img = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070"
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Poppins:wght@300;400;600&display=swap');

        @keyframes shimmer {{
            0% {{ background-position: -200% center; }}
            100% {{ background-position: 200% center; }}
        }}

        .stApp {{ 
            background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url("{bg_img}"); 
            background-size: cover; background-attachment: fixed; 
            font-family: 'Poppins', sans-serif;
        }}

        .royal-title {{
            font-family: 'Playfair Display', serif;
            font-size: 65px !important;
            font-weight: 900 !important;
            text-align: center;
            background: linear-gradient(to right, #BF953F 20%, #FCF6BA 40%, #ffffff 50%, #FCF6BA 60%, #BF953F 80%);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shimmer 4s linear infinite;
            text-shadow: 3px 6px 15px rgba(0,0,0,0.5);
            margin-bottom: 20px;
            letter-spacing: 1px;
        }}

        .movie-card {{ 
            border: 1px solid rgba(255, 255, 255, 0.2); 
            padding: 25px; 
            border-radius: 20px; 
            background: rgba(0, 0, 0, 0.75); 
            backdrop-filter: blur(15px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.8);
            transition: 0.4s ease;
            text-align: center;
            margin-bottom: 20px;
        }}
        
        .movie-card:hover {{
            transform: translateY(-10px);
            border: 1px solid #FCF6BA;
            box-shadow: 0 0 25px rgba(252, 246, 186, 0.4);
        }}

        .rating-badge {{ 
            background: linear-gradient(45deg, #BF953F, #FCF6BA); 
            color: #111; padding: 5px 15px; border-radius: 10px; font-weight: 800;
        }}

        .play-button {{ 
            background: linear-gradient(90deg, #BF953F, #FCF6BA) !important; 
            color: #000 !important; padding: 12px; border-radius: 10px; text-align: center; 
            font-weight: 900; display: block; text-decoration: none; margin-top: 20px;
        }}
        
        [data-testid="stSidebar"] {{ background: rgba(10, 10, 10, 0.98) !important; border-right: 2px solid #BF953F; }}
        h3, p, span, label, .stMarkdown {{ color: #ffffff !important; }}
        </style>
        """, unsafe_allow_html=True)

# --- 4. SECURE DATA FETCHING ---
@st.cache_data(ttl=3600)
def get_movie_details(m_id):
    try:
        res = movie_api.details(m_id, append_to_response="credits,watch/providers,videos")
        providers = getattr(res, 'watch/providers', {}).get('results', {}).get('IN', {})
        ott_n, ott_l = None, None
        for mode in ['flatrate', 'free', 'ads']:
            if mode in providers:
                ott_n = providers[mode][0]['provider_name']
                ott_l = providers.get('link')
                break
        
        videos = getattr(res, 'videos', {}).get('results', [])
        trailer = next((f"https://www.youtube.com/watch?v={v['key']}" for v in videos if v['site'] == 'YouTube'), None)
        
        return {
            "plot": getattr(res, 'overview', "No plot available."),
            "cast": ", ".join([c['name'] for c in getattr(res, 'credits', {}).get('cast', [])[:4]]),
            "ott_n": ott_n, "ott_l": ott_l, "trailer": trailer, "rating": getattr(res, 'vote_average', 0.0)
        }
    except: return None

# --- 5. MAIN APP FLOW ---
apply_royal_styles()

if not st.session_state.logged_in:
    st.markdown('<h1 class="royal-title">IRFAN CINEMATIC UNIVERSE</h1>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        u_name = st.text_input("Enter Member Access Name")
        if st.button("Access the Vault 🔐") and u_name:
            st.session_state.logged_in, st.session_state.u_name = True, u_name
            st.rerun()
else:
    st.markdown('<h1 class="royal-title">IRFAN CINEMATIC UNIVERSE</h1>', unsafe_allow_html=True)
    
    # Sidebar Filters
    st.sidebar.markdown(f"### 👑 Member: {st.session_state.u_name}")
    mood_map = {"Happy": 35, "Sad": 18, "Adventures": 12, "Thrill": 53, "Romantic": 10749}
    lang_map = {"Telugu": "te", "Hindi": "hi", "Tamil": "ta", "English": "en", "Malayalam": "ml"}
    
    sel_mood = st.sidebar.selectbox("Choose Mood", ["Select"] + list(mood_map.keys()))
    sel_lang = st.sidebar.selectbox("Choose Language", ["Select"] + list(lang_map.keys()))
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    query = st.text_input("🔍 Search for a Cinematic Masterpiece...")

    # --- RECTIFIED LOGIC: ZERO-ERROR MOVIE FETCHING ---
    movies_list = []
    if query:
        movies_list = list(search_api.movies(query))
    elif sel_mood != "Select" and sel_lang != "Select":
        raw_discovery = discover_api.discover_movies({
            'with_genres': mood_map[sel_mood],
            'with_original_language': lang_map[sel_lang],
            'sort_by': 'popularity.desc'
        })
        movies_list = list(raw_discovery) if raw_discovery else []
    else:
        movies_list = list(movie_api.popular())

    # --- DISPLAY GRID ---
    if movies_list:
        cols = st.columns(3)
        # Safe iteration using min() to prevent slicing errors
        limit = min(len(movies_list), 15)
        for i in range(limit):
            movie = movies_list[i]
            details = get_movie_details(movie.id)
            if not details or not movie.poster_path: continue
            
            with cols[i % 3]:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                st.image(f"https://image.tmdb.org/t/p/w500{movie.poster_path}", use_container_width=True)
                st.markdown(f"<h3>{movie.title}</h3>", unsafe_allow_html=True)
                st.markdown(f"<span class='rating-badge'>IMDb ⭐ {details['rating']:.1f}</span>", unsafe_allow_html=True)
                
                if details['ott_n']:
                    st.caption(f"Streaming on: {details['ott_n']}")
                
                with st.expander("Bio & Cast"):
                    st.write(details['plot'])
                    st.caption(f"Stars: {details['cast']}")
                
                if details['trailer']: st.video(details['trailer'])
                if details['ott_l']: st.markdown(f'<a href="{details["ott_l"]}" target="_blank" class="play-button">WATCH NOW</a>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("The Vault is searching... Please select a Mood and Language or Search.")
