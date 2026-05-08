#!/usr/bin/env bash
# GitHub Pages 公開用のビルドスクリプト。
# Marp スライドを HTML 化し、KPI ダッシュボード等と一緒に dist/ にまとめる。
# ローカル動作確認: bash scripts/build-pages.sh dist
# Actions からも同じスクリプトを呼ぶ。

set -euo pipefail

DIST="${1:-dist}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cd "$ROOT"
rm -rf "$DIST"
mkdir -p "$DIST/demo" "$DIST/outreach" "$DIST/dashboard"

build_slide() {
  local src="$1"
  local out="$2"
  echo "  $src -> $out"
  npx --yes @marp-team/marp-cli@latest "$src" --html --output "$out" >/dev/null
}

echo "[1/3] Building Marp slides..."
build_slide phase1_proposal/proposals/demo/tax_office_slides.md "$DIST/demo/tax_office.html"
build_slide phase1_proposal/proposals/demo/law_office_slides.md "$DIST/demo/law_office.html"
build_slide phase1_proposal/proposals/outreach/daikanyama_intro.md "$DIST/outreach/daikanyama.html"
build_slide phase1_proposal/proposals/outreach/hillford_intro.md "$DIST/outreach/hillford.html"

echo "[2/3] Copying static assets..."
cp phase4_reporting/kpi_dashboard_template.html "$DIST/dashboard/index.html"

echo "[3/3] Generating index.html..."
BUILT_AT="$(date -u +'%Y-%m-%d %H:%M UTC')"
GIT_SHA="$(git rev-parse --short HEAD 2>/dev/null || echo '-')"
GIT_BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '-')"

cat > "$DIST/index.html" <<HTML
<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0f172a">
<title>aiforpro / 士業向けAI導入コンサル 成果物</title>
<style>
  :root {
    --bg: #0f172a;
    --panel: #1e293b;
    --text: #e2e8f0;
    --muted: #94a3b8;
    --link: #38bdf8;
    --accent: #4ade80;
    --warn: #fbbf24;
    --border: #334155;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body {
    font-family: -apple-system, "Hiragino Sans", "Yu Gothic UI", "Meiryo", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
  }
  header {
    padding: 28px 20px 16px;
    border-bottom: 1px solid var(--border);
  }
  header h1 { margin: 0 0 4px; font-size: 22px; }
  header p { margin: 0; color: var(--muted); font-size: 13px; }
  main { padding: 16px 14px 60px; max-width: 720px; margin: 0 auto; }
  section { margin-top: 28px; }
  section h2 {
    font-size: 15px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0 0 10px;
    padding: 0 6px;
  }
  ul { list-style: none; padding: 0; margin: 0; }
  li { margin-bottom: 10px; }
  a.card {
    display: block;
    padding: 16px 18px;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    text-decoration: none;
    color: var(--text);
    transition: border-color .15s, transform .05s;
  }
  a.card:active { transform: scale(0.99); }
  a.card:hover { border-color: var(--link); }
  .title { font-weight: 700; font-size: 16px; }
  .desc { color: var(--muted); font-size: 13px; margin-top: 4px; }
  .pill {
    display: inline-block;
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 999px;
    background: #0b1220;
    border: 1px solid var(--border);
    color: var(--muted);
    margin-right: 6px;
    vertical-align: middle;
  }
  .pill.demo { color: #a5f3fc; border-color: #155e75; }
  .pill.outreach { color: #fde68a; border-color: #92400e; }
  .pill.tool { color: #c4b5fd; border-color: #5b21b6; }
  footer {
    padding: 24px 20px;
    color: var(--muted);
    font-size: 12px;
    border-top: 1px solid var(--border);
    text-align: center;
  }
  footer a { color: var(--link); }
  .note {
    background: #0b1220;
    border-left: 3px solid var(--warn);
    border-radius: 6px;
    padding: 10px 14px;
    color: var(--muted);
    font-size: 12px;
    margin-top: 12px;
  }
</style>
</head>
<body>
<header>
  <h1>士業向けAI導入コンサル / 成果物</h1>
  <p>最終更新 ${BUILT_AT} ／ branch: ${GIT_BRANCH} ／ ${GIT_SHA}</p>
</header>

<main>
  <section>
    <h2>提案スライド</h2>
    <ul>
      <li>
        <a class="card" href="./outreach/daikanyama.html">
          <div><span class="pill outreach">打診版</span><span class="title">代官山綜合法律事務所 様</span></div>
          <div class="desc">知人経由・初回打診用 / 10スライド / 公開情報ベース</div>
        </a>
      </li>
      <li>
        <a class="card" href="./outreach/hillford.html">
          <div><span class="pill outreach">打診版</span><span class="title">ヒルフォード法律事務所 様</span></div>
          <div class="desc">知人経由・初回打診用 / 10スライド / プレースホルダ多め</div>
        </a>
      </li>
      <li>
        <a class="card" href="./demo/law_office.html">
          <div><span class="pill demo">デモ</span><span class="title">弁護士事務所向け（丸の内総合・仮）</span></div>
          <div class="desc">本格提案版テンプレート / 15スライド / 月48h・年454万円削減 想定</div>
        </a>
      </li>
      <li>
        <a class="card" href="./demo/tax_office.html">
          <div><span class="pill demo">デモ</span><span class="title">税理士事務所向け（神田・仮）</span></div>
          <div class="desc">本格提案版テンプレート / 15スライド / 月65h・年352万円削減 想定</div>
        </a>
      </li>
    </ul>
  </section>

  <section>
    <h2>ツール</h2>
    <ul>
      <li>
        <a class="card" href="./dashboard/">
          <div><span class="pill tool">テンプレート</span><span class="title">月次KPIダッシュボード</span></div>
          <div class="desc">Phase4 成果報告用 HTML テンプレート（プレースホルダ含む）</div>
        </a>
      </li>
    </ul>
  </section>

  <section>
    <h2>ソースコード</h2>
    <ul>
      <li>
        <a class="card" href="https://github.com/kenjisakuragi/aiforpro" target="_blank" rel="noopener">
          <div><span class="title">GitHub リポジトリ</span></div>
          <div class="desc">CLAUDE.md / ヒアリングシート / ROI計算スクリプト 等</div>
        </a>
      </li>
    </ul>
  </section>

  <div class="note">
    本サイトは AI を活用して作成された成果物のドラフトです。記載の試算値は仮データまたは公開情報・業界平均ベースであり、最終的な確認・判断は士業有資格者が行います。
  </div>
</main>

<footer>
  © 2026 株式会社 VIBE SHIP / <a href="https://github.com/kenjisakuragi/aiforpro">aiforpro</a>
</footer>
</body>
</html>
HTML

echo
echo "Done. Output: $DIST/"
echo "Open: $DIST/index.html"
