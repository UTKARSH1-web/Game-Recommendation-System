import streamlit as st
import pandas as pd
from src.recommender import GameRecommender

# Initialize Recommender
@st.cache_resource
def load_recommender():
    return GameRecommender()

recommender = load_recommender()

# ---- Page Configuration ----
st.set_page_config(page_title="Game Recommender", page_icon="🎮", layout="wide")

# ---- Custom CSS for Cool UI ----
# st.markdown("""
#     <style>
#     /* Pure CSS Live Animated Gaming Grid */
#     .stApp {
#         background-color: #0b0c10 !important;
#         background-image: 
#           linear-gradient(rgba(255, 75, 75, 0.15) 1px, transparent 1px),
#           linear-gradient(90deg, rgba(255, 75, 75, 0.15) 1px, transparent 1px) !important;
#         background-size: 40px 40px !important;
#         animation: panBg 10s linear infinite !important;
#     }
    
#     @keyframes panBg {
#         0% { background-position: 0px 0px; }
#         100% { background-position: 40px 40px; }
#     }

#     [data-testid="stHeader"] {
#         background: transparent !important;
#     }
#     /* Semi-transparent sidebar */
#     [data-testid="stSidebar"] {
#         background-color: rgba(15, 12, 41, 0.85);
#         backdrop-filter: blur(10px);
#     }
    
#     /* Glassmorphism for Game Cards */
#     .game-card {
#         background-color: rgba(30, 30, 46, 0.75);
#         backdrop-filter: blur(12px);
#         padding: 20px;
#         border-radius: 10px;
#         border-left: 5px solid #ff4b4b;
#         margin-bottom: 15px;
#         box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#     }
#     .game-title {
#         color: #ffffff;
#         font-size: 22px;
#         font-weight: bold;
#         margin-bottom: 5px;
#         text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
#     }
#     .game-genre {
#         color: #ff4b4b;
#         font-size: 14px;
#         font-weight: bold;
#     }
#     .game-rating {
#         color: #f1fa8c;
#         font-size: 16px;
#     }
#     .sim-score {
#         color: #50fa7b;
#         font-size: 14px;
#         float: right;
#         font-weight: bold;
#     }
    
#     /* Make standard text pop more against the background */
#     h1, h2, h3, p, span {
#         text-shadow: 1px 1px 5px rgba(0,0,0,0.9);
#     }
#     </style>
# """, unsafe_allow_html=True)

st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(to top, #090909, #1a0033);
    overflow: hidden;
}

/* SUNSET GLOW */
.stApp::before {
    content: "";
    position: fixed;
    top: 30%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, #ff0077 0%, #ff00cc 40%, transparent 70%);
    filter: blur(80px);
    animation: pulseSun 6s ease-in-out infinite;
    z-index: 0;
}

@keyframes pulseSun {
    0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.7; }
    50% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
}

/* RETRO GRID FLOOR */
.stApp::after {
    content: "";
    position: fixed;
    bottom: 0;
    width: 100%;
    height: 60%;
    background-image: 
        linear-gradient(rgba(0,255,255,0.3) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,255,0.3) 1px, transparent 1px);
    background-size: 50px 50px;
    transform: perspective(500px) rotateX(60deg);
    transform-origin: bottom;
    animation: moveGrid 5s linear infinite;
    z-index: 0;
}

@keyframes moveGrid {
    0% { background-position: 0 0; }
    100% { background-position: 0 50px; }
}

/* CONTENT ABOVE */
.main, .block-container {
    position: relative;
    z-index: 1;
}

/* SIDEBAR GLASS */
[data-testid="stSidebar"] {
    background: rgba(10, 10, 30, 0.85);
    backdrop-filter: blur(10px);
}

/* GAME CARDS */
.game-card {
    background: rgba(20, 20, 40, 0.6);
    backdrop-filter: blur(12px);
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(255,0,150,0.3);
    box-shadow: 0 0 20px rgba(255,0,150,0.4);
    transition: 0.3s;
}

.game-card:hover {
    transform: scale(1.05);
    box-shadow: 0 0 35px rgba(0,255,255,0.8);
}

.game-title {
    color: #fff;
    text-shadow: 0 0 10px #ff00cc;
}

</style>
""", unsafe_allow_html=True)

# ---- Main Layout ----
st.title("🎮 Next-Gen Game Recommender")
st.markdown("Discover your next favorite game based on content similarity and popularity!")

# Sidebar for Trending Games
with st.sidebar:
    st.header("🔥 Trending Games")
    st.write("Top rated & most popular games right now.")
    trending = recommender.get_trending_games(top_n=5)
    for game in trending:
        st.markdown(f"**{game['game_name']}** ⭐ {game['rating']}")
        st.caption(f"Genre: {game['genre']}")
        st.divider()

# Main Application Area
st.subheader("🎯 Find Similar Games")

# Select Box
games_list = recommender.get_all_game_names()
selected_game = st.selectbox("Search for a game you love:", games_list)

# Recommend Button
if st.button("Recommend 🚀", use_container_width=True):
    with st.spinner("Crunching the data..."):
        results = recommender.recommend(selected_game)
        
    if results:
        st.success(f"Because you liked **{selected_game}**, you might also enjoy:")
        
        # Display recommendations in a grid/columns
        cols = st.columns(len(results))
        for idx, result in enumerate(results):
            with cols[idx]:
                st.markdown(f"""
                <div class="game-card">
                    <div class="sim-score">{result['similarity_score']}% Match</div>
                    <div class="game-title">{result['game_name']}</div>
                    <div class="game-genre">{result['genre']}</div>
                    <div class="game-rating">⭐ {result['rating']} / 10</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No recommendations found. Try another game!")
