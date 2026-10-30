#!/usr/bin/env python3
"""AlphaX OTCharts backend. Keep OTCHARTS_API_KEY on the server only."""
import json, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.parse import urlparse, parse_qs, quote

KEY = os.environ.get("OTCHARTS_API_KEY", "").strip()
BASE = "https://otcharts.com"

class Handler(BaseHTTPRequestHandler):
    def send_json(self, code, obj):
        data=json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(data)))
        self.send_header("Cache-Control","no-store")
        self.end_headers()
        self.wfile.write(data)

    def api(self, path):
        if not KEY:
            raise RuntimeError("Server admin has not set OTCHARTS_API_KEY.")
        req=Request(BASE+path,headers={
            "Authorization":"Bearer "+KEY,
            "User-Agent":"AlphaX-OTCharts-Backend/1.0",
            "Accept":"application/json"
        })
        with urlopen(req,timeout=20) as r:
            return json.loads(r.read().decode())

    def do_GET(self):
        parsed=urlparse(self.path)
        if parsed.path == "/":
            try:
                with open("index.html","rb") as f: data=f.read()
                self.send_response(200);self.send_header("Content-Type","text/html; charset=utf-8")
                self.send_header("Content-Length",str(len(data)));self.end_headers();self.wfile.write(data)
            except OSError:self.send_json(404,{"error":"index.html not found"})
            return
        try:
            q=parse_qs(parsed.query)
            if parsed.path == "/api/venues":
                self.send_json(200,self.api("/v1/venues"));return
            if parsed.path == "/api/symbols":
                venue=q.get("venue",["quotex"])[0]
                self.send_json(200,self.api("/v1/symbols?venue="+quote(venue)));return
            if parsed.path == "/api/candles":
                symbol=q.get("symbol",["EURUSD_otc"])[0]
                tf=int(q.get("tf",["60"])[0]);limit=max(1,min(500,int(q.get("limit",["100"])[0])))
                if tf not in (5,15,30,60): raise ValueError("Supported timeframes: 5, 15, 30, 60 seconds.")
                path=f"/v1/candles?venue=quotex&symbol={quote(symbol)}&tf={tf}&limit={limit}"
                self.send_json(200,self.api(path));return
            self.send_json(404,{"error":"Not found"})
        except Exception as e:
            code=getattr(e,"code",None)
            detail=""
            if code:
                try: detail=e.read().decode()
                except Exception: pass
            self.send_json(code if isinstance(code,int) else 500,{"error":str(e),"details":detail[:1000]})
    def log_message(self,fmt,*args): print(fmt%args)

if __name__=="__main__":
    port=int(os.environ.get("PORT","8080"))
    print(f"AlphaX running on http://localhost:{port}")
    ThreadingHTTPServer(("0.0.0.0",port),Handler).serve_forever()
