import streamlit as st
import random

# Initialize session state to track game data and AI tendencies
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.user_tendencies = {"Run": 0, "Pass": 0, "Deep Bomb": 0}
    st.session_state.user_team = ""
    st.session_state.score = {"User": 0, "CPU": 0}

st.title("🏈 NFL Coach Simulator: 2026 Season")

# 1. Team Selection (Replaces input())
teams = [
    "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills",
    "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns",
    "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers",
    "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Kansas City Chiefs",
    "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins",
    "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants",
    "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers",
    "Seattle Seahawks", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Commanders"
]

if not st.session_state.game_started:
    st.session_state.user_team = st.selectbox("Select your franchise:", teams)
    if st.button("Start Game"):
        st.session_state.game_started = True
        st.rerun()

# 2. Game Interface
if st.session_state.game_started:
    st.subheader(f"{st.session_state.user_team} vs. CPU Opponent")
    st.write(f"**Current Score:** {st.session_state.user_team}: {st.session_state.score['User']} | CPU: {st.session_state.score['CPU']}")

    st.write("### Offensive Playcall")
    col1, col2, col3 = st.columns(3)

    # 3. AI Adaptivity Logic (The 'Chess Match')
    # This replaces the hidden input logic with interactive buttons
    with col1:
        if st.button("Rush Up Middle"):
            st.session_state.user_tendencies["Run"] += 1
            st.success("You gained 4 yards on a tough run.")
            
    with col2:
        if st.button("Short Pass"):
            st.session_state.user_tendencies["Pass"] += 1
            st.info("Complete for a 12-yard gain!")

    with col3:
        if st.button("Deep Bomb"):
            st.session_state.user_tendencies["Deep Bomb"] += 1
            # AI Check: If user spams Deep Bomb, CPU counters
            if st.session_state.user_tendencies["Deep Bomb"] > 2:
                st.error("SACKED! The Digital Scout AI predicted your deep pass.")
            else:
                st.warning("TOUCHDOWN! You caught the defense sleeping.")
                st.session_state.score["User"] += 7

    if st.button("Reset Game"):
        st.session_state.game_started = False
        st.rerun()
