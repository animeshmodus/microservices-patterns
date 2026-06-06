# -*- coding: utf-8 -*-
"""Post-build verification: pattern coverage per view, token/ref leaks, diagram counts."""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import manifest as M

def read_view(view):
    d = os.path.join(ROOT, view)
    txt = []
    for fn in os.listdir(d):
        if fn.endswith(".html"):
            txt.append(open(os.path.join(d, fn), encoding="utf-8").read())
    return "\n".join(txt)

patterns = M.all_patterns()
print("Patterns to cover: %d\n" % len(patterns))
ok = True
for view in ("by-pattern", "by-category", "by-chapter"):
    blob = read_view(view)
    missing = [p for p in patterns if p not in blob]
    tag = "OK " if not missing else "MISSING"
    print("[%s] %-12s : %d/%d patterns present" % (tag, view, len(patterns) - len(missing), len(patterns)))
    if missing:
        ok = False
        for m in missing:
            print("        missing:", m)

# leak checks + diagram counts across all generated html (exclude _src)
tok = ref = mermaid = arch = pages = 0
for dp, dn, fns in os.walk(ROOT):
    if "_src" in dp:
        continue
    for fn in fns:
        if not fn.endswith(".html"):
            continue
        pages += 1
        t = open(os.path.join(dp, fn), encoding="utf-8").read()
        tok += len(re.findall(r"\{\{[A-Z_]+\}\}", t))  # genuine template tokens only (not Mermaid {{..}})
        ref += t.count('href="ref:')
        mermaid += len(re.findall(r'class="mermaid"', t))
        arch += t.count("arch-canvas")

print("\nPages: %d | Mermaid diagrams: %d | Hero arch diagrams: %d" % (pages, mermaid, arch))
print("Leftover {{tokens}}: %d | Unresolved ref: links: %d" % (tok, ref))
print("\nRESULT:", "ALL GOOD" if (ok and tok == 0 and ref == 0) else "PROBLEMS FOUND")
