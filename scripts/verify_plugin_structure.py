#!/usr/bin/env python3
"""Structural verification for nexacro-fullstack-starter plugin.

Read-only. Produces PASS/FAIL for 7 structural checks required before Plan 1 sign-off.
"""
import json
import os
import re
import sys

BASE = os.path.join(os.path.dirname(__file__), "..")
BASE = os.path.abspath(BASE)
PLUGIN = os.path.join(BASE, "plugins", "nexacro-fullstack-starter")
SKILL_DIR = os.path.join(PLUGIN, "skills", "nexacro-fullstack-starter")

results = []

# 1. Marketplace entry
mp_path = os.path.join(BASE, ".claude-plugin", "marketplace.json")
with open(mp_path, encoding="utf-8") as f:
    mp = json.load(f)
names = [p["name"] for p in mp["plugins"]]
entry = next((p for p in mp["plugins"] if p["name"] == "nexacro-fullstack-starter"), None)
ok1 = (
    len(mp["plugins"]) == 3
    and entry is not None
    and entry["source"] == "./plugins/nexacro-fullstack-starter"
    and all(k in entry for k in ("name", "source", "description"))
)
results.append(("Marketplace entry", ok1, f"plugins={names}"))

# 2. Plugin manifest
pj_path = os.path.join(PLUGIN, ".claude-plugin", "plugin.json")
with open(pj_path, encoding="utf-8") as f:
    pj = json.load(f)
req = ["name", "version", "description", "author", "homepage", "repository", "license", "keywords"]
missing = [k for k in req if k not in pj]
ok2 = not missing and pj["version"] == "0.1.0" and pj["name"] == "nexacro-fullstack-starter"
results.append(("Plugin manifest", ok2, f"version={pj.get('version')} missing={missing}"))

# 3. SKILL.md frontmatter
skill_path = os.path.join(SKILL_DIR, "SKILL.md")
with open(skill_path, encoding="utf-8") as f:
    txt = f.read()
m = re.match(r"^---\s*\n(.*?)\n---", txt, re.S)
ok3 = False
if m:
    fm = m.group(1)
    ok3 = all(k in fm for k in ["name:", "description:", "argument-hint:"])
results.append(("SKILL.md frontmatter", ok3, "present" if ok3 else "missing required keys"))

# 4. Matrix integrity
mx_path = os.path.join(SKILL_DIR, "assets", "matrix.json")
with open(mx_path, encoding="utf-8") as f:
    mx = json.load(f)
expected = {
    "boot-jdk17-jakarta",
    "boot-jdk8-javax",
    "mvc-jdk17-jakarta",
    "mvc-jdk8-javax",
    "egov5-boot-jdk17-jakarta",
    "egov4-boot-jdk8-javax",
    "egov4-mvc-jdk8-javax",
    "webflux-jdk17-jakarta",
}
nx = mx["nexacroVersions"]["nexacroN"]
runner_ids = set(nx["runners"].keys())
runner_fields_ok = all(
    all(k in r for k in ["runnerPath", "businessTree", "jdk", "servletApi", "framework"])
    for r in nx["runners"].values()
)
rejected = nx.get("rejectedCombinations", [])
rej_str = json.dumps(rejected)
ok4 = (
    len(runner_ids) == 8
    and runner_ids == expected
    and runner_fields_ok
    and ("egov-mvc" in rej_str and "jdk17" in rej_str)
    and ("webflux" in rej_str and "jdk8" in rej_str)
)
results.append(
    ("Matrix integrity", ok4, f"runners={len(runner_ids)} fields_ok={runner_fields_ok} rejected={len(rejected)}")
)

# 5. References complete
refs_dir = os.path.join(SKILL_DIR, "references")
expected_refs = {"compatibility-matrix.md", "repo-map.md", "runner-selection-guide.md", "troubleshooting.md"}
actual_refs = set(os.listdir(refs_dir))
ok5 = expected_refs.issubset(actual_refs)
results.append(("References complete", ok5, f"found={sorted(actual_refs)}"))

# 6. README consistency
for fname in ("README.md", "README-ko.md"):
    with open(os.path.join(BASE, fname), encoding="utf-8") as f:
        t = f.read()
    has_install = "install nexacro-fullstack-starter@" in t
    # Section heading check: a line starting with "###" that mentions the plugin
    has_section = bool(re.search(r"^###.*nexacro-fullstack-starter", t, re.M))
    # Plain-text mentions (anywhere)
    mentions = t.count("nexacro-fullstack-starter")
    ok = has_install and has_section and mentions >= 4
    results.append((f"{fname} consistency", ok, f"install={has_install} section={has_section} total_mentions={mentions}"))

# 7. CHANGELOG
with open(os.path.join(BASE, "CHANGELOG.md"), encoding="utf-8") as f:
    cl = f.read()
ok7 = "## [1.8.0]" in cl and "nexacro-fullstack-starter" in cl
results.append(("CHANGELOG v1.8.0 entry", ok7, "found" if ok7 else "missing"))

for i, (name, ok, detail) in enumerate(results, 1):
    print(f"{i}. {name}: {'PASS' if ok else 'FAIL'} ({detail})")

all_pass = all(ok for _, ok, _ in results)
print()
print("ALL STRUCTURAL CHECKS PASSED" if all_pass else "FAILURES DETECTED")
sys.exit(0 if all_pass else 1)
