import streamlit as st
import requests

API_BASE = "https://king63500-unicorn.hf.space"

st.set_page_config(page_title="🦄 Unicorn Pro", layout="wide")
st.title("🦄 Unicorn Pro - AI Casino Assistant")

# -------------------- SESSION STATE --------------------
if 'history' not in st.session_state:
    st.session_state.history = []
if 'profit_loss_units' not in st.session_state:
    st.session_state.profit_loss_units = 0  # in units (base bet)
if 'recent_results' not in st.session_state:
    st.session_state.recent_results = []      # 1 = win, 0 = loss, 2 = tie
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

# -------------------- HELPER FUNCTIONS --------------------
def fetch_prediction():
    payload = {
        "history": st.session_state.history,
        "game": st.session_state.game,
        # Bankroll not needed now – backend uses fixed virtual bankroll
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

def reload_data():
    with st.spinner("Reloading data and retraining AI..."):
        try:
            resp = requests.post(f"{API_BASE}/reload", json={"game": st.session_state.game})
            if resp.status_code == 200:
                fetch_stats()
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
    # Update profit/loss in units based on last prediction
    if st.session_state.last_prediction and st.session_state.last_prediction.get('bet'):
        last = st.session_state.last_prediction
        bet = last.get('bet')
        # Kelly amount in units (backend returns units)
        kelly_units = last.get('kelly_amount', 0)
        if outcome == bet:
            # Win
            if st.session_state.game == "Baccarat" and bet == 'B':
                profit_units = kelly_units * 0.95  # banker commission
            else:
                profit_units = kelly_units
            st.session_state.profit_loss_units += profit_units
            st.session_state.recent_results.append(1)
        elif outcome in ('T', 'G'):
            # Tie or Green – no profit/loss
            st.session_state.recent_results.append(2)
        else:
            # Loss
            st.session_state.profit_loss_units -= kelly_units
            st.session_state.recent_results.append(0)
    else:
        # No previous bet – just record outcome for history, no P&L effect
        pass

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
if st.session_state.db_stats['shoes'] == 0:
    fetch_stats()

# -------------------- LAYOUT --------------------
left_col, mid_col, right_col = st.columns([1.2, 2, 1.2])

# ==================== LEFT COLUMN (SIDEBAR) ====================
with left_col:
    st.header("🎮 Game Selection")
    game = st.selectbox("Game", ["Baccarat", "Roulette"], key="game_selector")
    if game != st.session_state.game:
        st.session_state.game = game
        st.session_state.history = []
        st.session_state.recent_results = []
        st.session_state.profit_loss_units = 0
        st.session_state.last_prediction = None
        fetch_stats()
        st.rerun()

    st.subheader("🧠 Session Memory")
    if len(st.session_state.recent_results) >= 5:
        last5 = st.session_state.recent_results[-5:]
        wins = last5.count(1)
        losses = last5.count(0)
        ties = last5.count(2)
        win_pct = wins / 5 * 100
        if win_pct >= 80:
            status = "🚀 AGGRESSIVE (Hot)"
            color = "green"
        elif win_pct >= 60:
            status = "✅ STABLE (Normal)"
            color = "yellow"
        elif win_pct >= 40:
            status = "⚠️ CHOPPY (Recalib)"
            color = "orange"
        else:
            status = "❄️ OUT OF SYNC"
            color = "red"
        pattern = ''.join(['W' if x==1 else 'L' if x==0 else 'T' for x in last5])
        st.markdown(f"<p style='color:{color}; font-weight:bold;'>{status}</p>", unsafe_allow_html=True)
        st.write(f"Wins: {wins}/5 | Losses: {losses}/5 | Ties: {ties}/5")
        st.write(f"Pattern: {pattern} | Window: {st.session_state.window}")
    else:
        st.write(f"Gathering Data ({len(st.session_state.recent_results)}/5)...")

    st.subheader("📡 Database Uplink")
    if st.session_state.db_stats['status']:
        st.success(f"ONLINE ●\nLoaded Shoes: {st.session_state.db_stats['shoes']}\nTotal Hands: {st.session_state.db_stats['hands']}")
    else:
        st.error("OFFLINE ●")

    if st.button("📥 LOAD & TRAIN AI"):
        reload_data()
        st.rerun()

    st.subheader("🧬 Live Shoe DNA")
    stk = st.session_state.dna_stats.get('streak', {})
    zz = st.session_state.dna_stats.get('zigzag', {})
    if not stk and not zz:
        st.write("Feed more hands...")
    else:
        st.write("🔥 STREAK HEALTH")
        for length in range(1,5):
            if length in stk:
                d = stk[length]
                total = d.get('flip',0) + d.get('streak',0)
                if total > 0:
                    flip_pct = d['flip'] / total * 100
                    color = "red" if flip_pct > 50 else "green"
                    st.markdown(f"<p style='color:{color}'>S-{length}: {flip_pct:.0f}% Die</p>", unsafe_allow_html=True)
        st.write("⚡ ZIGZAG HEALTH")
        for length in range(2,6):
            if length in zz:
                d = zz[length]
                total = d.get('break',0) + d.get('cont',0)
                if total > 0:
                    break_pct = d['break'] / total * 100
                    color = "#00ccff" if break_pct > 50 else "red"
                    st.markdown(f"<p style='color:{color}'>Z-{length}: {break_pct:.0f}% Break</p>", unsafe_allow_html=True)

    st.subheader("💰 Base Bet ($)")
    st.session_state.base_bet = st.number_input("Base Bet", value=st.session_state.base_bet, step=5.0, label_visibility="collapsed")
    st.session_state.use_lstm = st.checkbox("Enable LSTM", value=st.session_state.use_lstm)

    if st.button("🗑️ RESET SHOE"):
        st.session_state.history = []
        st.session_state.recent_results = []
        st.session_state.profit_loss_units = 0
        st.session_state.last_prediction = None
        st.rerun()

# ==================== MIDDLE COLUMN (BEAD PLATE + BUTTONS) ====================
with mid_col:
    st.subheader("📿 Bead Plate")
    history = st.session_state.history
    if history:
        with st.container():
            st.markdown('<div style="height: 350px; overflow-y: scroll; border: 1px solid #444; border-radius: 5px; padding: 5px;">', unsafe_allow_html=True)
            cols_per_row = 10
            table_html = "<table style='border-collapse: collapse;'>"
            for i in range(0, len(history), cols_per_row):
                table_html += "<tr>"
                for j in range(cols_per_row):
                    idx = i + j
                    if idx < len(history):
                        outcome = history[idx]
                        if st.session_state.game == "Roulette" and outcome == 'B':
                            bg = '#333333'
                        elif outcome == 'B':
                            bg = '#ff4d4d'
                        elif outcome == 'P':
                            bg = '#4d79ff'
                        elif outcome in ('R', 'G', 'T'):
                            bg = '#5cd65c' if outcome in ('G','T') else '#ff4d4d'
                        else:
                            bg = '#888'
                        table_html += f"<td style='padding:2px;'><div style='background-color:{bg}; border-radius:50%; width:35px; height:35px; text-align:center; line-height:35px; color:white;'>{outcome}</div></td>"
                    else:
                        table_html += "<td style='padding:2px;'><div style='width:35px; height:35px;'></div></td>"
                table_html += "</tr>"
            table_html += "</table>"
            st.markdown(table_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No hands yet. Click the buttons below to start.")

    st.subheader("🎮 INPUT")
    col1, col2, col3 = st.columns(3)
    if st.session_state.game == "Baccarat":
        btn1_label, btn1_sym = "🔴 B", "B"
        btn2_label, btn2_sym = "🔵 P", "P"
        btn3_label, btn3_sym = "🟢 T", "T"
    else:
        btn1_label, btn1_sym = "🔴 Red", "R"
        btn2_label, btn2_sym = "⚫ Black", "B"
        btn3_label, btn3_sym = "🟢 Green", "G"

    with col1:
        if st.button(btn1_label, use_container_width=True):
            record_and_fetch(btn1_sym)
            st.rerun()
    with col2:
        if st.button(btn2_label, use_container_width=True):
            record_and_fetch(btn2_sym)
            st.rerun()
    with col3:
        if st.button(btn3_label, use_container_width=True):
            record_and_fetch(btn3_sym)
            st.rerun()

    col_undo, col_save = st.columns(2)
    with col_undo:
        if st.button("↩️ UNDO", use_container_width=True):
            if st.session_state.history:
                st.session_state.history.pop()
                if st.session_state.recent_results:
                    st.session_state.recent_results.pop()
                # Undo profit/loss? Not simple, so we'll reset prediction
                if st.session_state.history:
                    fetch_prediction()
                    fetch_dna()
                st.rerun()
    with col_save:
        if st.button("💾 SAVE SHOE", use_container_width=True):
            save_shoe()
            st.rerun()

# ==================== RIGHT COLUMN (LIVE DETAILS) ====================
with right_col:
    st.subheader("📊 Live Details")

    # Show profit/loss in units
    with st.expander("💰 P&L (Units)", expanded=True):
        st.metric("Net Profit/Loss", f"{st.session_state.profit_loss_units:.2f} units")
        st.write(f"**Win Streak:** {get_win_streak()}")
        st.write(f"**Loss Streak:** {get_loss_streak()}")
        if st.session_state.recent_results:
            last5 = st.session_state.recent_results[-5:]
            pattern = ''.join(['W' if x==1 else 'L' if x==0 else 'T' for x in last5])
            st.write(f"**Last 5 Pattern:** {pattern}")
        else:
            st.write("**Last 5 Pattern:** (none)")

    if st.session_state.last_prediction:
        data = st.session_state.last_prediction
        debug = data.get('debug_info', {})
        bet = data.get('bet')
        if bet:
            st.success(f"**{bet}** (Conf: {data.get('confidence',0):.1f}%)")
        else:
            st.warning("**SKIP** (No edge)")
        # Kelly amount in units
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
    else:
        st.info("No prediction yet. Click outcome buttons.")

    st.markdown("---")
    st.subheader("📝 Manual Record (if needed)")
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
