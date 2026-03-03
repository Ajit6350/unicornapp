import streamlit as st
import requests

API_BASE = "https://king63500-unicorn.hf.space"

st.set_page_config(page_title="🦄 Unicorn Pro", layout="wide")
st.title("🦄 Unicorn Pro - AI Casino Assistant")

# -------------------- UI (Responsive) --------------------
st.markdown(
    """
<style>
  /* ---------- Global Styles ---------- */
  .main, .block-container {
    max-width: 100%;
    padding-top: 1rem;
    padding-bottom: 2.5rem;
  }

  /* ---------- Streamlit default overrides ---------- */
  div[data-testid="stHorizontalBlock"] {
    flex-wrap: wrap !important;
    gap: 1.5rem !important;
  }
  @media (max-width: 900px) {
    div[data-testid="column"] {
      flex: 1 1 100% !important;
      width: 100% !important;
    }
  }

  /* ---------- Card Style for Sections ---------- */
  .card {
    background: rgba(30, 30, 40, 0.7);
    backdrop-filter: blur(8px);
    border-radius: 20px;
    padding: 1.5rem;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    margin-bottom: 1.5rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .card:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.6);
  }

  /* ---------- Headers ---------- */
  h1, h2, h3 {
    font-family: 'Segoe UI', 'Courier New', monospace;
    letter-spacing: 0.5px;
    font-weight: 600;
  }
  h1 {
    font-size: 2.5rem;
    background: linear-gradient(135deg, #ff6b6b, #4d79ff, #5cd65c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 1.5rem;
  }
  h2 {
    font-size: 1.8rem;
    border-bottom: 2px solid rgba(255,255,255,0.1);
    padding-bottom: 0.5rem;
    margin-top: 1rem;
  }

  /* ---------- Buttons ---------- */
  .stButton > button {
    border: none;
    border-radius: 40px;
    padding: 0.6rem 1.2rem;
    font-weight: 700;
    font-size: 1rem;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    transition: all 0.2s ease;
    width: 100%;
    border: 1px solid rgba(255,255,255,0.1);
  }
  .stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    background: linear-gradient(135deg, #764ba2, #667eea);
  }

  /* ---------- Outcome Buttons (custom) ---------- */
  .outcome-buttons {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
  }
  .outcome-btn {
    flex: 1;
    border: none;
    border-radius: 40px;
    padding: 1rem 0;
    font-weight: 800;
    font-size: 1.4rem;
    color: white;
    cursor: pointer;
    transition: all 0.2s;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    text-align: center;
  }
  .outcome-btn:hover {
    transform: scale(1.05);
    filter: brightness(1.1);
  }
  .btn-baccarat-b, .btn-roulette-r { background: linear-gradient(145deg, #ff4d4d, #cc0000); }
  .btn-baccarat-p, .btn-roulette-b { background: linear-gradient(145deg, #4d79ff, #003399); }
  .btn-baccarat-t, .btn-roulette-g { background: linear-gradient(145deg, #5cd65c, #008000); }

  /* ---------- Bead Plate ---------- */
  .bead-plate-scroll {
    max-width: 100%;
    height: 380px;
    overflow-y: auto;
    overflow-x: hidden;
    border-radius: 20px;
    padding: 1rem;
    background: rgba(20, 20, 30, 0.7);
    backdrop-filter: blur(4px);
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 1rem;
  }
  .bead-plate {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(38px, 1fr));
    gap: 8px;
  }
  .bead {
    aspect-ratio: 1/1;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1rem;
    color: #fff;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    box-shadow: 0 4px 8px rgba(0,0,0,0.3), inset 0 2px 4px rgba(255,255,255,0.3);
    transition: transform 0.2s;
    cursor: default;
  }
  .bead:hover {
    transform: scale(1.1);
    z-index: 2;
  }
  .bead-baccarat-b { background: radial-gradient(circle at 30% 30%, #ff9999, #ff4d4d); }
  .bead-baccarat-p { background: radial-gradient(circle at 30% 30%, #99c2ff, #4d79ff); }
  .bead-baccarat-t { background: radial-gradient(circle at 30% 30%, #b3ffb3, #5cd65c); }
  .bead-roulette-r { background: radial-gradient(circle at 30% 30%, #ff9999, #ff4d4d); }
  .bead-roulette-b { background: radial-gradient(circle at 30% 30%, #666666, #333333); }
  .bead-roulette-g { background: radial-gradient(circle at 30% 30%, #b3ffb3, #5cd65c); }
  .bead-unknown { background: #888; }

  /* ---------- Metric Cards ---------- */
  .metric-card {
    background: rgba(30, 30, 40, 0.8);
    border-radius: 16px;
    padding: 1rem;
    border: 1px solid rgba(255,255,255,0.05);
    backdrop-filter: blur(4px);
    margin: 0.5rem 0;
  }
  .metric-card .label {
    font-size: 0.9rem;
    color: #aaa;
    letter-spacing: 0.5px;
  }
  .metric-card .value {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.2;
  }
  .value-positive { color: #00c851; }
  .value-negative { color: #ff4444; }

  /* ---------- Status Badges ---------- */
  .status-badge {
    display: inline-block;
    padding: 0.2rem 1rem;
    border-radius: 30px;
    font-weight: 700;
    font-size: 0.9rem;
    margin: 0.2rem 0;
    text-align: center;
    background: rgba(0,0,0,0.3);
    border: 1px solid;
  }
  .badge-aggressive { border-color: #00c851; color: #00c851; }
  .badge-stable    { border-color: #ffbb33; color: #ffbb33; }
  .badge-choppy    { border-color: #ff8800; color: #ff8800; }
  .badge-outofsync { border-color: #ff4444; color: #ff4444; }

  /* ---------- Health Indicator ---------- */
  .health-indicator {
    position: fixed;
    top: 16px;
    right: 20px;
    z-index: 9999;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-radius: 40px;
    background: rgba(20,20,30,0.9);
    backdrop-filter: blur(8px);
    color: white;
    font-size: 0.9rem;
    font-weight: 500;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 20px rgba(0,0,0,0.5);
  }
  .health-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }
  .health-dot.ok { background: #00c851; box-shadow: 0 0 10px #00c851; }
  .health-dot.bad { background: #ff4444; box-shadow: 0 0 10px #ff4444; }

  /* ---------- Expander Styles ---------- */
  .streamlit-expanderHeader {
    font-weight: 600;
    background: rgba(255,255,255,0.05);
    border-radius: 30px;
    padding: 0.5rem 1rem;
    border: none;
  }
  .streamlit-expanderContent {
    background: rgba(0,0,0,0.2);
    border-radius: 16px;
    padding: 1rem;
  }
</style>
""",
    unsafe_allow_html=True,
)

# -------------------- SESSION STATE --------------------
if 'history' not in st.session_state:
    st.session_state.history = []
if 'profit_loss_units' not in st.session_state:
    st.session_state.profit_loss_units = 0
if 'recent_results' not in st.session_state:
    st.session_state.recent_results = []
if 'game' not in st.session_state:
    st.session_state.game = "Baccarat"
if 'last_prediction' not in st.session_state:
    st.session_state.last_prediction = None
if 'db_stats' not in st.session_state:
    st.session_state.db_stats = {"shoes": 0, "hands": 0, "status": False}
if 'dna_stats' not in st.session_state:
    st.session_state.dna_stats = {"streak": {}, "zigzag": {}}
if 'window' not in st.session_state:
    st.session_state.window = 15
if 'base_bet' not in st.session_state:
    st.session_state.base_bet = 20.0
if 'use_lstm' not in st.session_state:
    st.session_state.use_lstm = True
if 'health' not in st.session_state:
    st.session_state.health = {"ok": False, "components": []}
if 'model_info' not in st.session_state:
    st.session_state.model_info = None

# -------------------- HELPER FUNCTIONS --------------------
def fetch_prediction():
    payload = {
        "history": st.session_state.history,
        "game": st.session_state.game,
        "base_bet": st.session_state.base_bet,
        "use_lstm": st.session_state.use_lstm,
        "recent_results": st.session_state.recent_results
    }
    try:
        resp = requests.post(f"{API_BASE}/predict", json=payload, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            st.session_state.last_prediction = data
            if 'debug_info' in data and 'window' in data['debug_info']:
                st.session_state.window = data['debug_info']['window']
        else:
            st.warning(f"Prediction API returned {resp.status_code}")
            st.session_state.last_prediction = None
    except Exception as e:
        st.error(f"Prediction error: {e}")
        st.session_state.last_prediction = None

def fetch_dna():
    payload = {"history": st.session_state.history, "game": st.session_state.game}
    try:
        resp = requests.post(f"{API_BASE}/dna", json=payload, timeout=10)
        if resp.status_code == 200:
            st.session_state.dna_stats = resp.json()
        else:
            st.session_state.dna_stats = {"streak": {}, "zigzag": {}}
    except Exception as e:
        st.warning(f"DNA fetch failed: {e}")
        st.session_state.dna_stats = {"streak": {}, "zigzag": {}}

def fetch_stats():
    try:
        resp = requests.get(f"{API_BASE}/stats", params={"game": st.session_state.game})
        if resp.status_code == 200:
            st.session_state.db_stats = resp.json()
        else:
            st.session_state.db_stats = {"shoes": 0, "hands": 0, "status": False}
    except:
        st.session_state.db_stats = {"shoes": 0, "hands": 0, "status": False}

def fetch_health():
    try:
        resp = requests.get(f"{API_BASE}/health", timeout=10)
        if resp.status_code == 200:
            st.session_state.health = resp.json()
        else:
            st.session_state.health = {
                "ok": False,
                "components": [{"name": "backend", "ok": False, "message": f"HTTP {resp.status_code}"}]
            }
    except Exception as e:
        st.session_state.health = {
            "ok": False,
            "components": [{"name": "backend", "ok": False, "message": str(e)}]
        }

def fetch_model_info():
    try:
        resp = requests.get(f"{API_BASE}/model_info", timeout=10)
        if resp.status_code == 200:
            st.session_state.model_info = resp.json()
        else:
            st.session_state.model_info = None
    except Exception:
        st.session_state.model_info = None

def _bead_css_class(outcome: str, game: str) -> str:
    base = "bead"
    if game == "Roulette":
        if outcome == "R":
            return f"{base} bead-roulette-r"
        if outcome == "B":
            return f"{base} bead-roulette-b"
        if outcome == "G":
            return f"{base} bead-roulette-g"
        return f"{base} bead-unknown"
    if outcome == "B":
        return f"{base} bead-baccarat-b"
    if outcome == "P":
        return f"{base} bead-baccarat-p"
    if outcome == "T":
        return f"{base} bead-baccarat-t"
    return f"{base} bead-unknown"

def render_bead_plate(history, game: str):
    if not history:
        st.info("No hands yet. Click the buttons below to start.")
        return
    beads = []
    for outcome in history:
        cls = _bead_css_class(outcome, game)
        beads.append(f"<div class='{cls}' title='{outcome}'>{outcome}</div>")
    html = f"""
    <div class='bead-plate-scroll'>
        <div class='bead-plate'>
            {''.join(beads)}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def reload_data():
    with st.spinner("Reloading data and retraining AI..."):
        try:
            resp = requests.post(f"{API_BASE}/reload", json={"game": st.session_state.game})
            if resp.status_code == 200:
                fetch_stats()
                fetch_model_info()
                st.success("Data reloaded and AI retrained!")
            else:
                st.error(f"Reload failed with status {resp.status_code}")
        except Exception as e:
            st.error(f"Reload error: {e}")

def save_shoe():
    payload = {"history": st.session_state.history, "game": st.session_state.game}
    try:
        resp = requests.post(f"{API_BASE}/save", json=payload)
        if resp.status_code == 200 and resp.json().get("success"):
            st.success("Shoe saved successfully!")
            fetch_stats()
        else:
            st.error("Save failed")
    except Exception as e:
        st.error(f"Save error: {e}")

def record_and_fetch(outcome):
    if st.session_state.last_prediction and st.session_state.last_prediction.get('bet'):
        last = st.session_state.last_prediction
        bet = last.get('bet')
        kelly_units = last.get('kelly_amount', 0)
        if outcome == bet:
            if st.session_state.game == "Baccarat" and bet == 'B':
                profit_units = kelly_units * 0.95
            else:
                profit_units = kelly_units
            st.session_state.profit_loss_units += profit_units
            st.session_state.recent_results.append(1)
        elif outcome in ('T', 'G'):
            st.session_state.recent_results.append(2)
        else:
            st.session_state.profit_loss_units -= kelly_units
            st.session_state.recent_results.append(0)
    st.session_state.history.append(outcome)
    fetch_prediction()
    fetch_dna()

def get_win_streak():
    streak = 0
    for r in reversed(st.session_state.recent_results):
        if r == 1:
            streak += 1
        else:
            break
    return streak

def get_loss_streak():
    streak = 0
    for r in reversed(st.session_state.recent_results):
        if r == 0:
            streak += 1
        else:
            break
    return streak

# -------------------- INITIAL FETCH --------------------
fetch_health()
if st.session_state.db_stats['shoes'] == 0:
    fetch_stats()
if st.session_state.model_info is None:
    fetch_model_info()

# -------------------- HEALTH INDICATOR --------------------
health = st.session_state.get("health", {})
ok = bool(health.get("ok", False))
components = health.get("components", [])
bad_msgs = [f"{c.get('name')}: {c.get('message')}" for c in components if not c.get("ok", False)]
tooltip = "All systems OK" if ok else ("Issues: " + " | ".join(bad_msgs) if bad_msgs else "Health check failed")
dot_class = "health-dot ok" if ok else "health-dot bad"
label = "ONLINE" if ok else "CHECK"
st.markdown(
    f"""
<div class="health-indicator" title="{tooltip}">
  <div class="{dot_class}"></div>
  <span>{label}</span>
</div>
""",
    unsafe_allow_html=True,
)

# -------------------- LAYOUT --------------------
left_col, mid_col, right_col = st.columns([1.2, 2, 1.2])

# ==================== LEFT COLUMN (SIDEBAR) ====================
with left_col:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.header("🎮 Game Selection")
        game = st.selectbox("Game", ["Baccarat", "Roulette"], key="game_selector")
        if game != st.session_state.game:
            st.session_state.game = game
            st.session_state.history = []
            st.session_state.recent_results = []
            st.session_state.profit_loss_units = 0
            st.session_state.last_prediction = None
            fetch_stats()
            fetch_model_info()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🧠 Session Memory")
        if len(st.session_state.recent_results) >= 5:
            last5 = st.session_state.recent_results[-5:]
            wins = last5.count(1)
            losses = last5.count(0)
            ties = last5.count(2)
            win_pct = wins / 5 * 100
            if win_pct >= 80:
                status = "🚀 AGGRESSIVE (Hot)"
                badge_class = "badge-aggressive"
            elif win_pct >= 60:
                status = "✅ STABLE (Normal)"
                badge_class = "badge-stable"
            elif win_pct >= 40:
                status = "⚠️ CHOPPY (Recalib)"
                badge_class = "badge-choppy"
            else:
                status = "❄️ OUT OF SYNC"
                badge_class = "badge-outofsync"
            pattern = ''.join(['W' if x==1 else 'L' if x==0 else 'T' for x in last5])
            st.markdown(f"<div class='status-badge {badge_class}'>{status}</div>", unsafe_allow_html=True)
            st.write(f"**Wins:** {wins}/5  **Losses:** {losses}/5  **Ties:** {ties}/5")
            st.write(f"**Pattern:** {pattern}  **Window:** {st.session_state.window}")
        else:
            st.write(f"Gathering Data ({len(st.session_state.recent_results)}/5)...")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📡 Database Uplink")
        if st.session_state.db_stats['status']:
            st.success(f"ONLINE ●\nLoaded Shoes: {st.session_state.db_stats['shoes']}\nTotal Hands: {st.session_state.db_stats['hands']}")
        else:
            st.error("OFFLINE ●")
        if st.button("📥 LOAD & TRAIN AI"):
            reload_data()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📈 Model Training Info")
        mi = st.session_state.get("model_info") or {}
        games = mi.get("games", {}) if isinstance(mi, dict) else {}
        g = games.get(st.session_state.game, {}) if isinstance(games, dict) else {}
        if g:
            st.write(f"**Hands Loaded:** {g.get('hands_loaded', 'N/A')}  |  **Shoes Loaded:** {g.get('shoes_loaded', 'N/A')}")
            rf = g.get("rf", {}) or {}
            lstm = g.get("lstm", {}) or {}
            st.write(f"**RF:** trained={rf.get('trained','N/A')} | window={rf.get('window','N/A')} | patterns={rf.get('patterns','N/A')}")
            st.write(f"**LSTM:** window={lstm.get('window','N/A')} | samples={lstm.get('samples','N/A')}")
            note = lstm.get("note")
            if note:
                st.caption(note)
        else:
            st.write("Model info not available (backend may not have `/model_info`).")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🧬 Live Shoe DNA")
        # Backend JSON converts dict keys to strings; normalize to int for lookups below.
        _stk_raw = st.session_state.dna_stats.get('streak', {}) or {}
        _zz_raw = st.session_state.dna_stats.get('zigzag', {}) or {}
        try:
            stk = {int(k): v for k, v in _stk_raw.items()}
        except Exception:
            stk = _stk_raw
        try:
            zz = {int(k): v for k, v in _zz_raw.items()}
        except Exception:
            zz = _zz_raw
        if len(st.session_state.history) < 3:
            st.write("Feed more hands (need at least 3).")
        else:
            st.write("🔥 **STREAK HEALTH**")
            any_streak = False
            for length in range(1,5):
                if length in stk:
                    d = stk[length]
                    total = d.get('flip',0) + d.get('streak',0)
                    if total > 0:
                        flip_pct = d['flip'] / total * 100
                        color = "red" if flip_pct > 50 else "green"
                        st.markdown(f"<p style='color:{color}; margin:2px 0;'>S-{length}: {flip_pct:.0f}% Die</p>", unsafe_allow_html=True)
                        any_streak = True
            if not any_streak:
                st.write("No clear streak patterns yet.")
            st.write("⚡ **ZIGZAG HEALTH**")
            any_zz = False
            for length in range(2,6):
                if length in zz:
                    d = zz[length]
                    total = d.get('break',0) + d.get('cont',0)
                    if total > 0:
                        break_pct = d['break'] / total * 100
                        color = "#00ccff" if break_pct > 50 else "red"
                        st.markdown(f"<p style='color:{color}; margin:2px 0;'>Z-{length}: {break_pct:.0f}% Break</p>", unsafe_allow_html=True)
                        any_zz = True
            if not any_zz:
                st.write("No zigzag patterns yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("💰 Base Bet ($)")
        st.session_state.base_bet = st.number_input("Base Bet", value=st.session_state.base_bet, step=5.0, label_visibility="collapsed")
        st.session_state.use_lstm = st.checkbox("Enable LSTM", value=st.session_state.use_lstm)
        if st.button("🗑️ RESET SHOE"):
            st.session_state.history = []
            st.session_state.recent_results = []
            st.session_state.profit_loss_units = 0
            st.session_state.last_prediction = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== MIDDLE COLUMN (BEAD PLATE + BUTTONS) ====================
with mid_col:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📿 Bead Plate")
        render_bead_plate(st.session_state.history, st.session_state.game)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🎮 INPUT")
        # Custom outcome buttons
        col1, col2, col3 = st.columns(3)
        if st.session_state.game == "Baccarat":
            with col1:
                if st.button("🔴 B", use_container_width=True):
                    record_and_fetch("B")
                    st.rerun()
            with col2:
                if st.button("🔵 P", use_container_width=True):
                    record_and_fetch("P")
                    st.rerun()
            with col3:
                if st.button("🟢 T", use_container_width=True):
                    record_and_fetch("T")
                    st.rerun()
        else:
            with col1:
                if st.button("🔴 Red", use_container_width=True):
                    record_and_fetch("R")
                    st.rerun()
            with col2:
                if st.button("⚫ Black", use_container_width=True):
                    record_and_fetch("B")
                    st.rerun()
            with col3:
                if st.button("🟢 Green", use_container_width=True):
                    record_and_fetch("G")
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        col_undo, col_save = st.columns(2)
        with col_undo:
            if st.button("↩️ UNDO", use_container_width=True):
                if st.session_state.history:
                    st.session_state.history.pop()
                    if st.session_state.recent_results:
                        st.session_state.recent_results.pop()
                    if st.session_state.history:
                        fetch_prediction()
                        fetch_dna()
                    st.rerun()
        with col_save:
            if st.button("💾 SAVE SHOE", use_container_width=True):
                save_shoe()
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== RIGHT COLUMN (LIVE DETAILS) ====================
with right_col:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Live Details")
        with st.expander("💰 P&L (Units)", expanded=True):
            pl_color = "value-positive" if st.session_state.profit_loss_units >= 0 else "value-negative"
            st.markdown(f"<div class='metric-card'><span class='label'>Net Profit/Loss</span><div class='value {pl_color}'>{st.session_state.profit_loss_units:.2f} units</div></div>", unsafe_allow_html=True)
            st.write(f"**Win Streak:** {get_win_streak()}")
            st.write(f"**Loss Streak:** {get_loss_streak()}")
            if st.session_state.recent_results:
                last5 = st.session_state.recent_results[-5:]
                pattern = ''.join(['W' if x==1 else 'L' if x==0 else 'T' for x in last5])
                st.write(f"**Last 5 Pattern:** {pattern}")
            else:
                st.write("**Last 5 Pattern:** (none)")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.last_prediction:
        data = st.session_state.last_prediction
        debug = data.get('debug_info', {})
        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            bet = data.get('bet')
            if bet:
                st.success(f"**{bet}** (Conf: {data.get('confidence',0):.1f}%)")
            else:
                st.warning("**SKIP** (No edge)")
            st.info(f"💰 Kelly (units): {data.get('kelly_amount', 0):.1f} | 🎯 Strategy: {data.get('strategy_name','')}")

            with st.expander("🔍 Analyzer", expanded=True):
                st.write(f"**Market Mode:** {debug.get('market', 'N/A')}")
                st.write(f"**ZigZag Score:** {debug.get('score', 0):.1f}%")
                st.write(f"**DNA Text:** {debug.get('dna_text', 'N/A')}")
                st.write(f"**Global Wins:** {debug.get('g_wins', 0)} | **DNA Wins:** {debug.get('d_wins', 0)}")
                st.write(f"**Logic:** {debug.get('logic', 'N/A')}")

            with st.expander("🧠 AI Models", expanded=True):
                st.write(f"**RF Pattern AI:** {data.get('ai_pred', 'None')} (Conf: {data.get('ai_conf', 0):.1f}%)")
                st.write(f"**LSTM:** {'Enabled' if st.session_state.use_lstm else 'Disabled'}")
            ai_msg = data.get('ai_msg', 'N/A')
            st.info(f"🤖 Q-Learning: {ai_msg}")
            st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📝 Manual Record")
        col_w, col_l, col_tie = st.columns(3)
        with col_w:
            if st.button("✅ Win", use_container_width=True):
                if st.session_state.last_prediction:
                    last = st.session_state.last_prediction
                    kelly_units = last.get('kelly_amount', 0)
                    if kelly_units > 0:
                        if st.session_state.game == "Baccarat":
                            profit_units = kelly_units * 0.95 if last.get('bet') == 'B' else kelly_units
                        else:
                            profit_units = kelly_units
                        st.session_state.profit_loss_units += profit_units
                        st.session_state.recent_results.append(1)
                st.rerun()
        with col_l:
            if st.button("❌ Loss", use_container_width=True):
                if st.session_state.last_prediction:
                    kelly_units = st.session_state.last_prediction.get('kelly_amount', 0)
                    st.session_state.profit_loss_units -= kelly_units
                    st.session_state.recent_results.append(0)
                st.rerun()
        with col_tie:
            if st.button("🔄 Tie", use_container_width=True):
                st.session_state.recent_results.append(2)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
