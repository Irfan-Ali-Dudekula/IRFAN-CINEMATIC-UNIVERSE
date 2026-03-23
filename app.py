import streamlit as st
from tmdbv3api import TMDb, Movie, Discover

# --- 1. CONFIG ---
st.set_page_config(
    page_title="Irfan Cinematic Universe",
    page_icon="🎬",
    layout="wide"
)

# --- 2. SECURITY & SECRETS ---
# SMART UPDATE: Using st.secrets for the API Key to keep your GitHub safe.
tmdb = TMDb()
try:
    tmdb.api_key = st.secrets["TMDB_API_KEY"]
except:
    # Fallback for local testing if secrets aren't set
    tmdb.api_key = 'a3ce43541791ff5e752a8e62ce0fcde2' 

tmdb.language = 'en'
movie_api, discover_api = Movie(), Discover()

# --- 3. UI PROTECTION (Admin View) ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 4. ROYAL STYLES ---
def apply_styles():
    bg_img = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070"
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Poppins:wght@400;600&display=swap');
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), url("{bg_img}"); background-size: cover; background-attachment: fixed; }}
        
        @keyframes shimmer {{ 0% {{ background-position: -200% center; }} 100% {{ background-position: 200% center; }} }}
        .royal-title {{ font-family: 'Playfair Display', serif; font-size: 55px !important; text-align: center; background: linear-gradient(to right, #BF953F, #FCF6BA, #ffffff, #FCF6BA, #BF953F); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: shimmer 5s linear infinite; margin-bottom: 25px; text-transform: uppercase; }}
        
        .movie-card {{ background: rgba(0, 0, 0, 0.85); padding: 20px; border-radius: 15px; border: 1.5px solid #BF953F; text-align: center; margin-bottom: 25px; min-height: 720px; transition: transform 0.3s; }}
        .movie-card:hover {{ transform: scale(1.02); border-color: #FCF6BA; }}
        h3 {{ color: #FCF6BA !important; margin-bottom: 10px; font-size: 20px; height: 50px; overflow: hidden; }}
        .rating-badge {{ color: #BF953F !important; font-weight: bold; font-size: 18px; }}
        .plot-box {{ color: #dddddd !important; font-size: 13.5px; text-align: justify; height: 120px; overflow-y: auto; padding: 10px; border-top: 1px solid #BF953F33; margin-top: 10px; }}
        [data-testid="stSidebar"] {{ background-color: #000000 !important; border-right: 1px solid #BF953F; }}
        label {{ color: #BF953F !important; font-weight: bold; }}
        </style>
    """, unsafe_allow_html=True)

apply_styles()

# --- 5. DIRECTOR'S BOOTH (Admin) ---
ADMIN_KEY = "irfan_admin_2026"
with st.sidebar:
    st.markdown("<h2 style='color:#BF953F; text-align:center;'>DIRECTOR'S BOOTH</h2>", unsafe_allow_html=True)
    admin_input = st.text_input("Vault Key", type="password")
    if admin_input == ADMIN_KEY:
        st.success("Access Granted")
        if st.button("Clear Global Cache"):
            st.cache_data.clear()
            st.rerun()

# --- 6. APP SESSION LOGIC ---
if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<h1 class="royal-title">IRFAN CINEMATIC UNIVERSE</h1>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<p style='text-align:center; color:#FCF6BA;'>Welcome to the ICU Vault. Enter your access name to proceed.</p>", unsafe_allow_html=True)
        u_name = st.text_input("ACCESS NAME", placeholder="Enter your name...")
        if st.button("UNLOCK THE VAULT 💎") and u_name:
            st.session_state.logged_in = True
            st.rerun()
else:
    st.markdown('<h1 class="royal-title">IRFAN CINEMATIC UNIVERSE</h1>', unsafe_allow_html=True)
    
    # --- MOOD & LANG CONFIG ---
    mood_map = {"Happy / Laughter": "35", "Sad / Emotional": "18", "Thrill": "53,27", "Action": "28", "Romantic": "10749"}
    lang_map = {"Telugu": "te", "Hindi": "hi", "Tamil": "ta", "English": "en", "Malayalam": "ml", "Kannada": "kn"}

    c1, c2 = st.columns(2)
    with c1: sel_mood = st.selectbox("SELECT EMOTION", list(mood_map.keys()))
    with c2: sel_lang = st.selectbox("SELECT LANGUAGE", list(lang_map.keys()))

    if st.sidebar.button("Exit Vault"):
        st.session_state.logged_in = False
        st.rerun()

    # --- 7. DATA ENGINE (With Smart Caching) ---
    @st.cache_data(ttl=3600)
    def fetch_royal_records(mood_id, lang_id):
        return discover_api.discover_movies({
            'with_genres': mood_id,
            'with_original_language': lang_id,
            'sort_by': 'popularity.desc'
        })

    with st.spinner("Accessing Royal Records..."):
        raw_movies = fetch_royal_records(mood_map[sel_mood], lang_map[sel_lang])
        movies_list = list(raw_movies) if raw_movies else []

    # --- 8. DISPLAY GRID ---
    if movies_list:
        cols = st.columns(3)
        for i, m in enumerate(movies_list[:12]):
            with cols[i % 3]:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                
                # Poster Safety (Using your requested logic)
                img_path = getattr(m, 'poster_path', None)
                img = f"https://image.tmdb.org/t/p/w500{img_path}" if img_path else "https://via.placeholder.com/500x750?text=No+Poster+Available"
                
                st.image(img, use_container_width=True)
                
                # Title & Rating
                st.markdown(f"<h3>{getattr(m, 'title', 'Untitled')}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p class='rating-badge'>⭐ {getattr(m, 'vote_average', 'N/A')} | {getattr(m, 'release_date', 'N/A')[:4]}</p>", unsafe_allow_html=True)
                
                # Plot
                plot_text = getattr(m, 'overview', "Story details are currently classified in the ICU Vault.")
                st.markdown(f'<div class="plot-box"><b>STORY:</b><br>{plot_text}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("The Vault is currently empty for this combination. Try another emotion.")

    st.markdown("<p style='text-align:center; color:#BF953F; margin-top:50px;'>© 2026 IRFAN CINEMATIC UNIVERSE | Powered by TMDB API</p>", unsafe_allow_html=True)
