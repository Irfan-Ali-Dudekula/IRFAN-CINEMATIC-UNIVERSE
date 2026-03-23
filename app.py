import streamlit as st
from tmdbv3api import TMDb, Movie, Discover

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Irfan Cinematic Universe",
    page_icon="🎬",
    layout="wide"
)

# --- 2. ADMIN PROTECTION & HIDE UI ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
    """, unsafe_allow_html=True)

tmdb = TMDb()
tmdb.api_key = 'a3ce43541791ff5e752a8e62ce0fcde2'
tmdb.language = 'en'
movie_api, discover_api = Movie(), Discover()

# --- 3. ROYAL STYLES & BACKGROUND ---
def apply_styles():
    bg_img = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070"
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Poppins:wght@400;600&display=swap');
        .stApp {{ 
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{bg_img}"); 
            background-size: cover; background-attachment: fixed; 
        }}
        @keyframes shimmer {{ 0% {{ background-position: -200% center; }} 100% {{ background-position: 200% center; }} }}
        .royal-title {{
            font-family: 'Playfair Display', serif; font-size: 60px !important; text-align: center;
            background: linear-gradient(to right, #BF953F, #FCF6BA, #ffffff, #FCF6BA, #BF953F);
            background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            animation: shimmer 5s linear infinite; margin-bottom: 25px;
        }}
        .movie-card {{ background: rgba(0, 0, 0, 0.85); padding: 20px; border-radius: 15px; border: 1px solid #BF953F; text-align: center; margin-bottom: 25px; min-height: 720px; }}
        h3 {{ color: #FCF6BA !important; }}
        .plot-text {{ color: #ffffff !important; text-align: justify; font-size: 14px; padding: 10px; border-top: 1px solid #333; }}
        [data-testid="stSidebar"] {{ background-color: #000000 !important; border-right: 1px solid #BF953F; }}
        </style>
    """, unsafe_allow_html=True)

apply_styles()

# --- 4. DYNAMIC MUSIC PLAYER ---
def play_audio(url):
    audio_html = f"""
        <iframe src="{url}" allow="autoplay" style="display:none"></iframe>
        <audio autoplay loop><source src="{url}" type="audio/mp3"></audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# --- 5. ADMIN BOOTH (YOUR MUSICAL CHOICE) ---
ADMIN_KEY = "irfan_admin_2026"
# Added Rasputin and Bella Ciao Instrumentals
music_options = {
    "Rasputin (Instrumental)": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3", 
    "Bella Ciao (Instrumental)": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "Cinematic Orchestral": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3",
    "Silent Mode": ""
}

# Initial default
if 'bg_music' not in st.session_state:
    st.session_state.bg_music = music_options["Cinematic Orchestral"]

with st.sidebar:
    st.title("Director's Booth")
    admin_input = st.text_input("Admin Key", type="password")
    if admin_input == ADMIN_KEY:
        st.success("Admin Mode Active")
        choice = st.selectbox("Select Background Vibe", list(music_options.keys()))
        st.session_state.bg_music = music_options[choice]
        if st.button("Refresh Vault"):
            st.cache_data.clear()
            st.rerun()

# --- 6. MAIN APP FLOW ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<h1 class="royal-title">IRFAN CINEMATIC UNIVERSE</h1>', unsafe_allow_html=True)
    u_name = st.text_input("Enter Member Name")
    if st.button("UNLOCK THE VAULT 💎") and u_name:
        st.session_state.logged_in = True
        st.rerun()
else:
    # Play the selected music
    if st.session_state.bg_music:
        play_audio(st.session_state.bg_music)
    
    st.markdown('<h1 class="royal-title">IRFAN CINEMATIC UNIVERSE</h1>', unsafe_allow_html=True)
    
    mood_map = {"Happy": "35", "Sad": "18", "Thrill": "53", "Action": "28", "Romantic": "10749", "Sci-Fi": "878"}
    lang_map = {"Telugu": "te", "Hindi": "hi", "Tamil": "ta", "English": "en", "Malayalam": "ml", "Kannada": "kn"}

    c1, c2 = st.columns(2)
    with c1: sel_mood = st.selectbox("Current Mood", list(mood_map.keys()))
    with c2: sel_lang = st.selectbox("Preferred Language", list(lang_map.keys()))

    with st.spinner("Fetching from the Irfan Vault..."):
        movies = discover_api.discover_movies({
            'with_genres': mood_map[sel_mood],
            'with_original_language': lang_map[sel_lang],
            'sort_by': 'popularity.desc'
        })

    if movies:
        grid = st.columns(3)
        for i, m in enumerate(list(movies)[:12]):
            with grid[i % 3]:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                img = f"https://image.tmdb.org/t/p/w500{m.poster_path}" if m.poster_path else "https://via.placeholder.com/500x750"
                st.image(img, use_container_width=True)
                st.markdown(f"<h3>{m.title}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:#BF953F;'><b>⭐ Rating: {m.vote_average}</b></p>", unsafe_allow_html=True)
                st.markdown(f'<div class="plot-text"><b>STORY:</b> {m.overview if m.overview else "Confidential..."}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
