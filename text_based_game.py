import streamlit as st
import random

# ==========================================
# 1. THE GAME ENGINE (Exact same logic/math)
# ==========================================
class NFLMasterSim:
    def __init__(self):
        # ALL 32 TEAMS with 2026 Ratings (Unchanged)
        self.nfl_teams = {
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
        self.user_team = ""
        self.opponent = ""
        self.score = { "User": 0, "Opp": 0 }
        self.yard_line = 25
        self.down = 1
        self.ytg = 10
        self.quarter = 1
        self.clock = 10
        self.current_week = 1
        self.season_record = {"W": 0, "L": 0}
        self.is_user_offense = True
        self.game_log = ["The 2026 Season kicks off today."]
        self.user_tendencies = {'1': 0, '2': 0, '3': 0, '5': 0}
        self.runs_this_drive = 0
        self.last_sim_result = ""

    def set_new_opponent(self):
        remaining = [t for t in self.nfl_teams.keys() if t != self.user_team]
        self.opponent = random.choice(remaining)
        self.score = {self.user_team: 0, self.opponent: 0}
        self.quarter = 1
        self.clock = 10
        self.yard_line = 25
        self.down = 1
        self.ytg = 10
        self.is_user_offense = True

    def sim_week_logic(self):
        u_pwr = (self.nfl_teams[self.user_team]['off'] + self.nfl_teams[self.user_team]['def'])
        o_pwr = (self.nfl_teams[self.opponent]['off'] + self.nfl_teams[self.opponent]['def'])
        u_s = random.randint(10, 35) + int((u_pwr - o_pwr)/5)
        o_s = random.randint(10, 35) + int((o_pwr - u_pwr)/5)

        self.last_sim_result = f"FINAL: {self.user_team} {u_s} - {self.opponent} {o_s}"
        if u_s > o_s: self.season_record["W"] += 1
        else: self.season_record["L"] += 1
        self.current_week += 1
        self.set_new_opponent()

    def resolve_play(self, o_c, d_c, o_n, d_n):
        o_r = self.nfl_teams[o_n]['off']; d_r = self.nfl_teams[d_n]['def']
        g = random.randint(-1, 9) + (o_r - d_r) * 0.1
        if o_c == '1' and d_c == '1': g -= 5
        return int(g)

    def update_drive(self):
        if self.yard_line >= 100:
            self.score[self.user_team if self.is_user_offense else self.opponent] += 7
            self.game_log.append("TOUCHDOWN!")
            self.swap()
        elif self.ytg <= 0:
            self.down = 1; self.ytg = 10
            self.game_log.append("First Down!")
        else:
            self.down += 1
            if self.down > 4: 
                self.game_log.append("Turnover on downs!")
                self.swap()

    def special_teams(self):
        if self.yard_line > 65: 
            self.score[self.user_team] += 3
            self.game_log.append("FG Good!")
        else: 
            self.game_log.append("Punted.")
        self.swap()

    def swap(self):
        self.is_user_offense = not self.is_user_offense
        self.yard_line = 25; self.down = 1; self.ytg = 10
        self.game_log.append("[POSSESSION CHANGE]")

# ==========================================
# 2. STREAMLIT WEB UI SETUP
# ==========================================
st.set_page_config(page_title="NFL Coach Master", layout="centered")

# Initialize the game logic in session memory
if 'sim' not in st.session_state:
    st.session_state.sim = NFLMasterSim()
    st.session_state.screen = "TEAM_SELECT"

sim = st.session_state.sim

# ==========================================
# 3. SCREEN ROUTING (Replaces While Loops)
# ==========================================

# --- SCREEN 1: TEAM SELECTION ---
if st.session_state.screen == "TEAM_SELECT":
    st.title("🏈 NFL COACH MASTER: 32-TEAM SEASON")
    t_list = sorted(list(sim.nfl_teams.keys()))
    
    selected_team = st.selectbox("Select your team:", t_list)
    if st.button("Confirm Team & Start Season"):
        sim.user_team = selected_team
        sim.set_new_opponent()
        st.session_state.screen = "MAIN_MENU"
        st.rerun()

# --- SCREEN 2: MAIN MENU ---
elif st.session_state.screen == "MAIN_MENU":
    if sim.current_week > 18:
        st.session_state.screen = "SEASON_OVER"
        st.rerun()

    st.title(f"WEEK {sim.current_week}")
    st.subheader(f"{sim.user_team} ({sim.season_record['W']}-{sim.season_record['L']})")
    st.write(f"**UPCOMING:** {sim.user_team} vs {sim.opponent}")
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎮 PLAY GAME (Full Sideline Control)", use_container_width=True):
            st.session_state.screen = "PLAY_GAME"
            st.rerun()
    with col2:
        if st.button("⏩ SIM WEEK (Instant Result)", use_container_width=True):
            sim.sim_week_logic()
            st.session_state.screen = "SIM_RESULT"
            st.rerun()

# --- SCREEN 3: SIMULATION RESULT ---
elif st.session_state.screen == "SIM_RESULT":
    st.title("Simulated Week Result")
    st.success(sim.last_sim_result)
    if st.button("Continue to Next Week"):
        st.session_state.screen = "MAIN_MENU"
        st.rerun()

# --- SCREEN 4: PLAY GAME (The HUD and Playcalling) ---
elif st.session_state.screen == "PLAY_GAME":
    # 1. Draw HUD
    mode = "OFFENSE" if sim.is_user_offense else "DEFENSE"
    st.markdown(f"### 🏟️ {sim.user_team} vs {sim.opponent} | **{mode}**")
    st.markdown(f"**SCORE:** {sim.user_team}: {sim.score[sim.user_team]} - {sim.opponent}: {sim.score[sim.opponent]} | **Q{sim.quarter}** | Plays left: {sim.clock}")
    st.markdown(f"**BALL:** {sim.yard_line}yd line ({sim.down} down & {sim.ytg} to go)")
    st.info(f"**LOG:** {sim.game_log[-1]}")
    st.divider()

    # Helper function to process the turn when a button is clicked
    def execute_play(u_call, is_st=False):
        if sim.is_user_offense:
            if is_st:
                sim.special_teams()
            else:
                c_def = str(random.randint(1, 3))
                gain = sim.resolve_play(u_call, c_def, sim.user_team, sim.opponent)
                sim.yard_line += gain
                sim.ytg -= gain
                sim.game_log.append(f"You gained {gain}yds.")
                sim.update_drive()
        else:
            c_off = str(random.randint(1, 3))
            gain = sim.resolve_play(c_off, u_call, sim.opponent, sim.user_team)
            sim.yard_line += gain
            sim.ytg -= gain
            sim.game_log.append(f"Opponent gained {gain}yds.")
            sim.update_drive()

        sim.clock -= 1
        
        # Quarter / Game Over Logic
        if sim.clock <= 0:
            sim.quarter += 1
            sim.clock = 10
            sim.game_log.append(f"--- END OF Q{sim.quarter-1} ---")
            if sim.quarter > 4:
                st.session_state.screen = "GAME_OVER"

    # 2. Draw Playcalling Buttons based on possession
    st.write("**Call your play:**")
    if sim.is_user_offense:
        c1, c2, c3, c4, c5 = st.columns(5)
        if c1.button("1. Run"): 
            execute_play('1')
            st.rerun()
        if c2.button("2. Pass"): 
            execute_play('2')
            st.rerun()
        if c3.button("3. Deep"): 
            execute_play('3')
            st.rerun()
        if c4.button("4. Punt/FG"): 
            execute_play('4', is_st=True)
            st.rerun()
        if c5.button("5. PA"): 
            execute_play('5')
            st.rerun()
    else:
        c1, c2, c3 = st.columns(3)
        if c1.button("1. Base"): 
            execute_play('1')
            st.rerun()
        if c2.button("2. Nickel"): 
            execute_play('2')
            st.rerun()
        if c3.button("3. Blitz"): 
            execute_play('3')
            st.rerun()

# --- SCREEN 5: GAME OVER SUMMARY ---
elif st.session_state.screen == "GAME_OVER":
    st.title("GAME OVER")
    st.subheader(f"FINAL SCORE: {sim.user_team} {sim.score[sim.user_team]} - {sim.opponent} {sim.score[sim.opponent]}")
    
    if st.button("Advance to Next Week"):
        if sim.score[sim.user_team] > sim.score[sim.opponent]: 
            sim.season_record["W"] += 1
        else: 
            sim.season_record["L"] += 1
        sim.current_week += 1
        sim.set_new_opponent()
        st.session_state.screen = "MAIN_MENU"
        st.rerun()

# --- SCREEN 6: SEASON OVER ---
elif st.session_state.screen == "SEASON_OVER":
    st.title("🏆 SEASON OVER!")
    st.header(f"Final Record: {sim.season_record['W']} Wins - {sim.season_record['L']} Losses")
    if st.button("Start New Season"):
        # Wipes memory completely and starts fresh
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
