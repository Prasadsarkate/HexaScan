#!/usr/bin/env python3
"""
Simple Flask dashboard to view results.json produced by skan.py
Run:
  export FLASK_ENV=development
  python3 dashboard.py
Open http://127.0.0.1:5000
"""
from flask import Flask, render_template_string, jsonify, request
import json, os, time

RESULTS_FILE = "results.json"
app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Skan Dashboard</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mini.css/3.0.1/mini-default.min.css">
<style>pre{white-space:pre-wrap;word-wrap:break-word}</style>
</head>
<body>
<nav><a href="/">Home</a> <a href="/api/results">API (JSON)</a></nav>
<header><h1>Skan Dashboard</h1><p>Auto-refresh every 6s</p></header>
<main>
<button onclick="location.reload()">Refresh Now</button>
<button onclick="clearResults()">Clear results.json</button>
<table>
<thead><tr><th>Target</th><th>IP</th><th>Port</th><th>Proto</th><th>Banner (preview)</th><th>Plugins</th></tr></thead>
<tbody id="rows"></tbody>
</table>
<script>
async function load(){
  const res = await fetch('/api/results');
  const json = await res.json();
  const tbody = document.getElementById('rows');
  tbody.innerHTML = '';
  for(const r of json){
    const plugins = (r.plugins || []).map(p => JSON.stringify(p)).join('<br>');
    const banner = (r.banner||'').slice(0,300).replace(/</g,'&lt;');
    tbody.innerHTML += `<tr><td>${r.target||''}</td><td>${r.ip||''}</td><td>${r.port}</td><td>${r.proto||''}</td><td><pre>${banner}</pre></td><td>${plugins}</td></tr>`;
  }
}
function clearResults(){
  fetch('/api/clear',{method:'POST'}).then(()=>load());
}
load();
setInterval(load, 6000);
</script>
</main>
<footer><p>Generated: {{ ts }}</p></footer>
</body>
</html>
"""

@app.route("/")
def index():
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(TEMPLATE, ts=ts)

@app.route("/api/results")
def api_results():
    if not os.path.exists(RESULTS_FILE):
        return jsonify([])
    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return jsonify(data)
    except Exception:
        return jsonify([])

@app.route("/api/clear", methods=["POST"])
def api_clear():
    try:
        if os.path.exists(RESULTS_FILE):
            os.remove(RESULTS_FILE)
        return ("", 204)
    except Exception:
        return ("", 500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
