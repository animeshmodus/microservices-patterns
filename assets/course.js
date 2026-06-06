/* Microservices Patterns course — interactivity
   - light/dark theme (persisted)
   - Mermaid load + render + re-theme on toggle
   - auto "On this page" TOC + scrollspy
   - mobile sidebar
   - index page search filter
*/
(function () {
  "use strict";
  var root = document.documentElement;
  var MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js";
  // Derive asset root from the stylesheet link — works at any URL depth (root, sub-folder, gh-pages subdir)
  var _css = document.querySelector('link[rel=stylesheet][href*="styles.css"]');
  var MERMAID_LOCAL = _css
    ? _css.href.replace(/\/styles\.css(\?.*)?$/, "") + "/vendor/mermaid.min.js"
    : null;

  /* ---------- Theme ---------- */
  function currentTheme() { return root.getAttribute("data-theme") || "dark"; }
  function applyTheme(t) {
    root.setAttribute("data-theme", t);
    try { localStorage.setItem("ms-theme", t); } catch (e) {}
    var btn = document.querySelector(".theme-toggle");
    if (btn) btn.innerHTML = (t === "dark") ? "☀" : "☽"; // sun / moon
  }
  (function initTheme() {
    var saved = null;
    try { saved = localStorage.getItem("ms-theme"); } catch (e) {}
    applyTheme(saved || "dark");
  })();

  /* ---------- Mermaid ---------- */
  function loadScript(url) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = url;
      s.onload = function () { resolve(); };
      s.onerror = function () { reject(); };
      document.head.appendChild(s);
    });
  }
  var mermaidLoading = null;
  function loadMermaid() {
    if (window.mermaid) return Promise.resolve(window.mermaid);
    if (mermaidLoading) return mermaidLoading;
    // Try vendored copy first, fall back to CDN
    var load = MERMAID_LOCAL
      ? loadScript(MERMAID_LOCAL).catch(function () { return loadScript(MERMAID_CDN); })
      : loadScript(MERMAID_CDN);
    mermaidLoading = load.then(function () { return window.mermaid; });
    return mermaidLoading;
  }
  function mermaidVars(theme) {
    var dark = theme === "dark";
    return {
      primaryColor: dark ? "#182238" : "#eef2f9",
      primaryTextColor: dark ? "#e7ecf5" : "#16213a",
      primaryBorderColor: dark ? "#38bdf8" : "#0284c7",
      lineColor: dark ? "#6f82a3" : "#64748b",
      secondaryColor: dark ? "#131c2e" : "#ffffff",
      tertiaryColor: dark ? "#0f1626" : "#f3f6fc",
      fontFamily: '"Segoe UI", system-ui, sans-serif',
      fontSize: "15px",
      actorBkg: dark ? "#182238" : "#eef2f9",
      actorBorder: dark ? "#38bdf8" : "#0284c7",
      noteBkgColor: dark ? "#1f2a44" : "#fef3c7",
      noteTextColor: dark ? "#e7ecf5" : "#16213a"
    };
  }
  function captureSources() {
    var nodes = document.querySelectorAll("pre.mermaid, div.mermaid");
    nodes.forEach(function (n) {
      if (!n.dataset.src) n.dataset.src = n.textContent.trim();
    });
    return nodes;
  }
  function renderMermaid() {
    var nodes = captureSources();
    if (!nodes.length) return;
    loadMermaid().then(function (mermaid) {
      var theme = currentTheme();
      // restore source + reset processed flag so re-theming works
      nodes.forEach(function (n) {
        n.textContent = n.dataset.src;
        n.removeAttribute("data-processed");
        n.innerHTML = n.innerHTML; // ensure text node
        n.textContent = n.dataset.src;
      });
      mermaid.initialize({
        startOnLoad: false,
        theme: theme === "dark" ? "dark" : "default",
        securityLevel: "loose",
        themeVariables: mermaidVars(theme),
        flowchart: { curve: "basis", htmlLabels: true, useMaxWidth: true },
        sequence: { useMaxWidth: true, mirrorActors: false }
      });
      try {
        mermaid.run({ querySelector: "pre.mermaid, div.mermaid" });
      } catch (e) { /* older API fallback */
        try { mermaid.init(undefined, nodes); } catch (e2) {}
      }
    }).catch(function () {
      document.querySelectorAll("pre.mermaid,div.mermaid").forEach(function (n) {
        n.style.color = "var(--faint)";
      });
    });
  }

  /* ---------- On-this-page TOC ---------- */
  function slugify(s) {
    return s.toLowerCase().replace(/[^\w\s-]/g, "").trim().replace(/\s+/g, "-").slice(0, 60);
  }
  function buildToc() {
    var nav = document.querySelector(".toc-nav");
    var prose = document.querySelector(".prose");
    if (!nav || !prose) return;
    var heads = prose.querySelectorAll("h2, h3, .unit-title");
    if (heads.length < 2) { var t = document.querySelector(".toc"); if (t) t.style.display = "none"; return; }
    var seen = {};
    var links = [];
    heads.forEach(function (h) {
      var id = h.id;
      if (!id) {
        id = slugify(h.textContent) || "sec";
        while (seen[id]) id = id + "-x";
        h.id = id;
      }
      seen[id] = true;
      var a = document.createElement("a");
      a.href = "#" + id;
      a.textContent = h.textContent;
      var lvl = h.classList.contains("unit-title") ? 2 : (h.tagName === "H3" ? 3 : 2);
      a.className = "lvl-" + lvl;
      nav.appendChild(a);
      links.push(a);
    });
    // scrollspy
    var map = {};
    links.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var a = map[en.target.id];
        if (!a) return;
        if (en.isIntersecting) {
          links.forEach(function (l) { l.classList.remove("active"); });
          a.classList.add("active");
        }
      });
    }, { rootMargin: "-80px 0px -70% 0px", threshold: 0 });
    heads.forEach(function (h) { obs.observe(h); });
  }

  /* ---------- Mobile sidebar ---------- */
  function initNav() {
    var btn = document.querySelector(".nav-toggle");
    var scrim = document.querySelector(".nav-scrim");
    function close() { document.body.classList.remove("nav-open"); if (btn) btn.setAttribute("aria-expanded", "false"); }
    if (btn) btn.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    if (scrim) scrim.addEventListener("click", close);
    document.querySelectorAll(".sidebar .nav a").forEach(function (a) {
      a.addEventListener("click", close);
    });
  }

  /* ---------- Index search ---------- */
  function initSearch() {
    var input = document.getElementById("pattern-search");
    if (!input) return;
    input.addEventListener("input", function () {
      var q = input.value.toLowerCase().trim();
      document.querySelectorAll(".pattern-card").forEach(function (card) {
        var hay = (card.getAttribute("data-search") || card.textContent).toLowerCase();
        card.classList.toggle("is-hidden", q !== "" && hay.indexOf(q) === -1);
      });
      document.querySelectorAll(".cat-section").forEach(function (sec) {
        var anyVisible = sec.querySelector(".pattern-card:not(.is-hidden)");
        sec.classList.toggle("is-hidden", !anyVisible);
      });
    });
  }

  /* ---------- Boot ---------- */
  function boot() {
    var tt = document.querySelector(".theme-toggle");
    if (tt) tt.addEventListener("click", function () {
      applyTheme(currentTheme() === "dark" ? "light" : "dark");
      renderMermaid();
    });
    initNav();
    buildToc();
    initSearch();
    renderMermaid();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
