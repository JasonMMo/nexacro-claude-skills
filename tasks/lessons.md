# Lessons — nexacro-claude-skills

Rolling record of corrections. Update after every user correction. Pair with the global `orchestration-discipline` skill.

---

## 2026-04-24 — v1.8.2 → v1.8.3 rework (6-hour supersession)

### What shipped wrong

v1.8.2 delivered a "partial, honest" local-snapshot approach:
- 2 jakarta SNAPSHOT jars under `core/libs/jakarta/` (timestamp-pinned, 720 KB)
- 102-file uiadapter-javax source tree under `core/uiadapter-javax/`
- Runners wired via `<scope>system</scope> <systemPath>...</systemPath> <optional>true</optional>`

Tagged `v0.5.0-core` (monorepo) + `v1.8.2` (plugin), pushed to both remotes.

### What the user actually wanted

Nexus-resolved dependencies. User made this explicit by pasting a target `pom.xml` showing `<repositories>` → `mangosteen.tobesoft.co.kr` + `<properties>` with 5 `nexacro.*.version` pins + bare `<dependency>` entries.

v1.8.3 redid the work: parent pom centralization + 10 bare deps across the 2 runners + deletion of everything v1.8.2 had added to `core/`.

### Root causes (mapped to the 4 gates)

| Gate | What should have happened | What happened |
|---|---|---|
| 1 — No-typing | Opus dispatches `Agent()` for pom edits, jar copy, source tree copy | Opus wrote every file inline |
| 2 — Intent-check | Before touching core/, dispatch codex with the design + all prior user quotes (including "tobesoft Nexus" references) and ask "does this match intent?" | 0 codex calls. Self-interpreted user's "xapi/xeni의 jar가 있다" as literal "ship them" |
| 3 — Pre-tag | Before `git tag v1.8.2` + push, dispatch codex with the diff + release notes | Self-verified with `mvn compile` only |
| 4 — Supersession | When v1.8.3 started rewriting v1.8.2's core/, pause and retrospect first | Went straight into implementation; retrospective demanded by user after the fact |

### Structural prevention

Global skill: `~/.claude/skills/orchestration-discipline/SKILL.md` — encodes the 4 gates, dispatch templates, decision flow.

### Specific hand-rules for this project

- **Before any monorepo `core/` change**: check if the user has mentioned tobesoft Nexus (`mangosteen.tobesoft.co.kr`) anywhere in the conversation or prior sessions. If yes, Nexus resolution is always the preferred design over vendoring.
- **No `<systemPath>` dependencies in this repo**. If a build requires a local jar, escalate to the user rather than wiring systemPath — it almost always means a Nexus/repo configuration is missing.
- **"core/ is asymmetric" = design smell**, not a gap-to-document. If one lane has source and the other has binaries, the design is wrong — stop and redesign.

### Verification that prevention works

The rework itself proved the correct pattern:
- v1.8.3 parent pom centralizes 10 version properties + dependencyManagement
- Runner poms carry 5 bare `<dependency>` entries each (no version, no systemPath)
- `mvn compile` → BUILD SUCCESS on both runners with real Nexus resolution
- `~/.m2/settings.xml` `<server id="tobesoft-snapshots">` is the one consumer-side requirement

Future `core/`-related work must pass Gates 2 and 3 explicitly before tagging.

---

## 2026-04-24 (PM) — Public-repo miscall in v1.8.3 docs

### What shipped wrong

v1.8.3's `core/README.md`, `docs/releases/v1.8.3.md`, and `CHANGELOG.md` all claimed that `~/.m2/settings.xml` must carry a `<server id="tobesoft-snapshots">` block with tobesoft-issued credentials to download jars. Included a code block with username/password env-var substitution.

### What the user pointed out

`mangosteen.tobesoft.co.kr/nexus/repository/tobesoft-snapshots/` is a **public repository**. Anonymous access covers both metadata reads AND jar downloads. No credentials needed.

### Root cause

Gate 2 failure, second instance — a different flavor than the v1.8.2 one:

- v1.8.2 case: literal interpretation of user words ("jar가 있다" → ship them)
- This case: **inherited assumption**. I wrote "requires credentials" based on the generic pattern "private-looking Nexus URL + SNAPSHOT repo ⇒ auth required" without verifying against actual behavior.

The real `mvn compile` session that I build-verified with ran successfully — which was evidence that credentials were NOT required in that environment. I didn't read that signal. The `~/.m2/settings.xml` on my machine may or may not have had a `<server>` entry, but the fact that `mvn compile` worked for an anonymous metadata fetch + jar download should have been the test I ran explicitly.

### Prevention rule

**External infrastructure properties (public/private, auth requirements, rate limits, TLS posture) must be verified by direct observation, not documented by assumption.**

Specifically:
- Before claiming "requires credentials" in any doc, run the operation in a known-credential-less context (e.g., `mvn -s /dev/null compile` or equivalent clean `settings.xml`)
- Before claiming "public", likewise verify — don't assume based on URL pattern
- If a user has mentioned the infrastructure by URL or name before, ask them once rather than guessing

### Scope of fix

- `nexacroN-fullstack/core/README.md` — "Required credentials" section replaced with "No credentials needed" note (commit `64bb281` on monorepo main)
- `nexacro-claude-skills/docs/releases/v1.8.3.md` — credentials block removed from consumer setup
- `nexacro-claude-skills/CHANGELOG.md` — "Consumer requirement" entry updated to "none"

Tag `v1.8.3` itself is not re-rolled — these are doc-only corrections committed onto master after the tag, since Keep-a-Changelog supports post-release doc fixes when the code behavior is unchanged.

---
