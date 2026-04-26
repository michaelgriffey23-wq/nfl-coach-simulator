import streamlit as st
import random

# 1. Initialize session state so the app remembers your team and score
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.user_team = ""
    st.session_state.score_user = 0
    st.session_state.score_cpu = 0

st.title("🏈 NFL Coach Simulator: 2026 Season")

# 2. The 32 NFL Teams from your screenshot
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

# 3. TEAM SELECTION MENU (This completely replaces the old input() line)
if not st.session_state.game_started:
    st.subheader("Welcome Coach!")
    
    # Streamlit dropdown menu instead of terminal input
    selected_team = st.selectbox("Select your franchise:", teams)
    
    # Start button
    if st.button("Start Game"):
        st.session_state.user_team = selected_team
        st.session_state.game_started = True
        st.rerun()

# 4. THE GAME ENGINE
if st.session_state.game_started:
    st.success(f"You are now coaching the {st.session_state.user_team}!")
    st.write(f"**Score:** {st.session_state.user_team}: {st.session_state.score_user} | CPU: {st.session_state.score_cpu}")
    
    st.write("### Call Your Next Play")
    
    # Use interactive buttons instead of input() for the plays
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Run the Ball"):
            yards = random.randint(-2, 8)
            st.info(f"You ran the ball for {yards} yards.")
            
    with col2:
        if st.button("Short Pass"):
            yards = random.randint(0, 15)
            st.info(f"Short pass complete for {yards} yards.")
            
    with col3:
        if st.button("Deep Pass"):
            success = random.choice([True, False])
            if success:
                st.warning("Touchdown! 40 yard bomb!")
                st.session_state.score_user += 7
            else:
                st.error("Incomplete. Defense swatted it away.")

    # Reset button to go back to the team menu
    st.divider()
    if st.button("Quit Game / Select New Team"):
        st.session_state.game_started = False
        st.session_state.score_user = 0
        st.session_state.score_cpu = 0
        st.rerun()
