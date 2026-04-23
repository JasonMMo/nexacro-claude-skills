#!/usr/bin/env python3
"""Dry-run for `/plugin install nexacro-fullstack-starter@nexacro-claude-skills`.

Simulates what Claude Code does on plugin installation:
  1. Parse marketplace.json, find plugin entry by name.
  2. Resolve source path relative to marketplace root.
  3. Load target plugin.json at <source>/.claude-plugin/plugin.json.
  4. Enumerate skills at <source>/skills/*/SKILL.md.
  5. Parse each SKILL.md YAML frontmatter (minimally — name / description / argument-hint).
  6. Enumerate assets and references per skill.

Read-only. Produces a summary report. Exits 0 on success, 1 on any resolution failure.
"""
import json
import os
import re
import sys

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN_NAME = "nexacro-fullstack-starter"
MARKETPLACE = "nexacro-claude-skills"


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


print(f"=== Dry-run: /plugin install {PLUGIN_NAME}@{MARKETPLACE} ===")
print()

# Step 1: marketplace lookup
mp_path = os.path.join(BASE, ".claude-plugin", "marketplace.json")
if not os.path.exists(mp_path):
    fail(f"marketplace.json not found at {mp_path}")
with open(mp_path, encoding="utf-8") as f:
    mp = json.load(f)
if mp["name"] != MARKETPLACE:
    fail(f"marketplace.name = {mp['name']!r}, expected {MARKETPLACE!r}")
entry = next((p for p in mp["plugins"] if p["name"] == PLUGIN_NAME), None)
if entry is None:
    fail(f"plugin {PLUGIN_NAME!r} not found in marketplace")
print(f"[1] Marketplace lookup:   OK ({MARKETPLACE} has {len(mp['plugins'])} plugins)")
print(f"    source: {entry['source']}")
print(f"    description: {entry['description'][:80]}...")

# Step 2: resolve plugin root
plugin_root = os.path.abspath(os.path.join(BASE, entry["source"]))
if not os.path.isdir(plugin_root):
    fail(f"plugin source directory missing: {plugin_root}")
print(f"[2] Source resolution:    OK ({plugin_root})")

# Step 3: plugin.json
pj_path = os.path.join(plugin_root, ".claude-plugin", "plugin.json")
if not os.path.exists(pj_path):
    fail(f"plugin.json missing at {pj_path}")
with open(pj_path, encoding="utf-8") as f:
    pj = json.load(f)
print(f"[3] plugin.json:          OK (version={pj['version']}, license={pj['license']})")
print(f"    keywords: {', '.join(pj['keywords'])}")

# Step 4: skill discovery
skills_dir = os.path.join(plugin_root, "skills")
if not os.path.isdir(skills_dir):
    fail(f"skills directory missing: {skills_dir}")
skill_names = sorted(
    d for d in os.listdir(skills_dir)
    if os.path.isdir(os.path.join(skills_dir, d))
)
print(f"[4] Skill discovery:      OK ({len(skill_names)} skill(s): {', '.join(skill_names)})")

# Step 5: per-skill frontmatter + asset enumeration
for sn in skill_names:
    sdir = os.path.join(skills_dir, sn)
    skill_md = os.path.join(sdir, "SKILL.md")
    if not os.path.exists(skill_md):
        fail(f"SKILL.md missing for skill {sn!r}")
    with open(skill_md, encoding="utf-8") as f:
        fm = parse_frontmatter(f.read())
    if fm is None:
        fail(f"YAML frontmatter missing/malformed in {skill_md}")
    for k in ("name", "description"):
        if k not in fm:
            fail(f"required frontmatter key {k!r} missing in {skill_md}")
    print(f"[5] SKILL.md ({sn}):")
    print(f"    name: {fm['name']}")
    print(f"    description: {fm['description'][:80]}...")
    if "argument-hint" in fm:
        print(f"    argument-hint: {fm['argument-hint']}")

    # Assets
    assets_dir = os.path.join(sdir, "assets")
    if os.path.isdir(assets_dir):
        assets = sorted(os.listdir(assets_dir))
        print(f"    assets: {assets}")
    else:
        print("    assets: (none)")

    # References
    refs_dir = os.path.join(sdir, "references")
    if os.path.isdir(refs_dir):
        refs = sorted(os.listdir(refs_dir))
        print(f"    references ({len(refs)}): {refs}")
    else:
        print("    references: (none)")

print()
print("DRY-RUN COMPLETE — plugin would install successfully.")
