import streamlit as st
import requests
import threading

API_BASE = "https://king63500-unicorn.hf.space"

# ---- Silent keep-alive ping (prevents HF Space from sleeping) ----
def _background_ping():
    try:
        requests.get(f"{API_BASE}/ping", timeout=5)
    except Exception:
        pass

threading.Thread(target=_background_ping, daemon=True).start()

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
if 'provider' not in st.session_state:
    st.session_state.provider = None
if 'game' not in st.session_state:
    st.session_state.game = None
if 'game_id' not in st.session_state:
    st.session_state.game_id = None
if 'game_cfg' not in st.session_state:
    st.session_state.game_cfg = None   # full cfg dict from /games
if 'games_config' not in st.session_state:
    st.session_state.games_config = {}  # {provider: [{id, name, button_labels, colors}, ...]}
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

# Optimization: Connection Pooling for faster API calls
if 'http_session' not in st.session_state:
    st.session_state.http_session = requests.Session()
if 'model_info' not in st.session_state:
    st.session_state.model_info = None

# -------------------- HELPER FUNCTIONS --------------------

def fetch_games():
    """Call GET /games and populate games_config session state."""
    try:
        resp = st.session_state.http_session.get(f"{API_BASE}/games", timeout=10)
        if resp.status_code == 200:
            st.session_state.games_config = resp.json()
        else:
            st.session_state.games_config = {}
    except Exception as e:
        st.session_state.games_config = {}
        st.error(f"Failed to fetch games: {e}")

def get_current_cfg():
    """Return the current game config dict, or None if not selected."""
    return st.session_state.game_cfg

def test_connection():
    """Test basic connectivity to backend."""
    try:
        r = requests.get(f"{API_BASE}/ping", timeout=5)
        if r.status_code == 200:
            st.success(f"✅ Backend reachable: {r.json()}")
        else:
            st.error(f"❌ Backend returned status {r.status_code}")
    except Exception as e:
        st.error(f"❌ Connection failed: {e}")

def fetch_prediction():
    if not st.session_state.game_id:
        return
    payload = {
        "game_id": st.session_state.game_id,
        "history": st.session_state.history,
        "base_bet": st.session_state.base_bet,
        "use_lstm": st.session_state.use_lstm,
        "recent_results": st.session_state.recent_results
    }
    try:
        resp = st.session_state.http_session.post(f"{API_BASE}/predict", json=payload, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            st.session_state.last_prediction = data
            if 'debug_info' in data and 'window' in data['debug_info']:
                st.session_state.window = data['debug_info']['window']
        else:
            st.warning(f"Prediction API returned {resp.status_code}: {resp.text[:200]}")
            st.session_state.last_prediction = None
    except Exception as e:
        st.error(f"Prediction error: {e}")
        st.session_state.last_prediction = None

def fetch_dna():
    if not st.session_state.game_id:
        return
    payload = {
        "game_id": st.session_state.game_id,
        "history": st.session_state.history
    }
    try:
        resp = st.session_state.http_session.post(f"{API_BASE}/dna", json=payload, timeout=10)
        if resp.status_code == 200:
            st.session_state.dna_stats = resp.json()
        else:
            st.session_state.dna_stats = {"streak": {}, "zigzag": {}}
    except Exception as e:
        st.warning(f"DNA fetch failed: {e}")
        st.session_state.dna_stats = {"streak": {}, "zigzag": {}}

def fetch_stats():
    if not st.session_state.game_id:
        return
    try:
        resp = st.session_state.http_session.get(
            f"{API_BASE}/stats",
            params={"game_id": st.session_state.game_id},
            timeout=10
        )
        if resp.status_code == 200:
            st.session_state.db_stats = resp.json()
        else:
            st.session_state.db_stats = {"shoes": 0, "hands": 0, "status": False}
    except Exception:
        st.session_state.db_stats = {"shoes": 0, "hands": 0, "status": False}

def fetch_health():
    try:
        resp = st.session_state.http_session.get(f"{API_BASE}/health", timeout=10)
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
        resp = st.session_state.http_session.get(f"{API_BASE}/model_info", timeout=10)
        if resp.status_code == 200:
            st.session_state.model_info = resp.json()
        else:
            st.session_state.model_info = None
    except Exception:
        st.session_state.model_info = None

def reload_data():
    with st.spinner("Reloading data and retraining AI..."):
        try:
            resp = st.session_state.http_session.post(
                f"{API_BASE}/train",
                json={"game_id": st.session_state.game_id},
                timeout=120
            )
            if resp.status_code == 200:
                fetch_stats()
                fetch_model_info()
                st.success("Data reloaded and AI retrained!")
            else:
                st.error(f"Reload failed: {resp.status_code} - {resp.text[:200]}")
        except Exception as e:
            st.error(f"Reload error: {e}")

def save_shoe():
    if not st.session_state.history:
        st.warning("No hands to save.")
        return
    payload = {
        "game_id": st.session_state.game_id,
        "history": st.session_state.history
    }
    try:
        resp = st.session_state.http_session.post(f"{API_BASE}/save", json=payload, timeout=30)
        if resp.status_code == 200 and resp.json().get("success"):
            st.success(f"Shoe saved! New shoe ID: {resp.json().get('new_shoe_id', '?')}")
            fetch_stats()
        else:
            st.error(f"Save failed: {resp.text[:200]}")
    except Exception as e:
        st.error(f"Save error: {e}")

def render_bead_plate(history, cfg):
    """Render bead plate using colors from game config."""
    if not history:
        st.info("No hands yet. Click the buttons below to start.")
        return
    colors = cfg.get('colors', {}) if cfg else {}
    beads = []
    for outcome in history:
        color = colors.get(outcome, '#888888')
        beads.append(
            f"<div class='bead' style='background: radial-gradient(circle at 30% 30%, {color}cc, {color});' "
            f"title='{outcome}'>{outcome}</div>"
        )
    html = f"""
    <div class='bead-plate-scroll'>
        <div class='bead-plate'>
            {''.join(beads)}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def record_and_fetch(outcome):
    """Record outcome, update P&L, fetch new prediction."""
    last = st.session_state.last_prediction
    if last and last.get('bet'):
        bet = last['bet']
        kelly = last.get('kelly_amount', 0)
        if outcome == bet:
            # Win — Banker commission only for Baccarat-like games
            cfg = get_current_cfg()
            allowed = cfg.get('allowed_chars', []) if cfg else []
            if bet == allowed[0] if allowed else False:  # First symbol = Banker equivalent
                profit = kelly * 0.95
            else:
                profit = kelly
            st.session_state.profit_loss_units += profit
            st.session_state.recent_results.append(1)
        else:
            # Check for push/tie: if outcome is the 3rd symbol and game has 3 symbols
            cfg = get_current_cfg()
            allowed = cfg.get('allowed_chars', []) if cfg else []
            if len(allowed) >= 3 and outcome == allowed[2]:
                # 3rd symbol = Tie/Push in baccarat, Green in roulette → push (no P&L)
                st.session_state.recent_results.append(2)
            else:
                st.session_state.profit_loss_units -= kelly
                st.session_state.recent_results.append(0)
    else:
        pass  # No prediction → just record outcome

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

def reset_shoe_state():
    """Reset per-shoe session state when game changes."""
    st.session_state.history = []
    st.session_state.recent_results = []
    st.session_state.profit_loss_units = 0
    st.session_state.last_prediction = None
    st.session_state.dna_stats = {"streak": {}, "zigzag": {}}

# -------------------- INITIAL FETCH --------------------
fetch_health()
if not st.session_state.games_config:
    fetch_games()
if st.session_state.db_stats['shoes'] == 0:
    fetch_stats()
if st.session_state.model_info is None:
    fetch_model_info()

# Set a default provider/game if not set yet and games_config is available
if st.session_state.games_config and st.session_state.provider is None:
    first_provider = list(st.session_state.games_config.keys())[0]
    first_game = st.session_state.games_config[first_provider][0]
    st.session_state.provider = first_provider
    st.session_state.game = first_game['name']
    st.session_state.game_id = first_game['id']
    st.session_state.game_cfg = first_game
    fetch_stats()

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

        games_config = st.session_state.games_config

        if not games_config:
            st.warning("⚠️ Could not load games from backend. Click to retry.")
            if st.button("🔄 Retry Loading Games"):
                fetch_games()
                st.rerun()
        else:
            # Provider selector
            providers = list(games_config.keys())
            current_provider = st.session_state.provider if st.session_state.provider in providers else providers[0]
            selected_provider = st.selectbox(
                "Provider",
                providers,
                index=providers.index(current_provider),
                key="provider_selector"
            )

            # Game selector filtered by provider
            provider_games = games_config.get(selected_provider, [])
            game_names = [g['name'] for g in provider_games]
            current_game_name = st.session_state.game if (st.session_state.game in game_names and st.session_state.provider == selected_provider) else game_names[0]
            selected_game_name = st.selectbox(
                "Game",
                game_names,
                index=game_names.index(current_game_name) if current_game_name in game_names else 0,
                key="game_selector"
            )

            # Find the full game cfg for the selected game
            selected_game_obj = next((g for g in provider_games if g['name'] == selected_game_name), None)
            selected_game_id = selected_game_obj['id'] if selected_game_obj else None

            # Detect change and reset
            if selected_provider != st.session_state.provider or selected_game_name != st.session_state.game:
                st.session_state.provider = selected_provider
                st.session_state.game = selected_game_name
                st.session_state.game_id = selected_game_id
                st.session_state.game_cfg = selected_game_obj
                reset_shoe_state()
                fetch_stats()
                fetch_model_info()
                st.rerun()

        st.markdown(f"**Provider:** {st.session_state.provider or '—'}  |  **Game:** {st.session_state.game or '—'}")
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
        games_mi = mi.get("games", {}) if isinstance(mi, dict) else {}
        # Use game_id for lookup (e.g. "pragmatic_baccarat")
        current_game_id = st.session_state.game_id or ""
        g = games_mi.get(current_game_id, {}) if isinstance(games_mi, dict) else {}
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
            st.write("Model info not available.")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🧬 Live Shoe DNA")
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
            for length in range(1, 5):
                if length in stk:
                    d = stk[length]
                    total = d.get('flip', 0) + d.get('streak', 0)
                    if total > 0:
                        flip_pct = d['flip'] / total * 100
                        color = "red" if flip_pct > 50 else "green"
                        st.markdown(f"<p style='color:{color}; margin:2px 0;'>S-{length}: {flip_pct:.0f}% Die</p>", unsafe_allow_html=True)
                        any_streak = True
            if not any_streak:
                st.write("No clear streak patterns yet.")
            st.write("⚡ **ZIGZAG HEALTH**")
            any_zz = False
            for length in range(2, 6):
                if length in zz:
                    d = zz[length]
                    total = d.get('break', 0) + d.get('cont', 0)
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
            reset_shoe_state()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🔌 Connection Test")
        if st.button("Test Backend Connection"):
            test_connection()
        if st.button("🔄 Refresh Games List"):
            fetch_games()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== MIDDLE COLUMN (BEAD PLATE + BUTTONS) ====================
with mid_col:
    cfg = get_current_cfg()

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📿 Bead Plate")
        render_bead_plate(st.session_state.history, cfg)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🎮 INPUT")

        if cfg is None:
            st.info("Select a provider and game to start.")
        else:
            # Dynamic outcome buttons based on game config
            button_labels = cfg.get('button_labels', [])
            allowed_chars = cfg.get('allowed_chars', [])
            num_buttons = len(button_labels)

            if num_buttons == 0:
                st.warning("No button configuration found for this game.")
            else:
                # Render in rows of up to 3 buttons
                for row_start in range(0, num_buttons, 3):
                    row_labels = button_labels[row_start:row_start + 3]
                    row_chars = allowed_chars[row_start:row_start + 3]
                    cols = st.columns(len(row_labels))
                    for col, label, char in zip(cols, row_labels, row_chars):
                        with col:
                            if st.button(label, use_container_width=True, key=f"btn_{char}"):
                                record_and_fetch(char)
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
                lstm_pred = data.get('lstm_pred')
                lstm_conf = data.get('lstm_conf', 0.0)
                if lstm_pred is not None:
                    st.write(f"**LSTM:** {lstm_pred} (Conf: {lstm_conf:.1f}%)")
                else:
                    st.write(f"**LSTM:** {'Warming up...' if st.session_state.use_lstm else 'Disabled'}")
            ai_msg = data.get('ai_msg', 'N/A')
            st.info(f"🤖 Q-Learning: {ai_msg}")
            st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📝 Manual Record")
        cfg = get_current_cfg()
        allowed = cfg.get('allowed_chars', []) if cfg else []
        col_w, col_l, col_tie = st.columns(3)
        with col_w:
            if st.button("✅ Win", use_container_width=True):
                if st.session_state.last_prediction:
                    last = st.session_state.last_prediction
                    kelly_units = last.get('kelly_amount', 0)
                    if kelly_units > 0:
                        bet = last.get('bet')
                        # Banker commission for first-symbol bets
                        if allowed and bet == allowed[0]:
                            profit = kelly_units * 0.95
                        else:
                            profit = kelly_units
                        st.session_state.profit_loss_units += profit
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
            # Show "Push/Tie" button if game has a 3rd symbol (Tie/Green/etc.)
            if len(allowed) >= 3:
                if st.button("🔄 Push/Tie", use_container_width=True):
                    st.session_state.recent_results.append(2)
                    st.rerun()
            else:
                st.empty()
        st.markdown("</div>", unsafe_allow_html=True)
