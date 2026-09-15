# 脳の仕組み 複数ページ化 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 1ページ完結だった `brain` セクションを、本編10ページ＋コラム8ページ＋入口＋コラム一覧＝全20ページの解説サイトに組み替え、m-note.uk に段階公開する。

**Architecture:** 全HTMLをリポジトリのルート直下にフラット配置し、`css/style.css` を共通スタイルとして各ページが1行の `<link>` で読み込む。JavaScriptは使わない。ページ間の回遊はパンくず・前後リンク・末尾のサイトマップだけで担保する。テストフレームワークは無いので、`tools/check.py`（依存なしの静的検査）がこのプロジェクトのテストにあたる。各ページタスクは「checkが落ちる → ページを書く → checkが通る → ブラウザ目視 → コミット」のサイクルで進める。

**Tech Stack:** 静的HTML5 / CSS（カスタムプロパティ、`prefers-color-scheme`）/ インラインSVG / Google Fonts（Zen Maru Gothic, Noto Sans JP）/ Python 3 標準ライブラリのみ（検査スクリプト）/ GitHub Pages / `gh` CLI

**Spec:** `docs/superpowers/specs/2026-09-15-brain-multipage-design.md`

## Global Constraints

- 全HTMLはリポジトリのルート直下。サブディレクトリは `css/` と `tools/` と `docs/` のみ。
- `<html lang="ja">`、`<meta name="description">` を全ページに置く。
- favicon は全ページ共通で 🧠 の data URI。既存 `index.html` の行をそのまま複製する。
- 外部依存は Google Fonts のみ。JavaScriptは一切使わない。
- ラスター画像（`<img>`）を使わない。図はすべてインラインSVG。
- 各 `<svg role="img">` は直下に `<title id="...">` を持ち、`aria-labelledby` でそれを指す。
- 最大幅 720px、左右パディング 24px。375px幅で横スクロールを出さない。
- フッターの免責文は全ページ同一:
  `専門家ではない個人が調べ、考えたことをまとめた個人的なまとめです。内容の正確性を保証するものではありません。`
- ヘッダーとフッターに `../` への「← m-note トップ」を置く。
- 三位一体脳モデル（爬虫類脳→哺乳類脳→人間脳）は採用しない。`anatomy.html` では解剖学的な三層のみを描き、動物の対応づけは入れない。
- 未完成のページへのリンクは、その段階では出さない（`tools/check.py` がリンク切れとして検出する）。
- コミットメッセージは日本語1行サマリ + 空行 + `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`
- 公開は `git push origin main` → GitHub Pages のビルド完了を待つ → `curl` で確認、の順。

---

## File Structure

| ファイル | 責務 |
|---|---|
| `tools/check.py` | サイト全体の静的検査。リンク切れ、必須要素の欠落、SVGのtitle欠落、ラスター画像の混入を検出する |
| `css/style.css` | 全ページ共通のトークン・ベース・コンポーネント・SVGクラス |
| `index.html` | 入口。ヒーロー、三部のカード、コラムへの導線 |
| `cells.html` `anatomy.html` `networks.html` | 第1部 基本 |
| `signal.html` `synapse.html` `chemicals.html` | 第2部 仕組み |
| `perceive.html` `remember.html` `attention.html` `decide.html` | 第3部 はたらき |
| `columns.html` | コラム一覧 |
| `prediction.html` `free-energy.html` `thousand-brains.html` `dmn.html` `self-model.html` `consciousness.html` `anatta.html` `brain-and-ai.html` | コラム8本 |

既存の `index.html`（10章18,000字・図14点）は Task 3 で入口ページに置き換える。
中身は各タスクで新ページへ移す。移し終えるまで元ファイルを消さないため、
Task 3 の前に `docs/legacy/2026-09-14-single-page.html` へ退避する。

---

## 共通マークアップ（全ページで一字一句同じ）

以降のタスクは、このブロックを**そのまま**使う。

### `<head>` 内

```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__PAGETITLE__ ｜ 脳の仕組み</title>
<meta name="description" content="__DESC__">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🧠</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
```

### `<body>` 冒頭の SVG defs（矢印マーカー。同一ドキュメント内でしか参照できないため各ページに複製する）

```html
<svg width="0" height="0" aria-hidden="true" focusable="false" style="position:absolute">
  <defs>
    <marker id="ar-i" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z"/></marker>
    <marker id="ar-e" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z"/></marker>
    <marker id="ar-f" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z"/></marker>
  </defs>
</svg>
```

### ヘッダー

```html
<header class="top">
  <div class="wrap">
    <a class="sitemark" href="index.html">BRAIN ｜ 脳の仕組み</a>
    <a class="back" href="../">← m-note トップ</a>
  </div>
</header>
```

### パンくず（本編ページ。`__PART__` は「第1部 基本」等、`__SELF__` はページ名）

```html
<nav class="crumb" aria-label="パンくず">
  <a href="index.html">脳の仕組み</a><span>›</span><span>__PART__</span><span>›</span><span>__SELF__</span>
</nav>
```

コラムページは `__PART__` を `コラム` にし、`<a href="columns.html">コラム</a>` とする。

### コラム誘導カード（本編の該当箇所に置く）

```html
<aside class="colcard">
  <a href="__COLUMN__.html">
    <span class="k">COLUMN</span>
    <span class="t">__COLUMNTITLE__</span>
    <span class="d">__ONELINE__</span>
  </a>
</aside>
```

### 前へ／次へ（本編ページ）

```html
<nav class="pager" aria-label="ページ送り">
  <a class="prev" href="__PREV__.html"><span class="k">前へ</span><span class="t">__PREVTITLE__</span></a>
  <a class="next" href="__NEXT__.html"><span class="k">次へ</span><span class="t">__NEXTTITLE__</span></a>
</nav>
```

端のページでは、無い側の `<a>` を丸ごと省略する（空の `<a>` を残さない）。

### サイトマップ（全ページ共通。**その時点で存在するページだけ**を載せる）

```html
<nav class="sitemap" aria-label="このサイトの地図">
  <h2>このサイトの地図</h2>
  <div class="grp">
    <p class="k">第1部 基本</p>
    <ul>
      <li><a href="cells.html">01 脳をつくる細胞</a></li>
      <li><a href="anatomy.html">02 脳の地図</a></li>
      <li><a href="networks.html">03 つながりが機能をつくる</a></li>
    </ul>
  </div>
</nav>
```

第2部・第3部・コラムのグループは、そのページ群を作ったタスクで追記する。

### フッター

```html
<footer class="foot">
  <div class="wrap">
    <p>専門家ではない個人が調べ、考えたことをまとめた個人的なまとめです。内容の正確性を保証するものではありません。</p>
    <p><a href="../">← m-note トップ</a></p>
  </div>
</footer>
```

---

## Task 1: 検証スクリプト

**Files:**
- Create: `tools/check.py`

**Interfaces:**
- Produces: `python3 tools/check.py` — 問題があれば1行1件で標準出力に出し、exit 1。問題が無ければ `OK: N pages checked` を出し exit 0。
- Produces: `tools/check.py` 内の `STRUCTURE` 辞書 — 本編とコラムの正式な順序。後続タスクはここに1行追加してからページを作る。

- [ ] **Step 1: 失敗する検査スクリプトを書く**

`tools/check.py` を作る。外部依存なし（Python 3 標準ライブラリのみ）。

```python
#!/usr/bin/env python3
"""brain セクションの静的検査。依存なし。"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# サイトの正式な構造。ページを増やすときはここに追記してから作る。
STRUCTURE = {
    "第1部 基本":   ["cells", "anatomy", "networks"],
    "第2部 仕組み": ["signal", "synapse", "chemicals"],
    "第3部 はたらき": ["perceive", "remember", "attention", "decide"],
    "コラム": ["prediction", "free-energy", "thousand-brains", "dmn",
               "self-model", "consciousness", "anatta", "brain-and-ai"],
}
HUBS = ["index", "columns"]

DISCLAIMER = ("専門家ではない個人が調べ、考えたことをまとめた個人的なまとめです。"
              "内容の正確性を保証するものではありません。")

problems = []


def err(page, msg):
    problems.append("%s: %s" % (page, msg))


def check(path, name, html):
    if '<html lang="ja">' not in html:
        err(name, 'lang="ja" がない')
    if not re.search(r"<title>[^<]+</title>", html):
        err(name, "<title> がない")
    if not re.search(r'<meta name="description" content="[^"]{10,}"', html):
        err(name, "meta description がない、または短すぎる")
    if 'href="css/style.css"' not in html:
        err(name, "css/style.css を読み込んでいない")
    if html.count('href="../"') < 2:
        err(name, "「← m-note トップ」が header と footer の2か所にない")
    if DISCLAIMER not in html:
        err(name, "フッターの免責文が仕様と一致しない")
    if re.search(r"<img\b", html):
        err(name, "<img> が混入している（図はインラインSVGのみ）")

    # 本編ページはパンくずと前後リンクを持つ
    is_hub = name in HUBS
    if not is_hub:
        if 'class="crumb"' not in html:
            err(name, "パンくずがない")
        if 'class="pager"' not in html and name not in STRUCTURE["コラム"]:
            err(name, "前へ／次へがない")

    # role="img" の svg は title を持つ
    for m in re.finditer(r'<svg\b[^>]*role="img"[^>]*>(.*?)</svg>', html, re.S):
        head = m.group(0)[:400]
        if "aria-labelledby=" not in head:
            err(name, "svg role=img に aria-labelledby がない")
        if "<title" not in m.group(1)[:400]:
            err(name, "svg role=img に <title> がない")

    # id の重複（同一ドキュメント内で id は一意でなければならない）
    ids = re.findall(r'\sid="([^"]+)"', html)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    for i in dup:
        err(name, "id が重複している: %s" % i)

    # 内部リンクの解決
    for href in re.findall(r'href="([^"]+)"', html):
        if href.startswith(("http://", "https://", "mailto:", "data:", "#", "../")):
            continue
        target = href.split("#")[0]
        if not target:
            continue
        if not os.path.exists(os.path.join(ROOT, target)):
            err(name, "リンク切れ: %s" % href)


def main():
    pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    if not pages:
        print("html が1つもない")
        return 1
    for f in pages:
        name = f[:-5]
        with open(os.path.join(ROOT, f), encoding="utf-8") as fh:
            check(os.path.join(ROOT, f), name, fh.read())

    known = set(HUBS)
    for group in STRUCTURE.values():
        known |= set(group)
    for f in pages:
        if f[:-5] not in known:
            err(f[:-5], "STRUCTURE にも HUBS にも載っていない")

    for line in problems:
        print(line)
    if problems:
        print("\n%d problems" % len(problems))
        return 1
    print("OK: %d pages checked" % len(pages))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: 実行して現状で落ちることを確認する**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: FAIL（exit 1）。既存 `index.html` は新しい共通マークアップを満たしていないので、
`index: css/style.css を読み込んでいない` などが並ぶ。ここで落ちるのが正しい。

- [ ] **Step 3: 検査対象が想定どおりか確かめる**

現行 `index.html` は `f7-t` を2回使っている（「幅を持つ『今』」と「情報入力が、ぼんやりする時間を押し縮める」）。
これは同一ドキュメント内の id 重複で、いまの公開ページにある不具合。
Step 1 で足した重複チェックがこれを拾うことを確認する。

Run: `cd ~/Claude/brain && python3 tools/check.py | grep 'id が重複'`
Expected: `index: id が重複している: f7-t`

この不具合は Task 19 と Task 20 で図を移すときに解消する。

- [ ] **Step 4: コミット**

```bash
cd ~/Claude/brain
git add tools/check.py
git commit -m "$(printf 'サイト検査スクリプトを追加\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 2: 共通スタイル

**Files:**
- Create: `css/style.css`

**Interfaces（後続タスクが依存する名前。ここで決めた綴りを変えない）:**

トークン（`:root` と `@media (prefers-color-scheme: dark) :root` の両方で定義）:
`--ground --paper --ink --ink-soft --ink-faint --primary --primary-soft --accent --line --wash --shadow --primary-rgb --l0 --l1 --l2 --l3 --l4 --r-card --r-pill`

レイアウト: `.wrap .top .sitemark .back .crumb .lede .part-label .col-label .pager .pager .prev .pager .next .pager .k .pager .t .sitemap .sitemap .grp .sitemap .k .foot`

本文: `.fig .fig figcaption .tbl-scroll .q .q-label .colcard .colcard .k .colcard .t .colcard .d .err .chip .c0 .c1 .c2 .c3 .c4 .ce`

SVG: `.s-i`（主色の実線）`.s-e`（朱の破線）`.s-l .s-f .box .f-i .f-e .lb .ti .te .fill-0 .fill-1 .fill-2 .fill-3 .fill-4 .gyri .edge .sulc`
`#ar-i path { fill: var(--primary) }` `#ar-e path { fill: var(--accent) }` `#ar-f path { fill: var(--ink-faint) }`

**SVGのクラス名は現行 `index.html` と同一に保つ。** これにより既存14点のSVGを一字も直さずに新ページへ移せる。
変わるのはCSS側の色定義だけ。

- [ ] **Step 1: 既存の style ブロックを取り出す**

```bash
cd ~/Claude/brain
python3 - <<'EOF'
import re
s = open('index.html', encoding='utf-8').read()
m = re.search(r'<style>(.*?)</style>', s, re.S)
open('/tmp/old-style.css', 'w', encoding='utf-8').write(m.group(1))
print(len(m.group(1)), 'chars extracted')
EOF
```

- [ ] **Step 2: `css/style.css` を書く**

`/tmp/old-style.css` を土台に、次を変更する。

トークンを暖色に置き換える（**この値をそのまま使う**）:

```css
:root {
  --ground: #f7f1e7;
  --paper: #fffcf7;
  --ink: #33261c;
  --ink-soft: #6b5748;
  --ink-faint: #9e8a78;
  --primary: #8a5a2b;
  --primary-soft: #c9a97e;
  --accent: #cc4b33;
  --line: #e3d7c6;
  --wash: rgba(138, 90, 43, 0.05);
  --primary-rgb: 138, 90, 43;
  --l0: #fbf4e7;
  --l1: #f3e6ce;
  --l2: #e8d3ac;
  --l3: #dabf8c;
  --l4: #c9a46a;
  --shadow: 0 1px 2px rgba(51, 38, 28, 0.04), 0 10px 30px rgba(51, 38, 28, 0.06);
  --r-card: 16px;
  --r-pill: 999px;
}
@media (prefers-color-scheme: dark) {
  :root {
    --ground: #191410;
    --paper: #241d16;
    --ink: #f0e5d7;
    --ink-soft: #bca893;
    --ink-faint: #8a7462;
    --primary: #dca76a;
    --primary-soft: #6b5033;
    --accent: #e9765c;
    --line: #382c22;
    --wash: rgba(220, 167, 106, 0.07);
    --primary-rgb: 220, 167, 106;
    --l0: #221b14;
    --l1: #2a2118;
    --l2: #352920;
    --l3: #413227;
    --l4: #4e3c2d;
    --shadow: 0 1px 2px rgba(0, 0, 0, 0.25), 0 10px 30px rgba(0, 0, 0, 0.3);
  }
}
```

書体を差し替える:

```css
body {
  font-family: "Noto Sans JP", "Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic", sans-serif;
}
h1, h2, h3, .sitemark, .part-label, .col-label, .colcard .t, .pager .t, .sitemap h2, .fig text {
  font-family: "Zen Maru Gothic", "Hiragino Maru Gothic ProN", "Noto Sans JP", sans-serif;
  font-weight: 700;
}
```

`.serif` クラスと `Noto Serif JP` の読み込みは削除する（明朝は使わない）。

旧トークン名を全て置換する: `--indigo` → `--primary`、`--indigo-soft` → `--primary-soft`、
`--vermilion` → `--accent`、`--indigo-rgb` → `--primary-rgb`。
`#ar-i path`/`#ar-e path` の `fill` も新しい変数名にする。

丸みを足す:

```css
.fig { border-radius: var(--r-card); }
.colcard a, .pager a { border-radius: var(--r-card); }
.part-label, .col-label, .chip { border-radius: var(--r-pill); }
```

新しいコンポーネントを追加する。

```css
/* パンくず */
.crumb { max-width: 720px; margin: 0 auto; padding: 18px 24px 0; font-size: 12.5px; color: var(--ink-faint); }
.crumb a { color: var(--ink-soft); text-decoration: none; }
.crumb a:hover { color: var(--primary); }
.crumb span { margin: 0 8px; }

/* 部・コラムのラベル */
.part-label, .col-label {
  display: inline-block; padding: 5px 14px; font-size: 11px; letter-spacing: .16em;
}
.part-label { background: var(--wash); color: var(--primary); }
.col-label { background: var(--paper); color: var(--accent); border: 1px solid var(--accent); }

/* リード文 */
.lede { color: var(--ink-soft); font-size: 15.5px; margin: 0 0 8px; }

/* コラム誘導カード */
.colcard { margin: 34px 0; }
.colcard a {
  display: block; padding: 18px 20px; background: var(--paper);
  border: 1px solid var(--line); border-left: 3px solid var(--accent);
  text-decoration: none; box-shadow: var(--shadow);
}
.colcard a:hover { border-color: var(--accent); }
.colcard .k { display: block; font-size: 10.5px; letter-spacing: .18em; color: var(--accent); margin-bottom: 6px; }
.colcard .t { display: block; font-size: 15px; color: var(--ink); margin-bottom: 4px; }
.colcard .d { display: block; font-size: 12.5px; color: var(--ink-faint); line-height: 1.7; }

/* 前へ／次へ */
.pager { display: flex; gap: 12px; max-width: 720px; margin: 72px auto 0; padding: 0 24px; }
.pager a {
  flex: 1; padding: 16px 18px; background: var(--paper); border: 1px solid var(--line);
  text-decoration: none; box-shadow: var(--shadow);
}
.pager a:hover { border-color: var(--primary-soft); }
.pager .next { text-align: right; }
.pager .k { display: block; font-size: 10.5px; letter-spacing: .16em; color: var(--ink-faint); margin-bottom: 5px; }
.pager .t { display: block; font-size: 14px; color: var(--ink); }

/* サイトマップ */
.sitemap { max-width: 720px; margin: 72px auto 0; padding: 0 24px; }
.sitemap h2 { font-size: 13px; letter-spacing: .12em; color: var(--ink-faint); margin: 0 0 18px; font-weight: 500; }
.sitemap .grp { margin-bottom: 22px; }
.sitemap .k { font-size: 11px; letter-spacing: .16em; color: var(--primary); margin: 0 0 8px; }
.sitemap ul { list-style: none; margin: 0; padding: 0; }
.sitemap li { margin: 0 0 6px; }
.sitemap a { font-size: 14px; color: var(--ink); text-decoration: none; }
.sitemap a:hover { color: var(--primary); text-decoration: underline; }

@media (max-width: 560px) {
  .pager { flex-direction: column; }
  .pager .next { text-align: left; }
}
```

- [ ] **Step 3: 検査を実行する**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: まだ FAIL。`index` が旧マークアップのままなので `css/style.css を読み込んでいない` が残る。
`css/style.css` 自体は検査対象外（.html のみ）なので、ここでの合格は求めない。

- [ ] **Step 4: CSSが壊れていないことを確認する**

```bash
cd ~/Claude/brain
python3 - <<'EOF'
s = open('css/style.css', encoding='utf-8').read()
assert s.count('{') == s.count('}'), '波括弧の数が合わない'
for tok in ['--ground','--paper','--ink','--primary','--accent','--l0','--l4','--r-card','--r-pill']:
    assert s.count(tok) >= 2, tok + ' がライト/ダークの両方に無い'
for old in ['--indigo','--vermilion','Noto Serif JP']:
    assert old not in s, '旧トークンが残っている: ' + old
print('style.css OK', len(s), 'chars')
EOF
```

Expected: `style.css OK ...`

- [ ] **Step 5: コミット**

```bash
cd ~/Claude/brain
git add css/style.css
git commit -m "$(printf '共通スタイルを暖色・丸みに切り替えて css/style.css に分離\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 3: 入口ページ

**Files:**
- Create: `docs/legacy/2026-09-14-single-page.html`（既存 index.html の退避）
- Modify: `index.html`（全面置き換え）

**Interfaces:**
- Consumes: Task 2 の全クラス
- Produces: `index.html` — 全ページの `.sitemark` と `.crumb` のリンク先

- [ ] **Step 1: 既存ページを退避する**

```bash
cd ~/Claude/brain
mkdir -p docs/legacy
cp index.html docs/legacy/2026-09-14-single-page.html
```

以降のページタスクは、この退避ファイルから本文と既存SVGを取り出す。

- [ ] **Step 2: `index.html` を書き直す**

構成（この順序で）:

1. 共通マークアップの `<head>`。`__PAGETITLE__` = `脳の仕組み`、`<title>` は `脳の仕組み ｜ m-note`（入口だけ例外）。description は現行 index.html のものを流用。
2. SVG defs ブロック
3. ヘッダー
4. パンくずは置かない（入口のため）
5. ヒーロー: `.part-label` に `HOW THE BRAIN WORKS`、`h1` は現行の
   `脳は世界を受け取っていない。/ 予測し、選択し、作っている。` を引き継ぐ。
   `.lede` 2本も現行から引き継ぐ。
6. 「このサイトの歩き方」: 3〜4行。本編は順に読める一本道であること、
   理論はコラムに置いてあり読み飛ばしても本編は続くこと。
7. 三部のカード（`.colcard` と同じ見た目の `<a>` を3つ。第1部/第2部/第3部それぞれに
   1行の説明と収録ページ名）。**この時点では第1部のリンクのみ有効**にし、
   第2部・第3部・コラムのカードは `<a>` にせず `<div>` で「準備中」と出す。
8. サイトマップ（第1部のみ）
9. フッター

- [ ] **Step 3: 検査を実行する**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `index: リンク切れ: cells.html` 等が出て FAIL。第1部がまだ無いため。
Step 2 で第1部へのリンクを張ったなら、この失敗が正しい。

- [ ] **Step 4: 第1部が揃うまでリンクを出さない**

Step 2 の三部カードとサイトマップから、第1部のリンクも一旦外す（`<div>` 表記にする）。

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 1 pages checked`

- [ ] **Step 5: ブラウザで確認する**

`cd ~/Claude/brain && python3 -m http.server 8731` を起動し、
`http://localhost:8731/` を 780px幅と375px幅、ライト／ダークの計4通りで表示して、
暖色の配色・丸ゴシックの見出し・角丸が意図通りか、横スクロールが出ないかを目視する。

- [ ] **Step 6: コミット**

```bash
cd ~/Claude/brain
git add index.html docs/legacy/2026-09-14-single-page.html
git commit -m "$(printf '入口ページを作り、旧1ページ版を docs/legacy に退避\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 4: 01 脳をつくる細胞

**Files:**
- Create: `cells.html`
- Modify: `index.html`（第1部カードとサイトマップに `cells.html` を追加）

**Interfaces:**
- Consumes: Task 2 の `.fig .s-i .s-e .box .f-e .lb .ti .te` / Task 3 の `index.html`
- Produces: `cells.html` — `anatomy.html` の `.pager .prev` のリンク先

**このページの見出し（この通りに作る）:**

- リード文（2〜3行）
- `h2` 1000億という数
- `h2` ニューロンの構造
- `h2` ニューロンだけではない — グリア細胞
- `h2` 一種類ではない — 細胞の多様性

**図2点:**
- 既存「ニューロンとシナプス」（`docs/legacy/2026-09-14-single-page.html` の `f1a-t` のSVGをそのまま移す）
- 新規「グリアとニューロン」— 星状膠細胞・希突起膠細胞・ミクログリアがニューロンを取り巻く模式図。
  `viewBox="0 0 640 260"`、`<title id="fglia-t">グリア細胞とニューロン</title>`

**コラム誘導:** なし（このページからは出さない）

**前後:** prev なし（index が前）、next = `anatomy.html`（この時点では未作成なので pager は prev/next とも省略し、Task 5 で追加する）

- [ ] **Step 1: 既存SVGを取り出す**

```bash
cd ~/Claude/brain
python3 - <<'EOF'
import re
s = open('docs/legacy/2026-09-14-single-page.html', encoding='utf-8').read()
m = re.search(r'<figure class="fig">\s*<svg[^>]*aria-labelledby="f1a-t".*?</figure>', s, re.S)
open('/tmp/fig-neuron.html', 'w', encoding='utf-8').write(m.group(0))
print('extracted', len(m.group(0)), 'chars')
EOF
```

- [ ] **Step 2: `cells.html` を書く**

共通マークアップ + 上の見出し構成 + 図2点。本文3,000〜4,000字。

内容の要点:
- 1000億個のニューロン、結合は100兆超。ただし「数が多いから賢い」ではなく、
  つながり方が効くという点を先に置く（`networks.html` への伏線）。
- 細胞体・樹状突起・軸索・シナプス。樹状突起が入力、軸索が出力。
- グリア細胞はニューロンと同数かそれ以上。星状膠細胞（血流と栄養、シナプスの調整）、
  希突起膠細胞（髄鞘をつくる → `signal.html` への伏線）、ミクログリア（免疫、不要な結合の刈り込み）。
  「支持細胞」という古い扱いは改まりつつあること。
- 錐体細胞・介在ニューロンなど、ニューロン自体にも多様性があること。

- [ ] **Step 3: 検査を実行する**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 2 pages checked`
（`index.html` からまだ `cells.html` へリンクしていないので、リンク切れは出ない）

- [ ] **Step 4: index から第1部の1本目にリンクを張る**

`index.html` の第1部カードを `<a href="cells.html">` にし、サイトマップの第1部グループに
`<li><a href="cells.html">01 脳をつくる細胞</a></li>` を足す。
`cells.html` のサイトマップにも同じグループを置く。

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 2 pages checked`

- [ ] **Step 5: ブラウザで確認する**

780px / 375px、ライト／ダークで `http://localhost:8731/cells.html` を目視。
既存SVGが新しい暖色トークンで正しく描画されているか（`.s-i` が褐色、`.f-e` が朱）を確認する。

- [ ] **Step 6: コミット**

```bash
cd ~/Claude/brain
git add cells.html index.html
git commit -m "$(printf '第1部01「脳をつくる細胞」を追加\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 5: 02 脳の地図

**Files:**
- Create: `anatomy.html`
- Modify: `cells.html`（pager に next を追加）、`index.html`（サイトマップ）

**Interfaces:**
- Consumes: Task 2 の `.fill-0`〜`.fill-4` `.gyri` `.edge` `.sulc` `.chip` `.c0`〜`.c4` `.ce` `.tbl-scroll`
- Produces: `anatomy.html` — `networks.html` の prev

**見出し:**
- リード文
- `h2` 古い層の上に、新しい層
- `h2` 外側を覆う四つの葉
- `h2` 内側の構造 — 視床・扁桃体・海馬
- `h2` 左と右

**図3点:**
- 既存「進化の三層」（`f1L-t`）
- 既存「脳の外側面」（`f1b-t`）
- 新規「左右半球と脳梁」— 上から見た二つの半球と、それをつなぐ脳梁。
  `viewBox="0 0 640 300"`、`<title id="fhemi-t">左右の半球と脳梁</title>`

**表:** 既存の部位一覧表（色チップつき）をそのまま移す。

**重要:** 三位一体脳モデル（動物の対応づけ）は入れない。三層の図の直後に、
現行と同じ趣旨の注意書きを置き、`attention.html` を参照する
（`attention.html` は未作成なので、この段階では参照先を書かず「第3部で扱う」とだけ書く）。

**コラム誘導:** なし

- [ ] **Step 1: 既存の図と表を取り出す**

```bash
cd ~/Claude/brain
python3 - <<'EOF'
import re
s = open('docs/legacy/2026-09-14-single-page.html', encoding='utf-8').read()
for key, out in [('f1L-t', '/tmp/fig-layers.html'), ('f1b-t', '/tmp/fig-brain.html')]:
    m = re.search(r'<figure class="fig">\s*<svg[^>]*aria-labelledby="%s".*?</figure>' % key, s, re.S)
    open(out, 'w', encoding='utf-8').write(m.group(0))
    print(key, len(m.group(0)))
m = re.search(r'<div class="tbl-scroll">.*?</div>', s, re.S)
open('/tmp/tbl-parts.html', 'w', encoding='utf-8').write(m.group(0))
print('table', len(m.group(0)))
EOF
```

- [ ] **Step 2: `anatomy.html` を書く**

本文3,500〜4,500字。既存の第1章「部位」節の文章を土台に、左右半球の節を新規に足す
（半球の役割分担は俗説が多い領域なので、「言語は多くの人で左優位」「分離脳研究」までにとどめ、
「右脳人間／左脳人間」は明確に否定する）。

- [ ] **Step 3: `cells.html` に next を足す**

`cells.html` の `.pager` に `<a class="next" href="anatomy.html">` を追加（prev は無し）。

- [ ] **Step 4: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 3 pages checked`

- [ ] **Step 5: ブラウザで確認する**

`anatomy.html` を 780px / 375px、ライト／ダークで目視。
特に四葉の琥珀トーン（`--l0`〜`--l4`）がダークモードで潰れていないかを見る。

- [ ] **Step 6: コミット**

```bash
cd ~/Claude/brain
git add anatomy.html cells.html index.html
git commit -m "$(printf '第1部02「脳の地図」を追加\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 6: 03 つながりが機能をつくる

**Files:**
- Create: `networks.html`
- Modify: `anatomy.html`（pager に next）、`index.html`（サイトマップ）

**Interfaces:**
- Consumes: Task 2 の `.fig .box .s-e .lb .te`
- Produces: `networks.html` — `signal.html` の prev、`dmn.html` から参照される

**見出し:**
- リード文
- `h2` 灰白質と白質
- `h2` 部位ではなく、つながり
- `h2` 三つのネットワーク
- `h2` 使われた結合が、残る
- `h2` 燃費のわるい臓器

**図3点:**
- 新規「灰白質と白質」— 皮質の薄い層と、その内側を走る軸索の束。
  `viewBox="0 0 640 280"`、`<title id="fwm-t">灰白質と白質</title>`
- 既存「三つのネットワーク」（`f1c-t`）
- 新規「可塑性」— 使われた結合が太くなり、使われない結合が消える前後の対比。
  `viewBox="0 0 640 260"`、`<title id="fplast-t">使われた結合が残る</title>`

**コラム誘導:** 「三つのネットワーク」節の末尾に `dmn.html` へのカード。
ただし `dmn.html` は Task 19 で作るので、**このタスクではカードを置かない**。
Task 19 で `networks.html` に追記する。

- [ ] **Step 1: 既存の図を取り出す**

```bash
cd ~/Claude/brain
python3 - <<'EOF'
import re
s = open('docs/legacy/2026-09-14-single-page.html', encoding='utf-8').read()
m = re.search(r'<figure class="fig">\s*<svg[^>]*aria-labelledby="f1c-t".*?</figure>', s, re.S)
open('/tmp/fig-networks.html', 'w', encoding='utf-8').write(m.group(0))
print('extracted', len(m.group(0)))
EOF
```

- [ ] **Step 2: `networks.html` を書く**

本文3,000〜4,000字。既存の第1章「ネットワーク」「代謝と可塑性」節を土台に、
灰白質／白質の節を新規に足す。

- [ ] **Step 3: `anatomy.html` に next、`networks.html` に prev を足す**

- [ ] **Step 4: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 4 pages checked`

- [ ] **Step 5: ブラウザで確認する**

- [ ] **Step 6: コミット**

```bash
cd ~/Claude/brain
git add networks.html anatomy.html index.html
git commit -m "$(printf '第1部03「つながりが機能をつくる」を追加\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 7: リリース① 第1部を公開

**Files:**
- Modify: `index.html`（第1部カードを有効化。第2部以降は「準備中」のまま）

- [ ] **Step 1: 全ページのサイトマップを揃える**

`index.html` `cells.html` `anatomy.html` `networks.html` の4ファイルすべてに、
同じ第1部グループのサイトマップが入っていることを確認する。

```bash
cd ~/Claude/brain
for f in index cells anatomy networks; do
  printf '%-10s %s\n' "$f" "$(grep -c 'sitemap' $f.html)"
done
```
Expected: 各ファイルで1以上

- [ ] **Step 2: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 4 pages checked`

- [ ] **Step 3: 375px でリンク切れと横スクロールを確認する**

ローカルサーバを立て、4ページすべてを 375px 幅・ライト／ダークで開き、
`document.documentElement.scrollWidth > innerWidth` が `false` であることを確認する。

- [ ] **Step 4: プッシュしてビルドを待つ**

```bash
cd ~/Claude/brain
git push origin main
for i in $(seq 1 12); do
  st=$(gh api repos/doesman1227/brain/pages/builds/latest --jq .status)
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://m-note.uk/brain/cells.html")
  echo "[$i] build=$st cells=$code"
  [ "$st" = "built" ] && [ "$code" = "200" ] && break
  sleep 25
done
```
Expected: `build=built cells=200`

- [ ] **Step 5: 本番で確認する**

`https://m-note.uk/brain/` を開き、第1部の3ページを順に辿れること、
`← m-note トップ` が効くことを確認する。

---

## Task 8: 04 電気で走る

**Files:**
- Create: `signal.html`
- Modify: `networks.html`（pager に next）、全既存ページのサイトマップに第2部グループを追加

**Interfaces:**
- Consumes: Task 2 の `.fig .s-i .s-e .s-f .box .lb .ti .te`
- Produces: `signal.html` — `synapse.html` の prev

**見出し:**
- リード文
- `h2` 静止しているときも、電池である
- `h2` 閾値を越えると、一気に立ち上がる
- `h2` 全か無か
- `h2` 髄鞘が、速さを生む
- `h2` 強さは、頻度で伝える

**図4点（すべて新規）:**
- 「静止電位と活動電位」— 横軸ミリ秒、縦軸ミリボルトの折れ線。−70mV の静止、−55mV の閾値、
  +40mV のピーク、過分極からの復帰。`viewBox="0 0 640 300"`、`<title id="fap-t">活動電位の経過</title>`
- 「閾値と全か無かの法則」— 閾値に届かない入力は何も起きず、届いた入力はすべて同じ高さの
  スパイクになる対比。`viewBox="0 0 640 260"`、`<title id="fthr-t">閾値と全か無かの法則</title>`
- 「髄鞘と跳躍伝導」— 髄鞘に覆われた軸索とランビエ絞輪、信号が絞輪を飛ぶ様子。
  `viewBox="0 0 640 220"`、`<title id="fmye-t">髄鞘と跳躍伝導</title>`
- 「発火頻度による符号化」— 弱い刺激はまばらなスパイク列、強い刺激は密なスパイク列。
  `viewBox="0 0 640 240"`、`<title id="frate-t">発火頻度で強さを伝える</title>`

**コラム誘導:** なし

- [ ] **Step 1: STRUCTURE を確認する**

`tools/check.py` の `STRUCTURE["第2部 仕組み"]` に `signal` が既に入っていることを確認する
（Task 1 で全ページ分を書いてある）。

- [ ] **Step 2: `signal.html` を書く**

本文4,000〜5,000字。イオン（ナトリウム・カリウム）、ポンプとチャネル、脱分極、再分極、
不応期、髄鞘と多発性硬化症への一言、発火頻度符号化。
`cells.html` の希突起膠細胞の話を受けて髄鞘につなぐ。

- [ ] **Step 3: 全ページのサイトマップに第2部グループを追加する**

この時点で存在するのは `signal.html` のみなので、第2部グループには
`<li><a href="signal.html">04 電気で走る</a></li>` の1行だけを置く。
対象ファイル: `index.html` `cells.html` `anatomy.html` `networks.html` `signal.html`

- [ ] **Step 4: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 5 pages checked`

- [ ] **Step 5: ブラウザで確認する**

活動電位のグラフの目盛りと軸ラベルが 375px でも潰れないことを特に確認する。

- [ ] **Step 6: コミット**

```bash
cd ~/Claude/brain
git add signal.html index.html cells.html anatomy.html networks.html
git commit -m "$(printf '第2部04「電気で走る」を追加\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 9: 05 すきまを渡る

**Files:**
- Create: `synapse.html`
- Modify: `signal.html`（next）、全既存ページのサイトマップ

**見出し:**
- リード文
- `h2` 電気から化学へ
- `h2` 受け取る側で、何が起きるか
- `h2` 押す入力と、引く入力
- `h2` 足し合わせて、閾値を越えるか
- `h2` 使うほど、通りやすくなる

**図3点（すべて新規）:**
- 「シナプスの拡大図」— 小胞、開口放出、受容体、再取り込み、分解。
  `viewBox="0 0 640 320"`、`<title id="fsyn-t">シナプスで起きていること</title>`
- 「興奮性と抑制性の統合」— 複数の入力が細胞体に集まり、合計が閾値を越えるかどうか。
  `viewBox="0 0 640 280"`、`<title id="fsum-t">入力の足し合わせ</title>`
- 「シナプス強度の変化」— 同時に発火した結合が強まる（LTP）／使われない結合が弱まる（LTD）。
  `viewBox="0 0 640 240"`、`<title id="fltp-t">シナプス強度は変わる</title>`

**コラム誘導:** なし

- [ ] **Step 1: `synapse.html` を書く**

本文4,000〜5,000字。`signal.html` の活動電位が軸索末端に届いたところから始める。
興奮性（グルタミン酸）と抑制性（GABA）、時間的加重と空間的加重、閾値、
ヘッブ則と LTP/LTD、`networks.html` の可塑性との接続。

- [ ] **Step 2: pager とサイトマップを更新する**

- [ ] **Step 3: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 6 pages checked`

- [ ] **Step 4: ブラウザで確認する**

- [ ] **Step 5: コミット**

```bash
cd ~/Claude/brain
git add synapse.html signal.html index.html cells.html anatomy.html networks.html
git commit -m "$(printf '第2部05「すきまを渡る」を追加\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 10: 06 神経伝達物質

**Files:**
- Create: `chemicals.html`
- Modify: `synapse.html`（next）、全既存ページのサイトマップ

**見出し:**
- リード文
- `h2` 主な伝達物質と、その役回り
- `h2` ドーパミンは「快楽物質」ではない
- `h2` ホルモンとは、何が違うのか
- `h2` 薬は、どこに効いているのか

**図3点（すべて新規）:**
- 「主な神経伝達物質」— グルタミン酸・GABA・ドーパミン・セロトニン・アセチルコリン・
  ノルアドレナリンを、興奮性／抑制性／調節性の3群に分けた一覧。
  `viewBox="0 0 640 340"`、`<title id="fnt-t">主な神経伝達物質</title>`
- 「報酬予測誤差」— 予測どおり／予測より良い／予測より悪い の3条件でドーパミン発火が
  どう変わるかの3段グラフ。`viewBox="0 0 640 300"`、`<title id="frpe-t">報酬予測誤差とドーパミン</title>`
- 「神経伝達物質とホルモン」— シナプスという近距離・高速の伝達と、血流に乗る遠距離・低速の
  伝達の対比。`viewBox="0 0 640 260"`、`<title id="fhorm-t">近くに速く、遠くにゆっくり</title>`

**コラム誘導:** 「ドーパミンは快楽物質ではない」節の末尾に `prediction.html` へのカード。
ただし `prediction.html` は Task 18 で作るので、**このタスクでは置かない**。Task 18 で追記する。

- [ ] **Step 1: `chemicals.html` を書く**

本文4,000〜5,000字。ドーパミンの節が要。報酬そのものではなく「予測との差」に応答すること、
それが学習信号になっていること、依存や動機づけとの関係。
セロトニンと「幸せホルモン」という通俗的な呼び方の限界にも触れる。

- [ ] **Step 2: pager とサイトマップを更新する**

- [ ] **Step 3: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 7 pages checked`

- [ ] **Step 4: ブラウザで確認する**

- [ ] **Step 5: コミット**

```bash
cd ~/Claude/brain
git add chemicals.html synapse.html index.html cells.html anatomy.html networks.html signal.html
git commit -m "$(printf '第2部06「神経伝達物質」を追加\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 11: リリース② 第2部を公開

- [ ] **Step 1: index の第2部カードを有効化する**

- [ ] **Step 2: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 7 pages checked`

- [ ] **Step 3: 7ページすべてを 375px・ダークで目視する**

- [ ] **Step 4: プッシュしてビルドを待つ**

```bash
cd ~/Claude/brain
git push origin main
for i in $(seq 1 12); do
  st=$(gh api repos/doesman1227/brain/pages/builds/latest --jq .status)
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://m-note.uk/brain/chemicals.html")
  echo "[$i] build=$st chemicals=$code"
  [ "$st" = "built" ] && [ "$code" = "200" ] && break
  sleep 25
done
```
Expected: `build=built chemicals=200`

---

## Task 12: 07 感じる

**Files:**
- Create: `perceive.html`
- Modify: `chemicals.html`（next）、全既存ページのサイトマップ

**見出し:**
- リード文
- `h2` 受容器から、皮質まで
- `h2` 色・形・動きは、別々に処理される
- `h2` 嗅覚だけが、違う道を通る
- `h2` 日常に出るところ — 見ているのに、見ていない

**図2点:**
- 新規「感覚経路」— 受容器 → 視床 → 一次感覚野 → 連合野。嗅覚だけが視床を通らない分岐を朱で。
  `viewBox="0 0 640 300"`、`<title id="fpath-t">感覚が皮質に届くまで</title>`
- 既存「視野／注意／記憶の三層」（`f3-t`）

**コラム誘導:** 末尾に `prediction.html` へのカード（Task 18 で追記）。

- [ ] **Step 1: 既存の図を取り出す**

```bash
cd ~/Claude/brain
python3 - <<'EOF'
import re
s = open('docs/legacy/2026-09-14-single-page.html', encoding='utf-8').read()
m = re.search(r'<figure class="fig">\s*<svg[^>]*aria-labelledby="f3-t".*?</figure>', s, re.S)
open('/tmp/fig-three-layers.html', 'w', encoding='utf-8').write(m.group(0))
print('extracted', len(m.group(0)))
EOF
```

- [ ] **Step 2: `perceive.html` を書く**

本文3,500〜4,500字。既存の第3章と第4章（嗅覚の別経路）の一部を土台にする。
日常への着地は、非注意性盲目（見えているのに気づかない）、錯視、
スマホを見ながらの会話が入ってこないこと。

- [ ] **Step 3: pager とサイトマップを更新する**

- [ ] **Step 4: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 8 pages checked`

- [ ] **Step 5: ブラウザで確認する**

- [ ] **Step 6: コミット**

```bash
cd ~/Claude/brain
git add perceive.html chemicals.html index.html cells.html anatomy.html networks.html signal.html synapse.html
git commit -m "$(printf '第3部07「感じる」を追加\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 13: 08 覚える・思い出す

**Files:**
- Create: `remember.html`
- Modify: `perceive.html`（next）、全既存ページのサイトマップ

**見出し:**
- リード文
- `h2` 記憶は、一種類ではない
- `h2` 海馬が索引をつくる
- `h2` 眠っているあいだに、固定される
- `h2` 思い出すとは、作り直すこと
- `h2` 日常に出るところ — 覚えたいなら、どうするか

**図3点:**
- 新規「記憶の種類」— 短期／長期、長期を陳述記憶（エピソード記憶・意味記憶）と
  非陳述記憶（手続き記憶・プライミング）に分ける樹形図。
  `viewBox="0 0 640 320"`、`<title id="fmem-t">記憶の分類</title>`
- 新規「睡眠中の固定化」— 睡眠段階の帯グラフと、海馬から皮質への転送。
  `viewBox="0 0 640 280"`、`<title id="fsleep-t">眠っているあいだの固定化</title>`
- 既存「記憶の再構成」（`f4-t`）

**注意:** 上の樹形図の説明で日本語以外の文字を混入させないこと。
陳述記憶の下位は「エピソード記憶」「意味記憶」と書く。

**コラム誘導:** なし

- [ ] **Step 1: 既存の図を取り出す**

```bash
cd ~/Claude/brain
python3 - <<'EOF'
import re
s = open('docs/legacy/2026-09-14-single-page.html', encoding='utf-8').read()
m = re.search(r'<figure class="fig">\s*<svg[^>]*aria-labelledby="f4-t".*?</figure>', s, re.S)
open('/tmp/fig-reconstruct.html', 'w', encoding='utf-8').write(m.group(0))
print('extracted', len(m.group(0)))
EOF
```

- [ ] **Step 2: `remember.html` を書く**

本文4,000〜5,000字。既存の第4章を土台に、記憶の分類と睡眠の節を新規に足す。
日常への着地は、分散学習と想起練習、寝る前の詰め込みの是非、睡眠不足の影響。

- [ ] **Step 3: pager とサイトマップを更新する**

- [ ] **Step 4: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 9 pages checked`

- [ ] **Step 5: ブラウザで確認する**

- [ ] **Step 6: コミット**

```bash
cd ~/Claude/brain
git add remember.html perceive.html index.html cells.html anatomy.html networks.html signal.html synapse.html chemicals.html
git commit -m "$(printf '第3部08「覚える・思い出す」を追加\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 14: 09 注意と情動

**Files:**
- Create: `attention.html`
- Modify: `remember.html`（next）、`anatomy.html`（三層の注意書きから `attention.html` へリンク）、全既存ページのサイトマップ

**見出し:**
- リード文
- `h2` 注意は、切り替えである
- `h2` 理性の脳は、なかった
- `h2` 感情は、意味をつける
- `h2` 日常に出るところ — 集中が切れる、ストレスが残る

**図3点:**
- 新規「注意の切り替え」— 実行系とデフォルト・モードのあいだをサリエンスが切り替える様子。
  `viewBox="0 0 640 260"`、`<title id="fswitch-t">注意の切り替え</title>`
- 既存「二層構造の否定→網」（`f5-t`）
- 既存「感情のチェーン」（`f5b-t`）

**コラム誘導:** 末尾に `dmn.html` へのカード（Task 19 で追記）。

- [ ] **Step 1: 既存の図を取り出す**

```bash
cd ~/Claude/brain
python3 - <<'EOF'
import re
s = open('docs/legacy/2026-09-14-single-page.html', encoding='utf-8').read()
for key, out in [('f5-t', '/tmp/fig-twolayer.html'), ('f5b-t', '/tmp/fig-emotion.html')]:
    m = re.search(r'<figure class="fig">\s*<svg[^>]*aria-labelledby="%s".*?</figure>' % key, s, re.S)
    open(out, 'w', encoding='utf-8').write(m.group(0))
    print(key, len(m.group(0)))
EOF
```

- [ ] **Step 2: `attention.html` を書く**

本文4,000〜5,000字。既存の第5章をほぼそのまま土台にし、注意の節を新規に足す。
日常への着地は、マルチタスクの切り替えコスト、通知の割り込み、
ストレス反応が残ること、反芻。`../mindfulness/` と `../cbt/` へのリンクをここに置く。

- [ ] **Step 3: `anatomy.html` の注意書きを更新する**

「その話は第3部で扱う」と書いてあった箇所を、`attention.html` へのリンクに差し替える。

- [ ] **Step 4: pager とサイトマップを更新する**

- [ ] **Step 5: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 10 pages checked`

- [ ] **Step 6: ブラウザで確認する**

- [ ] **Step 7: コミット**

```bash
cd ~/Claude/brain
git add attention.html remember.html anatomy.html index.html cells.html networks.html signal.html synapse.html chemicals.html perceive.html
git commit -m "$(printf '第3部09「注意と情動」を追加\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 15: 10 決める・動く

**Files:**
- Create: `decide.html`
- Modify: `attention.html`（next）、全既存ページのサイトマップ

**見出し:**
- リード文
- `h2` 前頭前野は、抑える役でもある
- `h2` 大脳基底核と、習慣のループ
- `h2` 指令が、筋肉に届くまで
- `h2` 日常に出るところ — 先延ばしと、習慣づくり

**図3点（すべて新規）:**
- 「前頭前野による抑制」— 誘惑への反応を前頭前野が抑える経路と、
  疲労・睡眠不足でその抑制が弱まる様子。`viewBox="0 0 640 280"`、
  `<title id="fpfc-t">抑える働きと、その弱まり</title>`
- 「習慣のループ」— きっかけ → 行動 → 報酬 → 強化 の循環と、
  繰り返すほど前頭前野の関与が減って基底核に移る様子。
  `viewBox="0 0 640 300"`、`<title id="fhabit-t">習慣のループ</title>`
- 「運動指令の流れ」— 運動野 → 脊髄 → 筋、小脳と基底核による調整。
  `viewBox="0 0 640 300"`、`<title id="fmotor-t">指令が筋肉に届くまで</title>`

**コラム誘導:** 末尾に `self-model.html` へのカード（Task 20 で追記）。

- [ ] **Step 1: `decide.html` を書く**

本文4,000〜5,000字。日常への着地は、先延ばしを意志の弱さではなく抑制資源の問題として見ること、
環境を変えるほうが効くこと、習慣は繰り返しで基底核に移ること。

- [ ] **Step 2: pager とサイトマップを更新する**

- [ ] **Step 3: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 11 pages checked`

- [ ] **Step 4: ブラウザで確認する**

- [ ] **Step 5: コミット**

```bash
cd ~/Claude/brain
git add decide.html attention.html index.html cells.html anatomy.html networks.html signal.html synapse.html chemicals.html perceive.html remember.html
git commit -m "$(printf '第3部10「決める・動く」を追加\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 16: リリース③ 第3部を公開

- [ ] **Step 1: index の第3部カードを有効化する**

- [ ] **Step 2: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 11 pages checked`

- [ ] **Step 3: 11ページすべてを 375px・ダークで目視する**

- [ ] **Step 4: プッシュしてビルドを待つ**

```bash
cd ~/Claude/brain
git push origin main
for i in $(seq 1 12); do
  st=$(gh api repos/doesman1227/brain/pages/builds/latest --jq .status)
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://m-note.uk/brain/decide.html")
  echo "[$i] build=$st decide=$code"
  [ "$st" = "built" ] && [ "$code" = "200" ] && break
  sleep 25
done
```
Expected: `build=built decide=200`

---

## Task 17: コラム一覧

**Files:**
- Create: `columns.html`
- Modify: `index.html`（コラムカードを有効化）、全既存ページのサイトマップにコラムグループを追加

**Interfaces:**
- Produces: `columns.html` — 全コラムページのパンくずのリンク先

**構成:**
- 共通マークアップ
- パンくず（`脳の仕組み › コラム`）
- `.col-label` に `COLUMN`
- `h1` コラム
- リード文: 本編が「何がどう動いているか」なのに対し、コラムは「それをどう捉えるか」であること。
  読み飛ばしても本編は成立すること。
- 8本のカード（`.colcard` を並べる）。**この時点では8本とも未作成**なので、
  カードは `<a>` にせず `<div>` で「準備中」と出す。Task 18〜21 で1本ずつ `<a>` に変える。
- サイトマップ、フッター

- [ ] **Step 1: `columns.html` を書く**

- [ ] **Step 2: 全ページのサイトマップにコラムグループを追加する**

この時点ではコラムグループに `<li><a href="columns.html">コラム一覧</a></li>` の1行だけ。

- [ ] **Step 3: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 12 pages checked`

- [ ] **Step 4: コミット**

```bash
cd ~/Claude/brain
git add columns.html index.html cells.html anatomy.html networks.html signal.html synapse.html chemicals.html perceive.html remember.html attention.html decide.html
git commit -m "$(printf 'コラム一覧ページを追加\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 18: コラム 予測符号化・自由エネルギー原理

**Files:**
- Create: `prediction.html` `free-energy.html`
- Modify: `columns.html`（2本を `<a>` に）、`chemicals.html` `perceive.html`（コラム誘導カードを追加）、全ページのサイトマップ

**コラムページの共通構造:** 本編と同じだが、`.part-label` の代わりに `.col-label`（`COLUMN`）を使い、
`.pager` は置かず、末尾に「コラム一覧へ戻る」リンクと「関連する本編ページ」リンクを置く。

**`prediction.html`:**
- `h1` 脳は誤差だけを見ている
- 既存「予測と誤差のループ」（`f2-t`）を移す
- 本文は既存の第2章をほぼそのまま。末尾に `.q`（残る問い）ブロックも移す
- 関連: `perceive.html` `chemicals.html`

**`free-energy.html`:**
- `h1` 自由エネルギー原理
- 新規図「予測誤差を減らす二つの道」— 予測を変える（知覚）か、世界を変える（行動）か。
  `viewBox="0 0 640 280"`、`<title id="ffep-t">誤差を減らす二つの道</title>`
- 本文2,500〜3,500字。予測符号化を一段抽象化した枠組みであること、
  「生きているとは、予測誤差を小さく保ち続けることだ」という主張、
  そして仮説であって決着していないことを明記する
- 関連: `prediction.html`

- [ ] **Step 1: 既存の図と本文を取り出す**

```bash
cd ~/Claude/brain
python3 - <<'EOF'
import re
s = open('docs/legacy/2026-09-14-single-page.html', encoding='utf-8').read()
m = re.search(r'<section class="ch" id="ch2">.*?</section>', s, re.S)
open('/tmp/ch2.html', 'w', encoding='utf-8').write(m.group(0))
print('ch2', len(m.group(0)))
EOF
```

- [ ] **Step 2: 2ページを書く**

- [ ] **Step 3: 本編にコラム誘導カードを足す**

`chemicals.html` の「ドーパミンは快楽物質ではない」節の末尾と、
`perceive.html` の末尾に `.colcard` を置く。

- [ ] **Step 4: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 14 pages checked`

- [ ] **Step 5: ブラウザで確認する**

コラムページが本編と見分けられること（`COLUMN` ラベルが朱、地の色が違う）を確認する。

- [ ] **Step 6: コミット**

```bash
cd ~/Claude/brain
git add prediction.html free-energy.html columns.html chemicals.html perceive.html index.html cells.html anatomy.html networks.html signal.html synapse.html remember.html attention.html decide.html
git commit -m "$(printf 'コラム「予測符号化」「自由エネルギー原理」を追加\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 19: コラム 千の脳理論・デフォルトモードネットワーク

**Files:**
- Create: `thousand-brains.html` `dmn.html`
- Modify: `columns.html`、`networks.html` `attention.html`（コラム誘導カードを追加）、全ページのサイトマップ

**`thousand-brains.html`:**
- `h1` 千の脳と、座標系
- 既存「千の脳（皮質コラム）」（`f6-t`）と「地図と、自分を含む世界モデル」（`f6b-t`）を移す
- 本文は既存の第6章をそのまま。`.q` ブロックも移す
- 関連: `networks.html` `self-model.html`

**`dmn.html`:**
- `h1` 何もしない時間が、整理している
- 既存「CEN/DMN と情報入力」を移す。**移すときに id を `f7-t` から `fdmn-t` に変える**
  （現行ページで `f7-t` が「幅を持つ『今』」と重複しているため）。
  `<title id="fdmn-t">` と `aria-labelledby="fdmn-t"` の両方を書き換える
- 本文は既存の第9章をそのまま。`.q` ブロックも移す。`../mindfulness/` へのリンクを維持
- 関連: `networks.html` `attention.html`

- [ ] **Step 1: 既存の図と本文を取り出す**

```bash
cd ~/Claude/brain
python3 - <<'EOF'
import re
s = open('docs/legacy/2026-09-14-single-page.html', encoding='utf-8').read()
for cid in ['ch6', 'ch9']:
    m = re.search(r'<section class="ch" id="%s">.*?</section>' % cid, s, re.S)
    open('/tmp/%s.html' % cid, 'w', encoding='utf-8').write(m.group(0))
    print(cid, len(m.group(0)))
EOF
```

- [ ] **Step 2: 2ページを書く**

- [ ] **Step 3: 本編にコラム誘導カードを足す**

`networks.html` の「三つのネットワーク」節の末尾に `dmn.html` へのカード。
`attention.html` の末尾に `dmn.html` へのカード。

- [ ] **Step 4: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 16 pages checked`

- [ ] **Step 5: ブラウザで確認する**

- [ ] **Step 6: コミット**

```bash
cd ~/Claude/brain
git add thousand-brains.html dmn.html columns.html networks.html attention.html index.html cells.html anatomy.html signal.html synapse.html chemicals.html perceive.html remember.html decide.html prediction.html free-energy.html
git commit -m "$(printf 'コラム「千の脳と座標系」「デフォルト・モード・ネットワーク」を追加\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 20: コラム 自己モデル・意識の理論

**Files:**
- Create: `self-model.html` `consciousness.html`
- Modify: `columns.html`、`decide.html`（コラム誘導カード）、全ページのサイトマップ

**`self-model.html`:**
- `h1` 自己モデルと、自己同一性
- 既存「幅を持つ『今』」を移す。**移すときに id を `f7-t` から `fnow-t` に変える**
  （`dmn.html` の図と重複しているため）。
  `<title id="fnow-t">` と `aria-labelledby="fnow-t"` の両方を書き換える
- 本文は既存の第7章と第8章を統合。自己モデルと自己同一性の区別、機能的自由意志まで
- 関連: `decide.html` `anatta.html`

**`consciousness.html`:**
- `h1` 意識の理論と、ハードプロブレム
- 新規図「意識の理論の比較」— グローバル・ワークスペース理論、統合情報理論、予測処理、
  千の脳理論が、それぞれ何を説明しようとしているかの対比表を図にしたもの。
  `viewBox="0 0 640 340"`、`<title id="fcons-t">意識をめぐる理論</title>`
- 本文は既存の第10章前半。情報処理と主観的体験を分けること、どの理論も意識そのものは
  説明しきっていないこと
- 関連: `self-model.html` `brain-and-ai.html`

- [ ] **Step 1: 既存の図と本文を取り出す**

```bash
cd ~/Claude/brain
python3 - <<'EOF'
import re
s = open('docs/legacy/2026-09-14-single-page.html', encoding='utf-8').read()
for cid in ['ch7', 'ch8', 'ch10']:
    m = re.search(r'<section class="ch" id="%s">.*?</section>' % cid, s, re.S)
    open('/tmp/%s.html' % cid, 'w', encoding='utf-8').write(m.group(0))
    print(cid, len(m.group(0)))
EOF
```

- [ ] **Step 2: 2ページを書く**

- [ ] **Step 3: `decide.html` にコラム誘導カードを足す**

- [ ] **Step 4: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 18 pages checked`

- [ ] **Step 5: ブラウザで確認する**

- [ ] **Step 6: コミット**

```bash
cd ~/Claude/brain
git add self-model.html consciousness.html columns.html decide.html index.html cells.html anatomy.html networks.html signal.html synapse.html chemicals.html perceive.html remember.html attention.html prediction.html free-energy.html thousand-brains.html dmn.html
git commit -m "$(printf 'コラム「自己モデルと自己同一性」「意識の理論」を追加\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 21: コラム 無我・脳とAI

**Files:**
- Create: `anatta.html` `brain-and-ai.html`
- Modify: `columns.html`、全ページのサイトマップ

**`anatta.html`:**
- `h1` 無我と、プロセスとしての自己
- 既存「渦」（`docs/legacy` では `aria-labelledby="f8-t"`）を移す。
  移った先では単独なので id はそのままでよいが、読みやすさのため `fvortex-t` に振り直す
- 本文は既存の第8章の渦と無我の節。「脳科学＝仏教」とは言わない線引きを維持
- `../early-buddhism/` へのリンクを置く
- 関連: `self-model.html`

**`brain-and-ai.html`:**
- `h1` 脳とAI — 構造は似ているのか
- 新規図「人間の処理とAIの処理」— 入力から出力までの流れを並べ、
  似ている部分（内部状態を経て出力が出る）と、確かめられていない部分（内側で経験があるか）を
  分けて示す。`viewBox="0 0 640 320"`、`<title id="fai-t">似ているところと、分からないところ</title>`
- 本文は既存の第10章後半（AIとの相似、コピー問題）。
  情報的な同一性と主観的な同一性は別であること
- 関連: `consciousness.html`

- [ ] **Step 1: 図を取り出す**

```bash
cd ~/Claude/brain
python3 - <<'EOF'
import re
s = open('docs/legacy/2026-09-14-single-page.html', encoding='utf-8').read()
m = re.search(r'<figure class="fig">\s*<svg[^>]*aria-labelledby="f8-t".*?</figure>', s, re.S)
open('/tmp/fig-vortex.html', 'w', encoding='utf-8').write(m.group(0))
print('extracted', len(m.group(0)))
EOF
```

- [ ] **Step 2: 2ページを書く**

- [ ] **Step 3: `columns.html` の残り2本を `<a>` にする**

- [ ] **Step 4: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 20 pages checked`

- [ ] **Step 5: ブラウザで確認する**

- [ ] **Step 6: コミット**

```bash
cd ~/Claude/brain
git add anatta.html brain-and-ai.html columns.html index.html cells.html anatomy.html networks.html signal.html synapse.html chemicals.html perceive.html remember.html attention.html decide.html prediction.html free-energy.html thousand-brains.html dmn.html self-model.html consciousness.html
git commit -m "$(printf 'コラム「無我とプロセスとしての自己」「脳とAI」を追加\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
```

---

## Task 22: リリース④ 全体公開とハブの更新

**Files:**
- Modify: `~/Claude/hub/index.html`（説明文を新しい射程に合わせる）

- [ ] **Step 1: 全ページのサイトマップが20ページ分揃っていることを確認する**

```bash
cd ~/Claude/brain
for f in *.html; do
  n=$(grep -o 'class="sitemap"' "$f" | wc -l | tr -d ' ')
  links=$(sed -n '/class="sitemap"/,/<\/nav>/p' "$f" | grep -c '<li>')
  printf '%-22s sitemap=%s links=%s\n' "$f" "$n" "$links"
done
```
Expected: 全ファイルで `sitemap=1`、`links` が同じ数

- [ ] **Step 2: 検査**

Run: `cd ~/Claude/brain && python3 tools/check.py`
Expected: `OK: 20 pages checked`

- [ ] **Step 3: プッシュしてビルドを待つ**

```bash
cd ~/Claude/brain
git push origin main
for i in $(seq 1 12); do
  st=$(gh api repos/doesman1227/brain/pages/builds/latest --jq .status)
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://m-note.uk/brain/brain-and-ai.html")
  echo "[$i] build=$st ai=$code"
  [ "$st" = "built" ] && [ "$code" = "200" ] && break
  sleep 25
done
```

- [ ] **Step 4: 本番の全20ページが 200 を返すことを確認する**

```bash
for p in index cells anatomy networks signal synapse chemicals perceive remember attention decide columns prediction free-energy thousand-brains dmn self-model consciousness anatta brain-and-ai; do
  printf '%-18s %s\n' "$p" "$(curl -s -o /dev/null -w '%{http_code}' https://m-note.uk/brain/$p.html)"
done
```
Expected: 全て 200

- [ ] **Step 5: ハブの説明文を更新する**

```bash
cd ~/Claude/hub && git pull -q
```

`~/Claude/hub/index.html` の `brain/` 行の `.desc` を、複数ページ構成に合わせて書き換える。
現在の文（脳は世界をそのまま受け取ってはいない…）を、
「脳が何でできていて、どう動き、それが日々の活動にどうつながるか。理論はコラムに。」の趣旨に変える。

```bash
cd ~/Claude/hub
git add index.html
git commit -m "$(printf '脳の仕組みセクションの説明を複数ページ構成に合わせて更新\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
git push origin HEAD
```

- [ ] **Step 6: 旧仕様書に後継を明記する**

`docs/superpowers/specs/2026-09-13-brain-design.md` の先頭に1行足す。

```markdown
> この仕様は 2026-09-15 の複数ページ化設計（`2026-09-15-brain-multipage-design.md`）に置き換えられた。
```

```bash
cd ~/Claude/brain
git add docs/superpowers/specs/2026-09-13-brain-design.md
git commit -m "$(printf '旧仕様書に後継を明記\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>')"
git push origin main
```
