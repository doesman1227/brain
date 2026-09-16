#!/usr/bin/env python3
"""brain セクションの静的検査。依存なし。"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# サイトの正式な構造。ページを増やすときはここに追記してから作る。
STRUCTURE = {
    "第1部 基本":   ["cells", "anatomy", "networks"],
    "第2部 仕組み": ["signal", "synapse", "chemicals"],
    "第3部 はたらき": ["perceive", "remember", "attention", "decide"],
    "コラム": ["prediction", "free-energy", "thousand-brains", "intelligence",
               "dmn", "self-model", "consciousness", "anatta", "brain-and-ai"],
}
HUBS = ["index", "columns"]

DISCLAIMER = ("専門家ではない個人が調べ、考えたことをまとめた個人的なまとめです。"
              "内容の正確性を保証するものではありません。")

problems = []


def err(page, msg):
    problems.append("%s: %s" % (page, msg))


def load_css_vars(root):
    """css/style.css で定義されているカスタムプロパティ名(--xxx)の集合を返す。
    ファイルが無ければ None を返す（呼び出し側は検査をスキップする）。"""
    css_path = os.path.join(root, "css", "style.css")
    if not os.path.exists(css_path):
        return None
    with open(css_path, encoding="utf-8") as fh:
        css = fh.read()
    return set(re.findall(r"(--[\w-]+)\s*:", css))


def check(path, name, html, css_vars=None):
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

    # 未定義のCSS変数を参照していないか（style.css が見つかった場合のみ）
    if css_vars is not None:
        used = set(re.findall(r"var\((--[\w-]+)\)", html))
        undefined = sorted(used - css_vars)
        if undefined:
            err(name, "未定義のCSS変数を参照している: %s" % ", ".join(undefined))


def main():
    pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    if not pages:
        print("html が1つもない")
        return 1
    css_vars = load_css_vars(ROOT)
    for f in pages:
        name = f[:-5]
        with open(os.path.join(ROOT, f), encoding="utf-8") as fh:
            check(os.path.join(ROOT, f), name, fh.read(), css_vars)

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
