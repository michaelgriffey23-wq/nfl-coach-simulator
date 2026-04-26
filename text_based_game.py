import streamlit as st
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="NFL Coach Master 2026", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'game' not in st.session_state:
    st.session_state.nfl_teams = {
        "Buffalo Bills": {"off": 95, "def": 86}, "Miami Dolphins": {"off": 92, "def": 78},
        "New England Patriots": {"off": 94, "def": 95}, "New York Jets": {"off": 76, "def": 86},
        "Baltimore Ravens": {"off": 92, "def": 89}, "Cincinnati Bengals": {"off": 90, "def": 81},
        "Cleveland Browns": {"off": 78, "def": 89}, "Pittsburgh Steelers": {"off": 80, "def": 91},
        "Houston Texans": {"off": 90, "def": 95}, "Indianapolis Colts": {"off": 87, "def": 83},
        "Jacksonville Jaguars": {"off": 85, "def": 85}, "Tennessee Titans": {"off": 74, "def": 79},
        "Denver Broncos": {"off": 82, "def": 92}, "Kansas City Chiefs": {"off": 91, "def": 84},
        "Las Vegas Raiders": {"off": 75, "def": 80}, "Los Angeles Chargers": {"off": 85, "def": 81},
        "Dallas Cowboys": {"off": 87, "def": 82}, "New York Giants": {"off": 77, "def": 78},
        "Philadelphia Eagles": {"off": 89, "def": 87}, "Washington Commanders": {"off": 81, "def": 79},
        "Chicago Bears": {"off": 88, "def": 89}, "Detroit Lions": {"off": 94, "def": 82},
        "Green Bay Packers": {"off": 89, "def": 85}, "Minnesota Vikings": {"off": 84, "def": 88},
        "Atlanta Falcons": {"off": 86, "def": 82}, "Carolina Panthers": {"off": 75, "def": 79},
        "New Orleans Saints": {"off": 79, "def": 83}, "Tampa Bay Buccaneers": {"off": 82, "def": 84},
        "Arizona Cardinals": {"off": 83, "def": 74}, "Los Angeles Rams": {"off": 96, "def": 91},
        "San Francisco 49ers": {"off": 88, "def": 90}, "Seattle Seahawks": {"off": 92, "def": 97}
    }
    st.session_state.user_team = None
    st.session_state.opponent = None
    st.session_state.score = {"User": 0, "Opp": 0}
    st.session_state.yard_line = 25
    st.session_state.down = 1
    st.session_state.ytg = 10
    st.session_state.quarter = 1
    st.session_state.clock = 10
    st.session_state.current_week = 1
    st.session_state.record = {"W": 0, "L": 0}
    st.session_state.game_log = ["The 2026 Season kicks off today."]
    st.session_state.is_offense = True
    st.session_state.game_active = False

# --- HELPER FUNCTIONS ---
def set_opponent():
    teams = [t for t in st.session_state.nfl_teams.keys() if t != st.session_state.user_team]
    st.session_state.opponent = random.choice(teams)
    st.session_state.score = {st.session_state.user_team: 0, st.session_state.opponent: 0}
    st.session_state.quarter = 1
    st.session_state.clock = 15

def resolve_play(off_call, def_call, off_team, def_team):
    off_r = st.session_state.nfl_teams[off_team]['off']
    def_r = st.session_state.nfl_teams[def_team]['def']
    gain = random.randint(-2, 12) + (off_r - def_r) * 0.1
    # Logic modifiers
    if off_call == def_call: gain -= 5
    return int(gain)

def swap_possession():
    st.session_state.is_offense = not st.session_state.is_offense
    st.session_state.yard_line = 25
    st.session_state.down = 1
    st.session_state.ytg = 10
    st.session_state.game_log.append("--- POSSESSION CHANGE ---")

def update_game(gain):
    st.session_state.yard_line += gain
    st.session_state.ytg -= gain
    st.session_state.clock -= 1
    
    if st.session_state.yard_line >= 100:
        scorer = st.session_state.user_team if st.session_state.is_offense else st.session_state.opponent
        st.session_state.score[scorer] += 7
        st.session_state.game_log.append(f"TOUCHDOWN {scorer}!")
        swap_possession()
    elif st.session_state.ytg <= 0:
        st.session_state.down = 1
        st.session_state.ytg = 10
    else:
        st.session_state.down += 1
        if st.session_state.down > 4:
            st.session_state.game_log.append("Turnover on Downs!")
            swap_possession()

# --- SIDEBAR: TEAM SELECTION ---
with st.sidebar:
    st.title("🏈 Team Management")
    if not st.session_state.user_team:
        team_choice = st.selectbox("Select Your Franchise", sorted(st.session_state.nfl_teams.keys()))
        if st.button("Confirm Selection"):
            st.session_state.user_team = team_choice
            set_opponent()
            st.rerun()
    else:
        st.metric("Your Team", st.session_state.user_team)
        st.metric("Record", f"{st.session_state.record['W']} - {st.session_state.record['L']}")
        st.write(f"**Week {st.session_state.current_week} Opponent:** {st.session_state.opponent}")
        if st.button("Reset Season"):
            st.session_state.clear()
            st.rerun()

# --- MAIN INTERFACE ---
if st.session_state.user_team:
    st.title(f"🏈 {st.session_state.user_team} vs {st.session_state.opponent}")
    
    # HUD
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Score", f"{st.session_state.score[st.session_state.user_team]} - {st.session_state.score[st.session_state.opponent]}")
    c2.metric("Quarter", st.session_state.quarter)
    c3.metric("Yard Line", f"{st.session_state.yard_line} yd")
    c4.metric("Down & Distance", f"{st.session_state.down} & {st.session_state.ytg}")

    # PLAY CALLING
    st.divider()
    if st.session_state.clock > 0:
        if st.session_state.is_offense:
            st.subheader("📢 Offensive Play Call")
            col_off1, col_off2, col_off3, col_off4 = st.columns(4)
            if col_off1.button("🏃 Run"):
                gain = resolve_play("Run", str(random.randint(1,2)), st.session_state.user_team, st.session_state.opponent)
                st.session_state.game_log.append(f"{st.session_state.user_team} runs for {gain} yards.")
                update_game(gain); st.rerun()
            if col_off2.button("🎯 Pass"):
                gain = resolve_play("Pass", str(random.randint(1,2)), st.session_state.user_team, st.session_state.opponent)
                st.session_state.game_log.append(f"{st.session_state.user_team} passes for {gain} yards.")
                update_game(gain); st.rerun()
            if col_off3.button("🚀 Deep Shot"):
                gain = random.randint(-5, 40)
                st.session_state.game_log.append(f"Deep ball result: {gain} yards.")
                update_game(gain); st.rerun()
            if col_off4.button("🦵 Punt/FG"):
                if st.session_state.yard_line > 65:
                    st.session_state.score[st.session_state.user_team] += 3
                    st.session_state.game_log.append("Field Goal is GOOD!")
                else: st.session_state.game_log.append("Punted away.")
                swap_possession(); st.rerun()
        else:
            st.subheader("🛡️ Defensive Scheme")
            col_def1, col_def2, col_def3 = st.columns(3)
            if col_def1.button("Base Defense"):
                gain = resolve_play(str(random.randint(1,2)), "Base", st.session_state.opponent, st.session_state.user_team)
                st.session_state.game_log.append(f"Opponent gains {gain} yards.")
                update_game(gain); st.rerun()
            if col_def2.button("Nickel (Pass D)"):
                gain = resolve_play("Pass", "Nickel", st.session_state.opponent, st.session_state.user_team)
                st.session_state.game_log.append(f"Nickel coverage holds them to {gain} yards.")
                update_game(gain); st.rerun()
            if col_def3.button("All-Out Blitz"):
                gain = random.randint(-10, 20)
                st.session_state.game_log.append(f"Blitz result: {gain} yards.")
                update_game(gain); st.rerun()
    else:
        # END OF GAME LOGIC
        st.success("Game Over!")
        if st.session_state.score[st.session_state.user_team] > st.session_state.score[st.session_state.opponent]:
            st.session_state.record['W'] += 1
            st.balloons()
        else:
            st.session_state.record['L'] += 1
        
        if st.button("Advance to Next Week"):
            st.session_state.current_week += 1
            set_opponent()
            st.rerun()

    # GAME LOG
    st.divider()
    st.text_area("Live Game Log", "\n".join(st.session_state.game_log[-5:]), height=150)
else:
    st.info("Please select a team in the sidebar to begin your 2026 Season.")
