import streamlit as st
from tmdbv3api import TMDb, Movie
import requests

# 1. Configuration & Security
tmdb = TMDb()
try:
    tmdb.api_key = st.secrets["TMDB_API_KEY"]
except KeyError:
    st.error("Missing TMDB_API_KEY in Streamlit Secrets!")
    st.stop()

tmdb.language = 'en'

# 2. Page Setup & Styling
st.set_page_config(page_title="ICU - Irfan Cinematic Universe", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #f39c12; color: white; border-radius: 8px; font-weight: bold; }
    h1 { color: #f39c12; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 IRFAN-CINEMATIC-UNIVERSE (ICU)")

# 3. Optimized Data Fetching
@st.cache_data(ttl=3600)
def get_movies(genre_id, lang_code):
    movie = Movie()
    return movie.discover({
        'with_genres': genre_id,
        'with_original_language': lang_code,
        'sort_by': 'popularity.desc'
    })

# 4. User Inputs
col1, col2 = st.columns(2)
with col1:
    mood = st.selectbox("Current Mood", ["Happy", "Thrilled", "Sad", "Action", "Romantic"])
with col2:
    lang = st.selectbox("Language", ["English", "Telugu", "Hindi", "Tamil", "Kannada", "Malayalam"])

mood_map = {"Happy": 35, "Thrilled": 53, "Sad": 18, "Action": 28, "Romantic": 10749}
lang_map = {"English": "en", "Telugu": "te", "Hindi": "hi", "Tamil": "ta", "Kannada": "kn", "Malayalam": "ml"}

# 5. Execution & Display
if st.button("Generate Recommendations"):
    results = get_movies(mood_map[mood], lang_map[lang])
    
    if results:
        # Create a grid layout
        rows = [results[i:i + 4] for i in range(0, 12, 4)]
        for row in rows:
            cols = st.columns(4)
            for i, movie in enumerate(row):
                with cols[i]:
                    # --- UPDATED POSTER LOGIC ---
                    poster_url = f"https://image.tmdb.org/t/p/w500{movie.poster_path}" if movie.poster_path else "https://via.placeholder.com/500x750?text=No+Poster+Available"
                    
                    st.image(poster_url, use_column_width=True)
                    st.markdown(f"**{movie.title}**")
                    st.caption(f"⭐ {movie.vote_average} | {movie.release_date[:4] if movie.release_date else 'N/A'}")
    else:
        st.error("No matches found for this combination.")

st.divider()
st.caption("Developed by Irfan Ali Dudekula | Data via TMDB")
