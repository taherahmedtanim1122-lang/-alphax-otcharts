# AlphaX OTCharts (Quotex)

## Important
- This is a backend + web app package, not a single offline HTML file.
- Never put the OTCharts key in `index.html`, JavaScript, screenshots, or chat.
- The free OTCharts plan has 200 requests in its first month, five allowed instruments, and no live streaming.
- USD/BRL OTC is not among the known five free Quotex instruments. The app will show the API's refusal if your plan does not open it.
- The API is read-only; it does not place trades.
- Signals are simple EMA/RSI rules, not machine-learning predictions and not guaranteed.

## Run on a computer/server
1. Install Python 3.10+.
2. Put `index.html` and `server.py` in the same folder.
3. Set the secret environment variable:
   - Linux/macOS: `export OTCHARTS_API_KEY='your_key_here'`
   - Windows PowerShell: `$env:OTCHARTS_API_KEY='your_key_here'`
4. Run: `python server.py`
5. Open `http://localhost:8080`.

For public hosting, deploy this folder to a Python-capable host and set `OTCHARTS_API_KEY` in the host's secret/environment-variable settings. Do not commit the key to GitHub.

## Current implementation
- Quotex book, candle history endpoint, timeframe values 5/15/30/60 seconds.
- One manual analysis request at a time; no polling and no live stream.
- Free plan quota is limited. Avoid repeatedly pressing Analyze.
- The frontend currently offers common OTC symbols as shortcuts; the API is the authority on which are open on your plan.
