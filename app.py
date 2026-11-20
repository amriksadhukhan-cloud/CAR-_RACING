import streamlit as st
import random

# ==================================================
# PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="Neon Racing | Car Racing Game",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080D18, #111D30);
    color: white;
}
header[data-testid="stHeader"] { background: transparent; }
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3, p, label { color: white; }
.game-title {
    text-align: center;
    font-size: 44px;
    font-weight: 900;
    letter-spacing: 4px;
    color: #00E5FF;
    margin-bottom: 0;
}
.game-subtitle {
    text-align: center;
    color: #94A3B8;
    font-size: 13px;
    letter-spacing: 2px;
    margin-bottom: 30px;
}
.stat-card {
    background: linear-gradient(145deg, #192941, #101B2D);
    border: 1px solid #30445F;
    border-radius: 16px;
    padding: 18px 10px;
    text-align: center;
    min-height: 105px;
}
.stat-label {
    color: #94A3B8;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 1px;
}
.stat-value {
    color: #00E5FF;
    font-size: 32px;
    font-weight: 900;
    margin-top: 8px;
}
.road-container {
    max-width: 600px;
    margin: 15px auto;
    padding: 12px;
    background: #080D14;
    border: 3px solid #334155;
    border-radius: 16px;
    box-shadow: 0 0 25px rgba(0,229,255,0.12);
}
.road-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 4px;
    background: #0B111B;
    padding: 5px;
    border-radius: 8px;
}
.road-cell {
    height: 65px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    background: linear-gradient(90deg, #202C3B, #29384B, #202C3B);
    border-bottom: 1px dashed #64748B;
}
.player-cell {
    background: linear-gradient(135deg, #07516B, #123E51);
    border: 2px solid #00E5FF;
    border-radius: 8px;
    box-shadow: 0 0 15px rgba(0,229,255,0.4);
}
.traffic-cell {
    background: linear-gradient(135deg, #642A37, #401C28);
    border: 1px solid #F43F5E;
    border-radius: 8px;
}
.status-box {
    background: #14243A;
    border: 1px solid #30445F;
    border-radius: 12px;
    padding: 14px;
    text-align: center;
    color: #CBD5E1;
    margin: 15px 0;
}
.game-over {
    text-align: center;
    background: linear-gradient(135deg, #451B2B, #251526);
    border: 1px solid #F43F5E;
    border-radius: 16px;
    padding: 20px;
    margin: 15px 0;
}
.game-over h2 { color: #FB7185; }
.footer {
    text-align: center;
    color: #64748B;
    font-size: 12px;
    margin-top: 35px;
    letter-spacing: 1px;
}
div.stButton > button {
    width: 100%;
    height: 52px;
    border-radius: 12px;
    font-weight: bold;
    background: #142B42;
    color: #00E5FF;
    border: 1px solid #087E95;
    transition: 0.2s;
}
div.stButton > button:hover {
    background: #00AFC5;
    color: #07111E;
    border-color: #00E5FF;
}
@media(max-width: 600px) {
    .game-title { font-size: 29px; }
    .road-cell { height: 55px; font-size: 25px; }
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# INITIALIZE GAME
# ==================================================
def initialize_game():
    high_score = st.session_state.get("high_score", 0)
    st.session_state.player_lane = 1
    st.session_state.obstacles = []
    st.session_state.score = 0
    st.session_state.running = True
    st.session_state.game_over = False
    st.session_state.high_score = high_score

if "running" not in st.session_state:
    initialize_game()

# ==================================================
# PLAYER MOVEMENT
# ==================================================
def move_left():
    if st.session_state.running and st.session_state.player_lane > 0:
        st.session_state.player_lane -= 1

def move_right():
    if st.session_state.running and st.session_state.player_lane < 2:
        st.session_state.player_lane += 1

# ==================================================
# DRIVE FUNCTION
# ==================================================
def drive():
    if not st.session_state.running:
        return

    player_lane = st.session_state.player_lane
    updated_obstacles = []
    collision = False

    # Advance existing traffic by one row.
    for obstacle in st.session_state.obstacles:
        new_row = obstacle["row"] + 1

        if new_row == 5 and obstacle["lane"] == player_lane:
            collision = True
        elif new_row < 6:
            updated_obstacles.append({
                "lane": obstacle["lane"],
                "row": new_row
            })

    st.session_state.obstacles = updated_obstacles

    if collision:
        st.session_state.running = False
        st.session_state.game_over = True
        st.session_state.high_score = max(
            st.session_state.high_score,
            st.session_state.score
        )
        return

    st.session_state.score += 10

    # Traffic becomes more frequent as the score increases.
    spawn_probability = min(
        0.30 + (st.session_state.score // 10) * 0.015,
        0.75
    )

    if random.random() < spawn_probability:
        available_lanes = [
            lane for lane in range(3)
            if not any(
                obs["lane"] == lane and obs["row"] == 0
                for obs in st.session_state.obstacles
            )
        ]

        if available_lanes:
            new_lane = random.choice(available_lanes)
            st.session_state.obstacles.append({
                "lane": new_lane,
                "row": 0
            })

# ==================================================
# HEADER
# ==================================================
st.markdown("""
<div class="game-title">🏎️ NEON RACING</div>
<div class="game-subtitle">
    ARCADE RACING EXPERIENCE • AVOID TRAFFIC • BEAT YOUR RECORD
</div>
""", unsafe_allow_html=True)

# ==================================================
# DASHBOARD
# ==================================================
score = st.session_state.score
level = min(1 + score // 100, 10)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">🏁 CURRENT SCORE</div>
        <div class="stat-value">{score}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">🏆 BEST SCORE</div>
        <div class="stat-value">{st.session_state.high_score}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">⚡ RACING LEVEL</div>
        <div class="stat-value">{level}</div>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# GAME STATUS
# ==================================================
if st.session_state.running:
    st.markdown("""
    <div class="status-box">
        🟢 RACE IN PROGRESS<br>
        Avoid incoming traffic and survive as long as possible!
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# RACING TRACK
# ==================================================
st.markdown("""
<h3 style="text-align:center; color:#00E5FF;">🏁 RACING TRACK</h3>
""", unsafe_allow_html=True)

player_lane = st.session_state.player_lane
obstacles = st.session_state.obstacles

road_html = '<div class="road-container"><div class="road-grid">'

for row in range(6):
    for lane in range(3):
        emoji = ""
        cell_class = "road-cell"

        if row == 5 and lane == player_lane:
            emoji = "🏎️"
            cell_class += " player-cell"
        elif any(
            obs["lane"] == lane and obs["row"] == row
            for obs in obstacles
        ):
            emoji = "🚙"
            cell_class += " traffic-cell"

        road_html += f'<div class="{cell_class}">{emoji}</div>'

road_html += "</div></div>"
st.markdown(road_html, unsafe_allow_html=True)

st.markdown("""
<p style="text-align:center; color:#94A3B8;">
    🚙 INCOMING TRAFFIC &nbsp;&nbsp; | &nbsp;&nbsp; 🏎️ YOUR CAR
</p>
""", unsafe_allow_html=True)

# ==================================================
# GAME OVER
# ==================================================
if st.session_state.game_over:
    st.markdown(f"""
    <div class="game-over">
        <h2>💥 GAME OVER!</h2>
        <h3>Final Score: {score}</h3>
        <p>You collided with another vehicle!</p>
        <p>Try again and beat your best score.</p>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# GAME CONTROLS
# ==================================================
st.markdown("""
<h3 style="text-align:center; color:#00E5FF;">🎮 GAME CONTROLS</h3>
""", unsafe_allow_html=True)

left, center, right = st.columns([1, 1.5, 1])

with left:
    st.button(
        "⬅️ LEFT",
        on_click=move_left,
        disabled=not st.session_state.running,
        use_container_width=True
    )

with center:
    st.button(
        "🏎️ DRIVE",
        on_click=drive,
        disabled=not st.session_state.running,
        type="primary",
        use_container_width=True
    )

with right:
    st.button(
        "RIGHT ➡️",
        on_click=move_right,
        disabled=not st.session_state.running,
        use_container_width=True
    )

# ==================================================
# RESTART BUTTON
# ==================================================
if st.button("🔄 RESTART RACE", use_container_width=True):
    initialize_game()
    st.rerun()

# ==================================================
# INSTRUCTIONS
# ==================================================
with st.expander("📖 HOW TO PLAY"):
    st.markdown("""
    ### Racing Instructions
    1. Click LEFT to move your car to the left lane.
    2. Click RIGHT to move your car to the right lane.
    3. Click DRIVE to move the traffic forward.
    4. Avoid incoming vehicles.
    5. Every successful drive earns 10 points.
    6. Traffic frequency increases as your score grows.
    7. If another car reaches your lane, the game ends.

    ### Winning Tips
    - Watch the traffic carefully.
    - Change lanes before pressing DRIVE.
    - Avoid staying in a dangerous lane.
    - Try to beat your high score!
    """)

# ==================================================
# FOOTER
# ==================================================
st.markdown("""
<div class="footer">
    NEON RACING • POWERED BY PYTHON & STREAMLIT
    <br><br>
    DRIVE SMART. RACE HARD. BREAK RECORDS.
</div>
""", unsafe_allow_html=True)
