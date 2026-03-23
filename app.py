import streamlit as st
from tmdbv3api import TMDb, Movie, Discover

# --- 1. CONFIG ---
st.set_page_config(
    page_title="Irfan Cinematic Universe",
    page_icon="🎬",
    layout="wide"
)

# --- 2. ADMIN PROTECTION ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

tmdb = TMDb()
tmdb.api_key = 'a3ce43541791ff5e752a8e62ce0fcde2'
tmdb.language = 'en'
movie_api, discover_api = Movie(), Discover()

# --- 3. SAFE DATA FETCH (Prevents Black Boxes) ---
@st.cache_data(ttl=3600)
def get_safe_details(m_id):
    try:
        # We only fetch watch providers to avoid overloading
        res = movie_api.details(m_id, append_to_response="watch/providers")
        providers = getattr(res, 'watch/providers', {}).get('results', {}).get('IN', {})
        
        ott = "Theater / Rental"
        if 'flatrate' in providers:
            ott = providers['flatrate'][0]['provider_name']
        elif 'free' in providers:
            ott = providers['free'][0]['provider_name']
            
        return {"ott": ott, "rating": getattr(res, 'vote_average', 0.0)}
    except:
        return {"ott": "Check TMDB", "rating": 0.0}

# --- 4. ROYAL STYLES ---
def apply_styles():
    bg_img = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070"
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Poppins:wght@400;600&display=swap');
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), url("{bg_img}"); background-size: cover; background-attachment: fixed; }}
        
        @keyframes shimmer {{ 0% {{ background-position: -200% center; }} 100% {{ background-position: 200% center; }} }}
        .royal-title {{ font-family: 'Playfair Display', serif; font-size: 60px !important; text-align: center; background: linear-gradient(to right, #BF953F, #FCF6BA, #ffffff, #FCF6BA, #BF953F); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: shimmer 5s linear infinite; margin-bottom: 25px; }}
        
        .movie-card {{ background: rgba(0, 0, 0, 0.85); padding: 20px; border-radius: 15px; border: 1px solid #BF953F; text-align: center; margin-bottom: 25px; min-height: 700px; display: flex; flex-direction: column; justify-content: space-between; }}
        h3 {{ color: #FCF6BA !important; font-size: 22px; }}
        .ott-badge {{ background: #BF953F; color: black; padding: 5px 12px; border-radius: 8px; font-weight: 800; font-size: 14px; margin: 10px 0; }}
        .plot-box {{ color: #ffffff !important; font-size: 14px; text-align: justify; height: 120px; overflow-y: auto; padding: 10px; border-top: 1px solid #333; }}
        [data-testid="stSidebar"] {{ background-color: #000000 !important; border-right: 1px solid #BF953F; }}
        </style>
    """, unsafe_allow_html=True)

apply_styles()

# --- 5. ADMIN BOOTH ---
ADMIN_KEY = "irfan_admin_2026"
with st.sidebar:
    st.markdown("<h2 style='color:#BF953F;'>Director's Booth</h2>", unsafe_allow_html=True)
    admin_input = st.text_input("Admin Key", type="password")
    if admin_input == ADMIN_KEY:
        st.success("Admin Access Granted")
        if st.button("Clear Cache & Fix Display"):
            st.cache_data.clear()
            st.rerun()

# --- 6. APP FLOW ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

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
    
    mood_map = {"Happy / Comedy": "35", "Sad / Emotional": "18", "Thrill / Action": "53,28", "Romantic": "10749"}
    lang_map = {"Telugu": "te", "Hindi": "hi", "Tamil": "ta", "English": "en", "Malayalam": "ml", "Kannada": "kn"}

    c1, c2 = st.columns(2)
    with c1: sel_mood = st.selectbox("CHOOSE EMOTION", list(mood_map.keys()))
    with c2: sel_lang = st.selectbox("CHOOSE LANGUAGE", list(lang_map.keys()))

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- 7. DATA ENGINE ---
    with st.spinner("Accessing Royal Records..."):
        raw_movies = discover_api.discover_movies({
            'with_genres': mood_map[sel_mood],
            'with_original_language': lang_map[sel_lang],
            'sort_by': 'popularity.desc'
        })
        movies_list = list(raw_movies) if raw_movies else []

    # --- 8. STABLE DISPLAY GRID ---
    if movies_list:
        cols = st.columns(3)
        for i, m in enumerate(movies_list[:12]):
            # Get OTT and Details safely
            details = get_safe_details(m.id)
            
            with cols[i % 3]:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                
                # Image
                poster = f"https://image.tmdb.org/t/p/w500{m.poster_path}" if m.poster_path else "https://via.placeholder.com/500x750"
                st.image(poster, use_container_width=True)
                
                # Content
                st.markdown(f"<h3>{m.title}</h3>", unsafe_allow_html=True)
                st.markdown(f"<div class='ott-badge'>📺 {details['ott']}</div>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:#BF953F; font-weight:bold;'>⭐ Rating: {details['rating']}</p>", unsafe_allow_html=True)
                
                # Plot (Using data already in search to avoid extra call)
                plot_summary = m.overview if m.overview else "Story secret is kept in the vault."
                st.markdown(f'<div class="plot-box"><b>STORY:</b> {plot_summary}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Searching the vault... Try a different combination.")
