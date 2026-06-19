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
    n_stocks = st.slider("Stocks to scan", min_value=20, max_value=len(TICKERS), value=60, step=10)
with col3:
    filter_choice = st.selectbox("Filter", ["All", "BUY FIRED only", "ALERT + BUY FIRED", "WATCH NOW or higher"])

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
