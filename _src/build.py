# -*- coding: utf-8 -*-
"""
Static-site generator for the Microservices Patterns course.

Reads:  _src/manifest.py, _src/templates/page.html, _src/content/<slug>.html
Writes: <root>/index.html and <root>/{by-pattern,by-category,by-chapter}/*.html

Run:    python _src/build.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # microservices-patterns/
CONTENT_DIR = os.path.join(HERE, "content")
TEMPLATE = os.path.join(HERE, "templates", "page.html")

sys.path.insert(0, HERE)
import manifest as M  # noqa: E402

VIEWS = [("pattern", "by-pattern", "By Pattern"),
         ("category", "by-category", "By Category"),
         ("chapter", "by-chapter", "By Chapter")]
VIEW_DIR = {"pattern": "by-pattern", "category": "by-category", "chapter": "by-chapter"}


# ----------------------------------------------------------------- helpers
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def esc_attr(s):
    return esc(s).replace('"', "&quot;")


def chapter_file(num):
    return "ch%02d.html" % num


def chapter_title(num):
    for n, t, _ in M.CHAPTERS:
        if n == num:
            return t
    return "Chapter %d" % num


def read_template():
    with open(TEMPLATE, encoding="utf-8") as f:
        return f.read()


MISSING = []
def read_partial(slug):
    path = os.path.join(CONTENT_DIR, slug + ".html")
    if not os.path.exists(path):
        MISSING.append(slug)
        return ('<div class="callout callout--warn"><div class="ic">&#9888;</div><div class="body">'
                '<div class="ttl">Content coming soon</div><p>The lesson for '
                '<code>%s</code> has not been authored yet.</p></div></div>' % esc(slug))
    with open(path, encoding="utf-8") as f:
        return f.read()


def shift_headings(html, by=1):
    """Demote h2..h5 by `by` levels (for multi-unit category/chapter pages)."""
    if by <= 0:
        return html
    op = re.sub(r'(<\s*)h([2-5])\b',
                lambda m: m.group(1) + "h" + str(min(6, int(m.group(2)) + by)), html)
    cl = re.sub(r'(</\s*)h([2-5])\b',
                lambda m: m.group(1) + "h" + str(min(6, int(m.group(2)) + by)), op)
    return cl


REF_RE = re.compile(r'href="ref:([a-z0-9-]+)"')
VALID_SLUGS = set(u["slug"] for u in M.UNITS)
BAD_REFS = []
def resolve_refs(html, current_dir, page_slugs):
    def repl(m):
        slug = m.group(1)
        if slug not in VALID_SLUGS:
            BAD_REFS.append(slug)
        if slug in page_slugs:
            return 'href="#sec-%s"' % slug
        if current_dir == "by-pattern":
            tgt = "%s.html" % slug
        elif current_dir == "":
            tgt = "by-pattern/%s.html" % slug
        else:
            tgt = "../by-pattern/%s.html" % slug
        return 'href="%s"' % tgt
    return REF_RE.sub(repl, html)


def rel_prefix(current_dir):
    return "" if current_dir == "" else "../"


def view_tabs(current_dir, active):
    pre = rel_prefix(current_dir)
    out = []
    for key, folder, label in VIEWS:
        href = pre + folder + "/index.html"
        cls = ' class="active"' if key == active else ""
        out.append('<a href="%s"%s><span class="vt-label">%s</span></a>' % (href, cls, label))
    return "\n      ".join(out)


# ----------------------------------------------------------------- sidebars
def sidebar_pattern(active_slug):
    rows = []
    n = {u["slug"]: i + 1 for i, u in enumerate(M.UNITS)}
    for cat_slug, cat_title, _ in M.CATEGORIES:
        units = M.units_in_category(cat_slug)
        if not units:
            continue
        rows.append('<div class="nav-group">%s</div>' % esc(cat_title))
        for u in units:
            cls = ' class="active"' if u["slug"] == active_slug else ""
            rows.append('<a href="%s.html"%s><span class="nidx">%02d</span><span>%s</span></a>'
                        % (u["slug"], cls, n[u["slug"]], esc(u["title"])))
    return "\n      ".join(rows)


def sidebar_category(active_cat):
    rows = []
    for i, (cat_slug, cat_title, _) in enumerate(M.CATEGORIES, 1):
        if not M.units_in_category(cat_slug):
            continue
        cls = ' class="active"' if cat_slug == active_cat else ""
        rows.append('<a href="%s.html"%s><span class="nidx">%02d</span><span>%s</span></a>'
                    % (cat_slug, cls, i, esc(cat_title)))
    return "\n      ".join(rows)


def sidebar_chapter(active_num):
    rows = []
    for num, title, _ in M.CHAPTERS:
        cls = ' class="active"' if num == active_num else ""
        rows.append('<a href="%s"%s><span class="nidx">%02d</span><span>%s</span></a>'
                    % (chapter_file(num), cls, num, esc(title)))
    return "\n      ".join(rows)


# ----------------------------------------------------------------- page render
TPL = None
def render(current_dir, filename, title, desc, page_h1, subtitle, meta_html,
           breadcrumb, content, nav_title, nav_html, tabs_html, prevnext):
    pre = rel_prefix(current_dir)
    html = (TPL
            .replace("{{DESC}}", esc_attr(desc))
            .replace("{{TITLE}}", esc(title))
            .replace("{{ASSET}}", pre + "assets")
            .replace("{{HOME}}", pre + "index.html")
            .replace("{{VIEW_TABS}}", tabs_html)
            .replace("{{NAV_TITLE}}", esc(nav_title))
            .replace("{{NAV}}", nav_html)
            .replace("{{BREADCRUMB}}", breadcrumb)
            .replace("{{META}}", meta_html)
            .replace("{{PAGE_H1}}", esc(page_h1))
            .replace("{{SUBTITLE}}", esc(subtitle))
            .replace("{{CONTENT}}", content)
            .replace("{{PREVNEXT}}", prevnext))
    out_dir = ROOT if current_dir == "" else os.path.join(ROOT, current_dir)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    with open(os.path.join(out_dir, filename), "w", encoding="utf-8") as f:
        f.write(html)


def crumb(current_dir, view_label, view_index, leaf):
    pre = rel_prefix(current_dir)
    return ('<a href="%sindex.html">Home</a><span class="sep">/</span>'
            '<a href="%s">%s</a><span class="sep">/</span>%s'
            % (pre, view_index, esc(view_label), esc(leaf)))


def prevnext_html(prev, nxt):
    """prev/nxt are (href, label) tuples or None."""
    left = ('<a class="prev" href="%s"><span class="pn-dir">&larr; Previous</span>'
            '<span class="pn-ttl">%s</span></a>' % (prev[0], esc(prev[1]))) if prev else "<span></span>"
    right = ('<a class="next" href="%s"><span class="pn-dir">Next &rarr;</span>'
             '<span class="pn-ttl">%s</span></a>' % (nxt[0], esc(nxt[1]))) if nxt else "<span></span>"
    return left + "\n      " + right


def badge(text, kind=""):
    cls = "badge" + ((" " + kind) if kind else "")
    return '<span class="%s">%s</span>' % (cls, text)


def pattern_tags(u):
    return ('<div class="tags">'
            + "".join('<span class="badge badge--pat">%s</span>' % esc(p) for p in u["patterns"])
            + "</div>")


# ----------------------------------------------------------------- by-pattern detail
def build_pattern_pages():
    units = M.UNITS
    for i, u in enumerate(units):
        slug = u["slug"]
        cat_link = "../by-category/%s.html" % u["category"]
        ch_link = "../by-chapter/%s" % chapter_file(u["chapter"])
        meta = " ".join([
            badge(u["difficulty"], "badge--diff badge--%s" % u["difficulty"]),
            '<a class="badge" href="%s">%s</a>' % (cat_link, esc(M.category_title(u["category"]))),
            '<a class="badge badge--ch" href="%s">Chapter %d</a>' % (ch_link, u["chapter"]),
        ])
        body = resolve_refs(read_partial(slug), "by-pattern", {slug})
        content = ('<section class="unit" id="sec-%s">%s\n%s</section>'
                   % (slug, pattern_tags(u), body))
        prev = ("%s.html" % units[i - 1]["slug"], units[i - 1]["title"]) if i > 0 else None
        nxt = ("%s.html" % units[i + 1]["slug"], units[i + 1]["title"]) if i < len(units) - 1 else None
        render("by-pattern", slug + ".html", u["title"], u["summary"], u["title"], u["summary"],
               meta, crumb("by-pattern", "By Pattern", "index.html", u["title"]),
               content, "All Patterns", sidebar_pattern(slug),
               view_tabs("by-pattern", "pattern"), prevnext_html(prev, nxt))


# ----------------------------------------------------------------- by-category
def render_units_stacked(units, current_dir, page_slugs):
    blocks = []
    for u in units:
        body = shift_headings(read_partial(u["slug"]), 1)
        body = resolve_refs(body, current_dir, page_slugs)
        blocks.append('<section class="unit" id="sec-%s"><h2 class="unit-title">%s</h2>%s\n%s</section>'
                      % (u["slug"], esc(u["title"]), pattern_tags(u), body))
    return "\n".join(blocks)


def build_category_pages():
    cats = [(s, t, d) for (s, t, d) in M.CATEGORIES if M.units_in_category(s)]
    for i, (cat_slug, cat_title, cat_desc) in enumerate(cats):
        units = M.units_in_category(cat_slug)
        page_slugs = set(u["slug"] for u in units)
        npat = sum(len(u["patterns"]) for u in units)
        meta = " ".join([
            badge("%d lesson%s" % (len(units), "" if len(units) == 1 else "s")),
            badge("%d patterns" % npat, "badge--diff"),
        ])
        content = render_units_stacked(units, "by-category", page_slugs)
        prev = ("%s.html" % cats[i - 1][0], cats[i - 1][1]) if i > 0 else None
        nxt = ("%s.html" % cats[i + 1][0], cats[i + 1][1]) if i < len(cats) - 1 else None
        render("by-category", cat_slug + ".html", cat_title, cat_desc, cat_title, cat_desc,
               meta, crumb("by-category", "By Category", "index.html", cat_title),
               content, "Categories", sidebar_category(cat_slug),
               view_tabs("by-category", "category"), prevnext_html(prev, nxt))


# ----------------------------------------------------------------- by-chapter
def build_chapter_pages():
    chaps = M.CHAPTERS
    for i, (num, title, desc) in enumerate(chaps):
        units = M.units_in_chapter(num)
        page_slugs = set(u["slug"] for u in units)
        npat = sum(len(u["patterns"]) for u in units)
        meta = " ".join([
            badge("Chapter %d" % num, "badge--ch"),
            badge("%d lesson%s" % (len(units), "" if len(units) == 1 else "s")),
            badge("%d patterns" % npat, "badge--diff"),
        ])
        h1 = "Chapter %d · %s" % (num, title)
        content = render_units_stacked(units, "by-chapter", page_slugs) if units else \
            '<p class="page-sub">No standalone lessons map to this chapter.</p>'
        prev = (chapter_file(chaps[i - 1][0]), "Ch %d · %s" % (chaps[i - 1][0], chaps[i - 1][1])) if i > 0 else None
        nxt = (chapter_file(chaps[i + 1][0]), "Ch %d · %s" % (chaps[i + 1][0], chaps[i + 1][1])) if i < len(chaps) - 1 else None
        render("by-chapter", chapter_file(num), title, desc, h1, desc,
               meta, crumb("by-chapter", "By Chapter", "index.html", title),
               content, "Chapters", sidebar_chapter(num),
               view_tabs("by-chapter", "chapter"), prevnext_html(prev, nxt))


# ----------------------------------------------------------------- index pages
def pattern_card(u, idx, href):
    search = esc_attr(" ".join([u["title"], u["summary"], M.category_title(u["category"])] + u["patterns"]))
    return ('<a class="pattern-card" href="%s" data-search="%s">'
            '<div class="pc-top"><span class="pc-ic">%s</span>'
            '<span class="badge badge--%s">%s</span><span class="pc-idx">%02d</span></div>'
            '<h3>%s</h3><p>%s</p>'
            '<div class="tags">%s</div></a>'
            % (href, search, u["icon"], u["difficulty"], u["difficulty"], idx,
               esc(u["title"]), esc(u["summary"]),
               "".join('<span class="badge badge--pat">%s</span>' % esc(p) for p in u["patterns"][:3])
               + ("" if len(u["patterns"]) <= 3 else '<span class="badge">+%d</span>' % (len(u["patterns"]) - 3))))


def grid_by_category(href_for):
    out = []
    for cat_slug, cat_title, cat_desc in M.CATEGORIES:
        units = M.units_in_category(cat_slug)
        if not units:
            continue
        cards = "\n".join(pattern_card(u, M.UNITS.index(u) + 1, href_for(u)) for u in units)
        out.append('<section class="cat-section"><h2>%s <span class="c-count">%d</span></h2>'
                   '<p class="cat-desc">%s</p><div class="pattern-grid">%s</div></section>'
                   % (esc(cat_title), len(units), esc(cat_desc), cards))
    return "\n".join(out)


def build_view_indexes():
    # by-pattern index
    grid = grid_by_category(lambda u: "%s.html" % u["slug"])
    content = ('<p class="page-sub" style="margin-bottom:1.2rem">All %d lessons, grouped by category. '
               'Each lesson is a focused, self-contained page.</p>'
               '<div class="searchbox"><input id="pattern-search" type="search" '
               'placeholder="Filter patterns… (e.g. saga, gateway, kafka)" aria-label="Filter patterns"></div>'
               '%s' % (len(M.UNITS), grid))
    render("by-pattern", "index.html", "By Pattern", "Browse every microservices pattern individually.",
           "Browse by Pattern", "One focused page per pattern.", "",
           '<a href="../index.html">Home</a><span class="sep">/</span>By Pattern',
           content, "All Patterns", sidebar_pattern(None),
           view_tabs("by-pattern", "pattern"), "<span></span><span></span>")

    # by-category index
    cards = []
    for cat_slug, cat_title, cat_desc in M.CATEGORIES:
        units = M.units_in_category(cat_slug)
        if not units:
            continue
        items = "".join('<span class="badge">%s</span>' % esc(u["title"]) for u in units)
        cards.append('<a class="view-card" href="%s.html"><h3>%s</h3><p>%s</p>'
                     '<div class="tags" style="margin-top:.6rem">%s</div></a>'
                     % (cat_slug, esc(cat_title), esc(cat_desc), items))
    content = ('<p class="page-sub" style="margin-bottom:1.2rem">%d thematic categories. '
               'Each page gathers a family of related patterns.</p>'
               '<div class="view-cards">%s</div>'
               % (len([c for c in M.CATEGORIES if M.units_in_category(c[0])]), "\n".join(cards)))
    render("by-category", "index.html", "By Category", "Browse microservices patterns by theme.",
           "Browse by Category", "Patterns grouped into families.", "",
           '<a href="../index.html">Home</a><span class="sep">/</span>By Category',
           content, "Categories", sidebar_category(None),
           view_tabs("by-category", "category"), "<span></span><span></span>")

    # by-chapter index
    cards = []
    for num, title, desc in M.CHAPTERS:
        units = M.units_in_chapter(num)
        items = "".join('<span class="badge">%s</span>' % esc(u["title"]) for u in units)
        cards.append('<a class="view-card" href="%s"><span class="vc-ic">&#128214;</span>'
                     '<h3>Chapter %d · %s</h3><p>%s</p>'
                     '<div class="tags" style="margin-top:.6rem">%s</div></a>'
                     % (chapter_file(num), num, esc(title), esc(desc), items))
    content = ('<p class="page-sub" style="margin-bottom:1.2rem">Follow the book\'s narrative arc, '
               'chapter by chapter.</p><div class="view-cards">%s</div>' % "\n".join(cards))
    render("by-chapter", "index.html", "By Chapter", "Browse microservices patterns by book chapter.",
           "Browse by Chapter", "The guided, book-order path.", "",
           '<a href="../index.html">Home</a><span class="sep">/</span>By Chapter',
           content, "Chapters", sidebar_chapter(None),
           view_tabs("by-chapter", "chapter"), "<span></span><span></span>")


def build_master_index():
    npat = len(M.all_patterns())
    ncat = len([c for c in M.CATEGORIES if M.units_in_category(c[0])])
    grid = grid_by_category(lambda u: "by-pattern/%s.html" % u["slug"])
    view_cards = (
        '<a class="view-card" href="by-pattern/index.html"><span class="vc-ic">&#129513;</span>'
        '<h3>By Pattern</h3><p>%d focused pages — one per pattern. The reference view.</p></a>'
        '<a class="view-card" href="by-category/index.html"><span class="vc-ic">&#128218;</span>'
        '<h3>By Category</h3><p>%d thematic families of related patterns. The conceptual view.</p></a>'
        '<a class="view-card" href="by-chapter/index.html"><span class="vc-ic">&#128214;</span>'
        '<h3>By Chapter</h3><p>%d chapters in book order. The guided course view.</p></a>'
        % (len(M.UNITS), ncat, len(M.CHAPTERS)))
    body = """<header class="hero">
  <div class="page-meta">%s %s</div>
  <h1>%s</h1>
  <p class="lede">%s</p>
  <div class="stat-row">
    <div class="stat"><b>%d</b><span>lessons</span></div>
    <div class="stat"><b>%d</b><span>patterns</span></div>
    <div class="stat"><b>%d</b><span>categories</span></div>
    <div class="stat"><b>%d</b><span>chapters</span></div>
  </div>
</header>

<h2 style="margin-top:0">Choose how you want to learn</h2>
<p>The same material, organised three ways. Pick the lens that fits how you think — switch any time from the top bar.</p>
<div class="view-cards">%s</div>

<h2>All patterns</h2>
<p>Every pattern from the book, grouped by category. Use the filter to jump straight to one.</p>
<div class="searchbox"><input id="pattern-search" type="search" placeholder="Filter patterns… (e.g. saga, cqrs, kafka, gateway)" aria-label="Filter patterns"></div>
%s
""" % (badge("Architect's field guide", "badge--diff"),
       badge("Based on Chris Richardson · Manning", "badge--ch"),
       esc(M.COURSE_TITLE), esc(M.COURSE_SUBTITLE),
       len(M.UNITS), npat, ncat, len(M.CHAPTERS), view_cards, grid)

    pre = ""
    html = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="%s">
<title>%s — an architect's field guide</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<header class="topbar">
  <a class="brand" href="index.html"><span class="brand-mark">{ }</span><span class="brand-text">Microservices&nbsp;Patterns</span></a>
  <nav class="view-tabs" aria-label="Choose organization">
    <a href="by-pattern/index.html"><span class="vt-label">By Pattern</span></a>
    <a href="by-category/index.html"><span class="vt-label">By Category</span></a>
    <a href="by-chapter/index.html"><span class="vt-label">By Chapter</span></a>
  </nav>
  <button class="icon-btn theme-toggle" aria-label="Toggle light/dark theme" title="Toggle theme">&#9788;</button>
</header>
<main class="content" style="max-width:1180px;margin:0 auto">
%s
<footer class="page-foot"><p>Distilled from <em>Microservices Patterns</em> by Chris Richardson (Manning, 2019) and enriched with current tooling &amp; real-world practice. A self-study guide for IT professionals.</p></footer>
</main>
<script src="assets/course.js" defer></script>
</body>
</html>""" % (esc_attr(M.COURSE_SUBTITLE), esc(M.COURSE_TITLE), body)
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


# ----------------------------------------------------------------- validation
LOCAL_LINK_RE = re.compile(r'(?:href|src)="([^"#:]+\.(?:html|css|js))(#[^"]*)?"')
ANCHOR_RE = re.compile(r'(?:href)="#([^"]+)"')
ID_RE = re.compile(r'\bid="([^"]+)"')


def validate():
    problems = []
    pages = []
    for dirpath, _dirs, files in os.walk(ROOT):
        if (os.sep + "_src") in dirpath:
            continue
        for fn in files:
            if fn.endswith(".html"):
                pages.append(os.path.join(dirpath, fn))
    for p in pages:
        with open(p, encoding="utf-8") as f:
            html = f.read()
        base = os.path.dirname(p)
        ids = set(ID_RE.findall(html))
        for m in LOCAL_LINK_RE.finditer(html):
            target = os.path.normpath(os.path.join(base, m.group(1)))
            if not os.path.exists(target):
                problems.append("%s -> missing %s" % (os.path.relpath(p, ROOT), m.group(1)))
        for m in ANCHOR_RE.finditer(html):
            if m.group(1) not in ids:
                problems.append("%s -> dangling #%s" % (os.path.relpath(p, ROOT), m.group(1)))
    return pages, problems


# ----------------------------------------------------------------- main
def main():
    global TPL
    TPL = read_template()
    build_pattern_pages()
    build_category_pages()
    build_chapter_pages()
    build_view_indexes()
    build_master_index()
    pages, problems = validate()

    print("Generated %d HTML pages." % len(pages))
    print("  by-pattern : %d detail + 1 index" % len(M.UNITS))
    print("  by-category: %d detail + 1 index" % len([c for c in M.CATEGORIES if M.units_in_category(c[0])]))
    print("  by-chapter : %d detail + 1 index" % len(M.CHAPTERS))
    if MISSING:
        uniq = sorted(set(MISSING))
        print("\n[!] %d partial(s) not yet authored (placeholder shown):" % len(uniq))
        for s in uniq:
            print("      -", s)
    if BAD_REFS:
        print("\n[!] Unknown cross-reference slugs:", sorted(set(BAD_REFS)))
    if problems:
        print("\n[X] %d link problem(s):" % len(problems))
        for pr in problems[:60]:
            print("      -", pr)
    else:
        print("\n[OK] All internal links and anchors resolve.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
