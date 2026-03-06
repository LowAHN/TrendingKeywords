#!/usr/bin/env python3
"""
실시간 인기 키워드 수집기 (Web GUI)
브라우저에서 http://localhost:8877 접속
"""

from flask import Flask, render_template_string, jsonify, request
import requests as req
import feedparser
import json
import urllib.parse
from datetime import datetime
from pathlib import Path
import webbrowser
import threading

app = Flask(__name__)
OUTPUT_DIR = Path(__file__).parent / "results"
OUTPUT_DIR.mkdir(exist_ok=True)

# ─── 수집 함수 ───

def get_google_trending_kr():
    keywords = []
    try:
        url = "https://trends.google.co.kr/trending/rss?geo=KR"
        feed = feedparser.parse(url)
        for entry in feed.entries[:20]:
            title = entry.get("title", "").strip()
            traffic = entry.get("ht_approx_traffic", "")
            if title:
                keywords.append({"keyword": title, "traffic": traffic})
    except Exception as e:
        keywords.append({"keyword": f"[오류] {e}", "traffic": ""})
    return keywords


def get_google_suggest(seed_keywords):
    results = {}
    for seed in seed_keywords:
        try:
            encoded = urllib.parse.quote(seed)
            url = f"https://suggestqueries.google.com/complete/search?client=firefox&hl=ko&q={encoded}"
            resp = req.get(url, timeout=5)
            if resp.status_code == 200:
                results[seed] = resp.json()[1][:10]
        except Exception:
            results[seed] = []
    return results


def get_naver_suggest(seed_keywords):
    results = {}
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    for seed in seed_keywords:
        try:
            encoded = urllib.parse.quote(seed)
            url = f"https://ac.search.naver.com/nx/ac?q={encoded}&q_enc=UTF-8&st=100&frm=nv&r_format=json&r_enc=UTF-8&r_unicode=0&t_koreng=1"
            resp = req.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                suggestions = []
                for item_group in data.get("items", [[]]):
                    for item in item_group:
                        if isinstance(item, list) and item:
                            suggestions.append(item[0])
                results[seed] = suggestions[:10]
        except Exception:
            results[seed] = []
    return results


# ─── API ───

@app.route("/api/search", methods=["POST"])
def api_search():
    data = request.get_json()
    seeds = data.get("seeds", ["오늘", "추천", "방법", "비교", "후기", "순위"])

    google_trends = get_google_trending_kr()
    google_suggest = get_google_suggest(seeds)
    naver_suggest = get_naver_suggest(seeds)

    all_keywords = []
    for item in google_trends:
        all_keywords.append(item["keyword"])
    for suggestions in google_suggest.values():
        all_keywords.extend(suggestions)
    for suggestions in naver_suggest.values():
        all_keywords.extend(suggestions)
    unique = list(dict.fromkeys(all_keywords))

    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "google_trends": google_trends,
        "google_suggest": google_suggest,
        "naver_suggest": naver_suggest,
        "all_unique_keywords": unique,
    }

    # 자동 저장
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = OUTPUT_DIR / f"trending_{ts}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    result["saved_to"] = str(filepath)

    return jsonify(result)


# ─── 웹 페이지 ───

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Trending Keywords</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #0f0f1a;
    color: #e0e0e0;
    min-height: 100vh;
  }
  .container { max-width: 960px; margin: 0 auto; padding: 20px; }

  h1 {
    font-size: 28px;
    background: linear-gradient(135deg, #6ee7b7, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 20px;
  }

  .input-row {
    display: flex; gap: 10px; margin-bottom: 15px;
  }
  .input-row input {
    flex: 1; padding: 12px 16px;
    background: #1a1a2e; border: 1px solid #333;
    border-radius: 10px; color: #e0e0e0; font-size: 15px;
    outline: none; transition: border 0.2s;
  }
  .input-row input:focus { border-color: #3b82f6; }

  .btn {
    padding: 12px 24px; border: none; border-radius: 10px;
    font-size: 14px; font-weight: 600; cursor: pointer;
    transition: all 0.2s;
  }
  .btn-primary { background: #3b82f6; color: white; }
  .btn-primary:hover { background: #2563eb; transform: translateY(-1px); }
  .btn-green { background: #10b981; color: white; }
  .btn-green:hover { background: #059669; }
  .btn-purple { background: #8b5cf6; color: white; }
  .btn-purple:hover { background: #7c3aed; }
  .btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

  .btn-row { display: flex; gap: 8px; margin-bottom: 15px; flex-wrap: wrap; }

  .status {
    padding: 8px 14px; background: #1a1a2e;
    border-radius: 8px; font-size: 13px; color: #6ee7b7;
    margin-bottom: 15px;
  }

  .tabs {
    display: flex; gap: 0; margin-bottom: 0;
    border-bottom: 2px solid #1a1a2e;
  }
  .tab {
    padding: 10px 20px; cursor: pointer;
    background: #1a1a2e; color: #888;
    border: none; font-size: 14px; font-weight: 500;
    border-radius: 10px 10px 0 0;
    transition: all 0.2s;
  }
  .tab.active { background: #1e1e32; color: #6ee7b7; }
  .tab:hover { color: #e0e0e0; }

  .panel {
    display: none; background: #1e1e32;
    border-radius: 0 10px 10px 10px; padding: 20px;
    min-height: 400px; max-height: 500px; overflow-y: auto;
  }
  .panel.active { display: block; }

  .keyword-item {
    display: flex; align-items: center; padding: 8px 0;
    border-bottom: 1px solid #252540;
  }
  .keyword-item:last-child { border-bottom: none; }
  .keyword-num { color: #555; width: 35px; font-size: 13px; text-align: right; margin-right: 12px; }
  .keyword-text { color: #6ee7b7; font-weight: 500; flex: 1; }
  .keyword-traffic {
    color: #f59e0b; font-size: 12px;
    background: #f59e0b22; padding: 2px 8px; border-radius: 20px;
  }

  .seed-group { margin-bottom: 18px; }
  .seed-title {
    color: #f59e0b; font-weight: 600; font-size: 15px;
    margin-bottom: 8px; padding-left: 4px;
  }
  .suggest-item {
    padding: 5px 0 5px 20px; color: #a5b4fc;
    border-left: 2px solid #333; margin-left: 8px;
  }

  .all-keyword {
    display: inline-block; background: #252540;
    padding: 6px 14px; margin: 4px; border-radius: 20px;
    font-size: 13px; color: #6ee7b7;
    transition: all 0.2s;
  }
  .all-keyword:hover { background: #3b82f6; color: white; }

  .spinner {
    display: inline-block; width: 16px; height: 16px;
    border: 2px solid #333; border-top: 2px solid #3b82f6;
    border-radius: 50%; animation: spin 0.8s linear infinite;
    margin-right: 8px; vertical-align: middle;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  .empty { color: #555; text-align: center; padding: 40px; font-size: 15px; }
</style>
</head>
<body>
<div class="container">
  <h1>Trending Keywords</h1>

  <div class="input-row">
    <input type="text" id="seeds" placeholder="키워드 입력 (쉼표 구분) - 예: 맛집, 여행, 다이어트"
           value="오늘, 추천, 방법, 비교, 후기, 순위">
  </div>

  <div class="btn-row">
    <button class="btn btn-primary" id="searchBtn" onclick="doSearch()">검색 시작</button>
    <button class="btn btn-green" id="copyBtn" onclick="copyKeywords()" disabled>키워드 복사</button>
    <button class="btn btn-purple" id="saveInfo" style="display:none"></button>
  </div>

  <div class="status" id="status">준비됨 - 키워드를 입력하고 검색을 시작하세요</div>

  <div class="tabs">
    <button class="tab active" onclick="showTab(0)">구글 트렌드</button>
    <button class="tab" onclick="showTab(1)">구글 자동완성</button>
    <button class="tab" onclick="showTab(2)">네이버 자동완성</button>
    <button class="tab" onclick="showTab(3)">전체 키워드</button>
  </div>

  <div class="panel active" id="panel0"><div class="empty">검색을 시작하세요</div></div>
  <div class="panel" id="panel1"><div class="empty">검색을 시작하세요</div></div>
  <div class="panel" id="panel2"><div class="empty">검색을 시작하세요</div></div>
  <div class="panel" id="panel3"><div class="empty">검색을 시작하세요</div></div>
</div>

<script>
let lastResult = null;

document.getElementById('seeds').addEventListener('keydown', e => {
  if (e.key === 'Enter') doSearch();
});

function showTab(i) {
  document.querySelectorAll('.tab').forEach((t, idx) => t.classList.toggle('active', idx === i));
  document.querySelectorAll('.panel').forEach((p, idx) => p.classList.toggle('active', idx === i));
}

async function doSearch() {
  const btn = document.getElementById('searchBtn');
  const status = document.getElementById('status');
  btn.disabled = true;
  status.innerHTML = '<span class="spinner"></span>수집 중... (10~15초 소요)';

  const seedsText = document.getElementById('seeds').value;
  const seeds = seedsText.split(',').map(s => s.trim()).filter(s => s);

  try {
    const resp = await fetch('/api/search', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({seeds})
    });
    lastResult = await resp.json();
    renderResults(lastResult);

    document.getElementById('copyBtn').disabled = false;
    const saveBtn = document.getElementById('saveInfo');
    saveBtn.style.display = 'inline-block';
    saveBtn.textContent = '자동 저장됨';
    saveBtn.title = lastResult.saved_to;

    status.textContent = `완료! ${lastResult.all_unique_keywords.length}개 키워드 수집 (${lastResult.timestamp})`;
  } catch(e) {
    status.textContent = '오류: ' + e.message;
  }
  btn.disabled = false;
}

function renderResults(data) {
  // 구글 트렌드
  let html = '';
  data.google_trends.forEach((item, i) => {
    html += `<div class="keyword-item">
      <span class="keyword-num">${i+1}</span>
      <span class="keyword-text">${item.keyword}</span>
      ${item.traffic ? `<span class="keyword-traffic">${item.traffic}</span>` : ''}
    </div>`;
  });
  document.getElementById('panel0').innerHTML = html || '<div class="empty">데이터 없음</div>';

  // 구글 자동완성
  html = '';
  for (const [seed, suggestions] of Object.entries(data.google_suggest)) {
    html += `<div class="seed-group"><div class="seed-title">"${seed}"</div>`;
    suggestions.forEach(s => { html += `<div class="suggest-item">${s}</div>`; });
    html += '</div>';
  }
  document.getElementById('panel1').innerHTML = html || '<div class="empty">데이터 없음</div>';

  // 네이버 자동완성
  html = '';
  for (const [seed, suggestions] of Object.entries(data.naver_suggest)) {
    html += `<div class="seed-group"><div class="seed-title">"${seed}"</div>`;
    suggestions.forEach(s => { html += `<div class="suggest-item">${s}</div>`; });
    html += '</div>';
  }
  document.getElementById('panel2').innerHTML = html || '<div class="empty">데이터 없음</div>';

  // 전체 키워드
  html = '';
  data.all_unique_keywords.forEach(kw => {
    html += `<span class="all-keyword">${kw}</span>`;
  });
  document.getElementById('panel3').innerHTML = html || '<div class="empty">데이터 없음</div>';
}

function copyKeywords() {
  if (!lastResult) return;
  const text = lastResult.all_unique_keywords.join('\\n');
  navigator.clipboard.writeText(text).then(() => {
    document.getElementById('status').textContent =
      `클립보드에 ${lastResult.all_unique_keywords.length}개 키워드 복사됨!`;
  });
}
</script>
</body>
</html>
"""

if __name__ == "__main__":
    print("\n  Trending Keywords 서버 시작!")
    print("  http://localhost:8877 에서 접속하세요\n")
    threading.Timer(1, lambda: webbrowser.open("http://localhost:8877")).start()
    app.run(host="0.0.0.0", port=8877, debug=False)
