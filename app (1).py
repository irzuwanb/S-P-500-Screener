import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="S&P 500 Buy Signal Dashboard", layout="wide")

TICKERS = ["NVDA","GOOGL","AAPL","MSFT","AMZN","AVGO","META","TSLA","WMT","BRK-B","LLY","JPM","MU","AMD","XOM","V","JNJ","INTC","ORCL","COST","CSCO","MA","CAT","CVX","NFLX","ABBV","BAC","UNH","KO","LRCX","PG","AMAT","PLTR","MS","HD","PM","GE","GS","MRK","TXN","GEV","RTX","LIN","KLAC","WFC","QCOM","AXP","IBM","C","TMUS","ADI","PEP","PANW","MCD","VZ","NEE","DIS","ANET","BLK","AMGN","BA","T","TJX","APP","TMO","UNP","GILD","SCHW","CRWD","ISRG","DELL","ABT","UBER","DE","COP","WELL","APH","ETN","CRM","PFE","BX","HON","PLD","VRT","CB","SPGI","MO","CVS","LOW","LMT","SBUX","BKNG","SYK","PGR","NEM","BMY","COF","DHR","INTU","VRTX","CME","ACN","PWR","PH","NOW","SO","EQIX","ADBE","HWM","TT","MDT","DUK","SNPS","CDNS","WMB","MAR","CEG","HCA","BK","CMI","MCK","FTNT","GD","WM","ADP","CMCSA","ICE","FDX","FCX","MNST","KKR","CSX","PNC","ELV","SLB","JCI","BSX","USB","AMT","UPS","ABNB","MMM","MDLZ","NOC","MCO","APO","VLO","SPG","EOG","ORLY","CI","MPC","KMI","DDOG","SHW","CIEN","EMR","NXPI","MPWR","CVNA","HLT","PSX","CL","NSC","ITW","COHR","DASH","ECL","CTAS","AON","HOOD","AEP","CRH","MSI","ROST","WBD","RCL","DLR","TDG","RSG","GM","BKR","APD","FIX","TRV","REGN","LITE","NKE","AFL","GWW","D","OXY","URI","OKE","SRE","TRGP","PCAR","TFC","TEL","KEYS","LHX","FANG","O","DVN","ALL","TGT","AZO","CTVA","CARR","AJG","MET","NDAQ","PSA","F","AME","NUE","ADSK","COR","EBAY","FAST","EA","TER","MCHP","ETR","COIN","XEL","ROK","EW","CAH","VST","DAL","EXC","TTWO","WAB","HPE","GRMN","FITB","CMG","VTR","IDXX","ON","STT","MSCI","ODFL","AMP","XYZ","YUM","KR","AIG","ARES","KDP","ED","CCI","BDX","PYPL","ADM","DHI","EME","LYV","HSY","IBKR","CBOE","PEG","CBRE","HIG","TKO","IRM","HUM","EQT","PRU","HAL","JBL","WEC","SYY","PCG","VMC","CCL","PAYX","ROP","MLM","ACGL","LVS","KVUE","STLD","WAT","ZTS","CPRT","AXON","WDAY","KMB","A","CASY","HBAN","VICI","EXR","NTRS","MTB","RJF","UAL","ATO","AEE","RMD","DTE","EL","IQV","CNC","TDY","DOV","BIIB","GEHC","VRSN","DOW","KHC","FOXA","FICO","IR","OTIS","CNP","WRB","TPL","TPR","NRG","EIX","ROL","PPL","FOX","CINF","AVB","CFG","EXPE","XYL","FE","ES","STZ","EQR","DXCM","FSLR","HUBB","JBHT","AWK","CTSH","WTW","BG","LYB","SYF","NTAP","EXE","TSN","DG","PPG","RF","CHD","KEY","CPAY","VRSK","FIS","NI","CMS","L","DRI","PFG","TROW","AKAM","MTD","SBAC","WST","FFIV","VLTO","PHM","DGX","LH","ULTA","STE","OMC","ALB","LEN","EXPD","CHRW","DD","WSM","BRO","RL","SW","CHTR","EFX","CF","VTRS","HPQ","MRNA","INCY","EVRG","SNA","IFF","GPN","LUV","PKG","LNT","SMCI","ESS","FTV","GIS","DLTR","LII","BR","AMCR","INVH","PTC","TSCO","BEN","WY","ZBH","IP","KIM","TXT","LDOS","IEX","NDSN","NVR","MAA","HST","NWS","GNRC","BALL","GEN","REG","NWSA","APA","EG","LULU","DOC","CSGP","TYL","DECK","J","UDR","CDW","HAS","SOLV","MAS","HII","TRMB","GPC","DVA","AIZ","MKC","ZBRA","GL","BBY","IVZ","GDDY","PNW","BF-B","AVY","COO","PNR","SWK","ERIE","ALGN","CLX","APTV","HRL","SJM","ALLE","CPT","BXP","RVTY","SWKS","PODD","TTD","IT","AES","UHS","DPZ","FRT","JKHY","WYNN","MGM","BAX","HSIC","FDS","ARE","TAP","AOS","BLDR","CRL","NCLH","TECH","MOS","POOL","CAG","CPB","EPAM"]


def calc_indicators(df):
    df['ema100'] = df['Close'].ewm(span=100, adjust=False).mean()
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    df['basis'] = df['Close'].rolling(20).mean()
    df['std'] = df['Close'].rolling(20).std()
    df['upper'] = df['basis'] + 2.5 * df['std']
    df['lower'] = df['basis'] - 2.5 * df['std']
    df['bb_pct'] = (df['Close'] - df['lower']) / (df['upper'] - df['lower'])
    hl = df['High'] - df['Low']
    hc = (df['High'] - df['Close'].shift(1)).abs()
    lc = (df['Low'] - df['Close'].shift(1)).abs()
    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    df['atr'] = tr.rolling(14).mean()
    return df


def get_score(rsi_v, bb_pct, ema_diff):
    rsi_score = 0
    if rsi_v <= 30:
        rsi_score = 100
    elif rsi_v <= 35:
        rsi_score = 80
    elif rsi_v <= 40:
        rsi_score = 55
    elif rsi_v <= 45:
        rsi_score = 30
    elif rsi_v <= 50:
        rsi_score = 10

    bb_score = 0
    if bb_pct <= 0:
        bb_score = 100
    elif bb_pct <= 0.08:
        bb_score = 85
    elif bb_pct <= 0.15:
        bb_score = 60
    elif bb_pct <= 0.25:
        bb_score = 35
    elif bb_pct <= 0.35:
        bb_score = 15

    ema_score = 0
    if ema_diff >= 0:
        ema_score = 100
    elif ema_diff >= -0.02:
        ema_score = 60
    elif ema_diff >= -0.05:
        ema_score = 30

    final = rsi_score * 0.4 + bb_score * 0.4 + ema_score * 0.2
    return round(final)


@st.cache_data(ttl=900, show_spinner=False)
def score_stock(ticker):
    try:
        df = yf.download(ticker, period="60d", interval="1h", progress=False, auto_adjust=True)
    except Exception:
        return None

    if df is None or len(df) < 105:
        return None
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = calc_indicators(df)
    df_clean = df.dropna()
    if len(df_clean) == 0:
        return None

    last = df_clean.iloc[-1]
    close = float(last['Close'])
    rsi_v = float(last['rsi'])
    ema_v = float(last['ema100'])
    bb_pct = float(last['bb_pct'])
    lower_v = float(last['lower'])
    atr_v = float(last['atr'])

    recent_buy = None
    scan_window = df_clean.tail(72)
    n_window = len(scan_window)
    for idx in range(n_window):
        row = scan_window.iloc[idx]
        is_buy = row['Close'] < row['lower'] and row['rsi'] < 30 and row['Close'] < row['ema100']
        if is_buy:
            hrs_ago = n_window - 1 - idx
            recent_buy = {
                'hours_ago': hrs_ago,
                'price': float(row['Close']),
                'tp1': float(row['Close'] + row['atr'] * 2),
                'tp2': float(row['Close'] + row['atr'] * 4),
                'exit': float(row['Close'] + row['atr'] * 6),
            }

    ema_diff = (ema_v - close) / ema_v
    score = get_score(rsi_v, bb_pct, ema_diff)

    status = "NEUTRAL"
    if recent_buy:
        status = "BUY FIRED"
    elif score >= 75:
        status = "ALERT"
    elif score >= 50:
        status = "WATCH NOW"
    elif score >= 25:
        status = "ON RADAR"

    result = {
        'ticker': ticker, 'score': score, 'status': status, 'price': close,
        'rsi': rsi_v, 'ema100': ema_v, 'lower_bb': lower_v,
        'bb_pct': bb_pct * 100, 'atr': atr_v,
        'below_ema': close < ema_v, 'recent_buy': recent_buy,
    }
    return result


STATUS_COLOR = {"BUY FIRED": "#22c55e", "ALERT": "#ef4444", "WATCH NOW": "#f59e0b", "ON RADAR": "#3b82f6", "NEUTRAL": "#64748b"}
STATUS_ICON = {"BUY FIRED": "🟢", "ALERT": "🔴", "WATCH NOW": "🟡", "ON RADAR": "🔵", "NEUTRAL": "⚪"}


def render_card(r):
    color = STATUS_COLOR[r['status']]
    icon = STATUS_ICON[r['status']]

    buy_html = ""
    if r['recent_buy'] is not None:
        b = r['recent_buy']
        when = "CURRENT CANDLE" if b['hours_ago'] == 0 else str(b['hours_ago']) + "H AGO"
        buy_html = "<div style='margin-top:8px;padding:10px;background:#052e16;border-radius:8px;border:1px solid #166534;'>"
        buy_html += "<div style='font-size:11px;color:#22c55e;font-weight:700;margin-bottom:6px;'>"
        buy_html += "BUY SIGNAL - " + when + " @ $" + format(b['price'], '.2f') + "</div>"
        buy_html += "<div style='font-size:11px;color:#cbd5e1;'>"
        buy_html += "TP1: $" + format(b['tp1'], '.2f') + "  |  TP2: $" + format(b['tp2'], '.2f') + "  |  EXIT: $" + format(b['exit'], '.2f')
        buy_html += "</div></div>"

    needs_html = ""
    if r['recent_buy'] is None and r['score'] >= 25:
        needs = []
        if r['rsi'] > 30:
            needs.append("RSI -" + format(r['rsi'] - 30, '.1f') + "pts")
        if r['bb_pct'] > 0:
            gap_pct = (r['price'] - r['lower_bb']) / r['price'] * 100
            needs.append("price -" + format(gap_pct, '.1f') + "% to BB")
        if not r['below_ema']:
            needs.append("break below EMA100")
        if len(needs) > 0:
            needs_html = "<div style='margin-top:6px;font-size:10px;color:#64748b;'>Needs: " + " | ".join(needs) + "</div>"

    rsi_color = "#f87171" if r['rsi'] < 35 else "#64748b"
    bb_color = "#f87171" if r['bb_pct'] < 15 else "#64748b"

    card = "<div style='background:#0a0e1a;border:1px solid " + color + "30;border-left:3px solid " + color + ";border-radius:10px;padding:14px 16px;margin-bottom:10px;font-family:monospace;'>"
    card += "<div style='display:flex;justify-content:space-between;'>"
    card += "<div><span style='font-size:16px;font-weight:800;color:#f1f5f9;'>" + r['ticker'] + "</span>"
    card += "<span style='font-size:10px;font-weight:700;color:" + color + ";margin-left:10px;'>" + icon + " " + r['status'] + "</span></div>"
    card += "<div style='text-align:right;'><div style='font-size:16px;font-weight:700;color:#f1f5f9;'>$" + format(r['price'], '.2f') + "</div>"
    card += "<div style='font-size:18px;font-weight:800;color:" + color + ";'>" + str(r['score']) + "</div></div></div>"
    card += "<div style='display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;'>"
    card += "<div style='background:#0f172a;border-radius:6px;padding:6px 10px;'><div style='font-size:8px;color:#334155;'>RSI</div>"
    card += "<div style='font-size:12px;font-weight:700;color:" + rsi_color + ";'>" + format(r['rsi'], '.1f') + "</div></div>"
    card += "<div style='background:#0f172a;border-radius:6px;padding:6px 10px;'><div style='font-size:8px;color:#334155;'>BB %B</div>"
    card += "<div style='font-size:12px;font-weight:700;color:" + bb_color + ";'>" + format(r['bb_pct'], '.0f') + "%</div></div>"
    card += "<div style='background:#0f172a;border-radius:6px;padding:6px 10px;'><div style='font-size:8px;color:#334155;'>EMA100</div>"
    card += "<div style='font-size:12px;font-weight:700;color:#64748b;'>$" + format(r['ema100'], '.2f') + "</div></div>"
    card += "<div style='background:#0f172a;border-radius:6px;padding:6px 10px;'><div style='font-size:8px;color:#334155;'>ATR</div>"
    card += "<div style='font-size:12px;font-weight:700;color:#64748b;'>$" + format(r['atr'], '.2f') + "</div></div>"
    card += "</div>" + buy_html + needs_html + "</div>"
    return card


# ---------------- Page layout ----------------
st.markdown(
    "<div style='font-family:monospace;'>"
    "<div style='font-size:11px;color:#475569;letter-spacing:2px;'>S&P 500 - BUY SIGNAL DASHBOARD</div>"
    "<div style='font-size:22px;font-weight:800;'>Strategy: BB(20,2.5) + RSI(14)&lt;30 + Close&lt;EMA(100)</div>"
    "<div style='font-size:12px;color:#94a3b8;'>Scans last 72 hourly candles. Shows most recent buy signal per stock. Data: Yahoo Finance (delayed ~15-20min)</div>"
    "</div><br>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 2, 2])
with col1:
    scan_clicked = st.button("SCAN NOW", type="primary", use_container_width=True)
with col2:
    n_stocks = st.slider("Stocks to scan", min_value=20, max_value=len(TICKERS), value=100, step=10)
with col3:
    filter_choice = st.selectbox("Filter", ["All", "BUY FIRED only", "ALERT + BUY FIRED", "WATCH NOW or higher"])

st.caption("Total tickers loaded: " + str(len(TICKERS)) + " (full S&P 500 list, minus a few dual-class/edge-case tickers)")

if "results" not in st.session_state:
    st.session_state.results = []
    st.session_state.last_scan = None

if scan_clicked:
    subset = TICKERS[:n_stocks]
    results = []
    progress_bar = st.progress(0, text="Starting scan...")

    for i, t in enumerate(subset):
        r = score_stock(t)
        if r is not None:
            results.append(r)
        progress_bar.progress((i + 1) / len(subset), text="Scanning " + t + "...")

    progress_bar.empty()
    order = {"BUY FIRED": 0, "ALERT": 1, "WATCH NOW": 2, "ON RADAR": 3, "NEUTRAL": 4}
    results.sort(key=lambda x: (order[x['status']], -x['score']))
    st.session_state.results = results
    st.session_state.last_scan = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

results = st.session_state.results

if len(results) > 0:
    f = filter_choice
    if f == "BUY FIRED only":
        shown = [r for r in results if r['status'] == "BUY FIRED"]
    elif f == "ALERT + BUY FIRED":
        shown = [r for r in results if r['status'] in ("BUY FIRED", "ALERT")]
    elif f == "WATCH NOW or higher":
        shown = [r for r in results if r['status'] in ("BUY FIRED", "ALERT", "WATCH NOW")]
    else:
        shown = results

    buy_n = len([r for r in results if r['status'] == "BUY FIRED"])
    alert_n = len([r for r in results if r['status'] == "ALERT"])
    watch_n = len([r for r in results if r['status'] == "WATCH NOW"])

    summary = "<div style='font-family:monospace;background:#0d1117;padding:14px 18px;border-radius:10px;margin-bottom:14px;color:white;'>"
    summary += "<div style='color:#94a3b8;font-size:12px;margin-bottom:6px;'>Last scan: " + str(st.session_state.last_scan) + " | " + str(len(results)) + " stocks loaded</div>"
    summary += "<div style='display:flex;gap:16px;'>"
    summary += "<span style='color:#22c55e;font-weight:700;'>BUY FIRED: " + str(buy_n) + "</span>"
    summary += "<span style='color:#ef4444;font-weight:700;'>ALERT: " + str(alert_n) + "</span>"
    summary += "<span style='color:#f59e0b;font-weight:700;'>WATCH NOW: " + str(watch_n) + "</span>"
    summary += "</div></div>"
    st.markdown(summary, unsafe_allow_html=True)

    if len(shown) == 0:
        st.markdown("<div style='color:#64748b;font-family:monospace;padding:20px;'>No stocks match this filter right now.</div>", unsafe_allow_html=True)
    else:
        for r in shown:
            st.markdown(render_card(r), unsafe_allow_html=True)
else:
    st.markdown(
        "<div style='color:#64748b;font-family:monospace;padding:30px;text-align:center;'>"
        "Press SCAN NOW to load the dashboard.</div>",
        unsafe_allow_html=True
    )

st.markdown(
    "<div style='margin-top:30px;font-size:11px;color:#475569;text-align:center;'>"
    "For educational purposes only. Not financial advice. Verify all signals before trading.</div>",
    unsafe_allow_html=True
)
