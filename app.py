st.set_page_config(
    page_title="Irfan Cinematic Universe",
    page_icon="🎬",
    layout="wide"
)
import streamlit as st
from tmdbv3api import TMDb, Movie, Discover

# --- 1. CONFIG ---
st.set_page_config(page_title="IRFAN CINEMATIC UNIVERSE", layout="wide")

tmdb = TMDb()
tmdb.api_key = 'a3ce43541791ff5e752a8e62ce0fcde2'
tmdb.language = 'en'

movie_api, discover_api = Movie(), Discover()

# --- 2. THE MOVIE ENGINE (Plots + OTT Platform) ---
@st.cache_data(ttl=3600)
def get_premium_details(m_id):
    try:
        # Fetching details and watch providers in ONE call for speed
        res = movie_api.details(m_id, append_to_response="watch/providers")
        
        # Get OTT providers for India (IN)
        providers = getattr(res, 'watch/providers', {}).get('results', {}).get('IN', {})
        ott_name = "Theater / Rental"
        if 'flatrate' in providers:
            ott_name = providers['flatrate'][0]['provider_name']
        elif 'free' in providers:
            ott_name = providers['free'][0]['provider_name']
            
        return {
            "plot": getattr(res, 'overview', "Plot secret remains in the vault."),
            "ott": ott_name,
            "rating": getattr(res, 'vote_average', 0.0)
        }
    except:
        return {"plot": "Summary currently unavailable.", "ott": "Check TMDB", "rating": 0.0}

# --- 3. ROYAL STYLES ---
def apply_styles():
    bg_img = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070"
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Poppins:wght@400;600&display=swap');
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)), url("{bg_img}"); background-size: cover; background-attachment: fixed; }}
        
        @keyframes shimmer {{ 0% {{ background-position: -200% center; }} 100% {{ background-position: 200% center; }} }}
        .royal-title {{ font-family: 'Playfair Display', serif; font-size: 60px !important; text-align: center; background: linear-gradient(to right, #BF953F, #FCF6BA, #ffffff, #FCF6BA, #BF953F); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: shimmer 5s linear infinite; margin-bottom: 25px; }}
        
        .movie-card {{ background: rgba(0, 0, 0, 0.85); padding: 20px; border-radius: 15px; border: 1px solid #BF953F; text-align: center; margin-bottom: 25px; }}
        h3 {{ color: #FCF6BA !important; margin-bottom: 10px; font-size: 22px; }}
        .ott-badge {{ background: #BF953F; color: black; padding: 4px 10px; border-radius: 5px; font-weight: 800; font-size: 13px; display: inline-block; margin-bottom: 10px; }}
        .plot-box {{ color: #ffffff !important; font-size: 14px; text-align: justify; height: 120px; overflow-y: auto; padding: 5px; border-top: 1px solid #333; }}
        [data-testid="stSidebar"] {{ background-color: #000000 !important; border-right: 1px solid #BF953F; }}
        </style>
    """, unsafe_allow_html=True)

apply_styles()

# --- 4. APP FLOW ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<h1 class="royal-title">IRFAN CINEMATIC UNIVERSE</h1>', unsafe_allow_html=True)
    u_name = st.text_input("ACCESS NAME")
    if st.button("UNLOCK THE VAULT 💎") and u_name:
        st.session_state.logged_in = True
        st.rerun()
else:
    st.markdown('<h1 class="royal-title">IRFAN CINEMATIC UNIVERSE</h1>', unsafe_allow_html=True)
    
    mood_map = {"Happy / Laughter": "35", "Sad / Emotional": "18", "Thrill": "53,27", "Action": "28", "Romantic": "10749"}
    lang_map = {"Telugu": "te", "Hindi": "hi", "Tamil": "ta", "English": "en", "Malayalam": "ml", "Kannada": "kn"}

    st.sidebar.markdown("<h2 style='color:#BF953F;'>Settings</h2>", unsafe_allow_html=True)
    sel_mood = st.sidebar.selectbox("EMOTION", list(mood_map.keys()))
    sel_lang = st.sidebar.selectbox("LANGUAGE", list(lang_map.keys()))
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- 5. THE DATA ENGINE ---
    with st.spinner("Fetching Royal Records..."):
        raw_movies = discover_api.discover_movies({
            'with_genres': mood_map[sel_mood],
            'with_original_language': lang_map[sel_lang],
            'sort_by': 'popularity.desc'
        })
        movies_list = list(raw_movies) if raw_movies else []

    # --- 6. DISPLAY GRID (3 Columns for no-overlap) ---
    if movies_list:
        cols = st.columns(3)
        for i, m in enumerate(movies_list[:12]):
            details = get_premium_details(m.id) # Fast fetch
            with cols[i % 3]:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                img = f"https://image.tmdb.org/t/p/w500{m.poster_path}" if m.poster_path else "https://via.placeholder.com/500x750"
                st.image(img, use_container_width=True)
                st.markdown(f"<h3>{m.title}</h3>", unsafe_allow_html=True)
                st.markdown(f"<div class='ott-badge'>📺 {details['ott']}</div>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:#BF953F; font-weight:bold;'>⭐ {details['rating']}</p>", unsafe_allow_html=True)
                st.markdown(f'<div class="plot-box"><b>STORY:</b> {details["plot"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Vault search active... Choose a different combination.")
