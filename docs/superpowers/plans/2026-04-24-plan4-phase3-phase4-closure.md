# Phase 3 + Phase 4 Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to implement this plan task-by-task. Also bound by the global `orchestration-discipline` skill (4 gates).

**Goal:** Close out the `nexacro-fullstack-starter` rollout by (a) driving the 8 legacy GitLab repos into an archived state and (b) performing the post-release verification the spec's Phase 4 requires.

**Architecture:** This is closure / release-hygiene work, not code authoring. Most tasks are repo administration, verification scripts, and documentation. The only code artefacts produced are a drift-check script (Task 4.3) and a contract-dry-run harness (Task 4.2).

**Tech Stack:** `gh` CLI for GitHub repo admin, GitLab CLI (`glab`) or web UI for archival, `mvn` for smoke verification, Bash for scripting.

**Scope boundaries:**
- **IN SCOPE**: Phase 3 (GitLab 8-repo migration notice + archival) and Phase 4 closure items (plugin dry-run, drift test, release acknowledgment).
- **OUT OF SCOPE**: Task 1 (6 non-proven runner porting — `mvc-*`, `egov*`, `webflux-*`) → separate plan. Task 2 (14-endpoint controller alignment) → separate plan.
- **ALREADY SHIPPED** (do not re-execute): v1.8.0 tag, CHANGELOG baseline, plan1/2/3, v1.8.1/v1.8.2/v1.8.3 iterations, monorepo `v0.6.0-core-from-nexus`.

**Orchestration discipline:**
- Gate 1: plan authoring is coordinator-allowed (meta-doc). Per-task execution MUST dispatch a Sonnet/Haiku subagent.
- Gate 2: before the first repo-mutating task, intent-check each destructive step with codex-rescue (or Explore fallback).
- Gate 3: before tagging `v1.9.0` (the closure tag proposed here), pre-tag verification via independent reader.
- Gate 4: if any task requires undoing a prior tag (e.g., re-rolling v1.8.0 claims), STOP and write a retrospective first.

---

## Spec Coverage Map

| Spec section | Item | Plan task |
|---|---|---|
| §8 Phase 3 | 8 repo README 이관 공지 | Task 3.1 |
| §8 Phase 3 | 1~2 스프린트 후 아카이브 | Task 3.2 |
| §8 Phase 4 | codex:codex-rescue 검증 | Task 4.1 |
| §8 Phase 4 | 8 runner 실빌드/실행 스모크 | **OUT OF SCOPE** — owned by Task 1 plan (6 non-proven runners); jakarta+javax already covered by plan2/plan3 |
| §8 Phase 4 | 플러그인 설치 dry-run | Task 4.2 |
| §8 Phase 4 | v1.8.0 태그 + CHANGELOG 확정 | **ALREADY SHIPPED** — superseded by v1.8.3 |
| §11 Acceptance #1 | 8-조합 dispatch | **Deferred** — depends on Task 1 completion |
| §11 Acceptance #2 | `mvn verify` 통과 | **Deferred** — depends on Task 1 |
| §11 Acceptance #3 | nxui 8 menu 동작 | **Deferred** — depends on Task 1 |
| §11 Acceptance #4 | drift test 통과 | Task 4.3 |
| §11 Acceptance #5 | codex-rescue 독립 검증 | Task 4.1 |

---

## Task 3.1: GitLab 8-repo migration-notice README patch

**Files:**
- Modify (per legacy repo, 8 total): top-level `README.md` in each of:
  1. `nexacroN-boot-jdk17-jakarta` (legacy)
  2. `nexacroN-boot-jdk8-javax` (legacy)
  3. `nexacroN-mvc-jdk17-jakarta` (legacy)
  4. `nexacroN-mvc-jdk8-javax` (legacy)
  5. `nexacroN-egov5-boot-jdk17-jakarta` (legacy)
  6. `nexacroN-egov4-boot-jdk8-javax` (legacy)
  7. `nexacroN-egov4-mvc-jdk8-javax` (legacy)
  8. `nexacroN-webflux-jdk17-jakarta` (legacy)

*(Exact repo paths: to be confirmed from user's GitLab namespace before execution. This task's first step resolves the list.)*

- [ ] **Step 1: Resolve the 8 legacy repo slugs**

Dispatch Haiku subagent:
```
Agent(
  subagent_type="Explore",
  description="Resolve 8 legacy GitLab repo slugs",
  prompt="Query the user's GitLab namespace (via glab repo list --per-page 100 or equivalent) for repos matching the pattern nexacroN-*. Return the 8 slugs matching the runner matrix from spec §2.1. If the user has a different naming, return the actual slugs. Print one per line."
)
```
Expected: 8 `namespace/repo-name` slugs printed to stdout.

If glab is not installed or credentials missing → ESCALATE to user. Do not guess.

- [ ] **Step 2: Draft the migration-notice block (shared template)**

Dispatch Haiku subagent to write this to `D:\AI\workspace\nexacro-claude-skills\docs\superpowers\assets\migration-notice.md`:

```markdown
> ⚠️ **이관 공지 (Migration Notice)**
>
> 이 저장소는 **아카이브 예정**입니다. 동일 기능이 통합 monorepo로 이관되었습니다.
>
> - **신규 위치**: [github.com/JasonMMo/nexacroN-fullstack](https://github.com/JasonMMo/nexacroN-fullstack)
> - **사용 방법**: Claude Code에서 `/plugin install nexacro-fullstack-starter@nexacro-claude-skills` 후 `/nexacro-fullstack-starter` 호출
> - **조합 선택**: JDK(8/17) × framework(Spring Boot / Spring MVC / eGov / WebFlux) 조합을 대화식으로 선택
> - **1차 아카이브 시점**: 본 공지 게시 후 2 스프린트 경과 시
>
> 기존 이슈/PR은 새 모노레포로 재오픈 바랍니다.
```

- [ ] **Step 3: Per-repo README patch (×8)**

For each of the 8 slugs, dispatch a Haiku subagent (one per repo, serial to avoid GitLab rate limits):
```
Agent(
  subagent_type="general-purpose",
  description="Patch migration notice into repo <slug> README",
  prompt="Clone <namespace/slug> into a temp dir. Prepend the contents of D:\\AI\\workspace\\nexacro-claude-skills\\docs\\superpowers\\assets\\migration-notice.md to README.md (or create README.md if absent) above any existing content. Commit with message 'docs: add migration notice to nexacroN-fullstack monorepo'. Push to the default branch. Print the resulting commit SHA."
)
```

- [ ] **Step 4: Verify all 8 repos carry the notice**

Dispatch Explore subagent to fetch each repo's README.md HEAD via glab and confirm the first line matches `> ⚠️ **이관 공지`. Print a per-repo PASS/FAIL table.

- [ ] **Step 5: Record in tasks/todo.md**

Update `tasks/todo.md` with the 8 slugs + commit SHAs and the earliest-archival-date (sprint-start + 2 sprints, e.g., 2026-05-22 if sprints are 2-week).

---

## Task 3.2: Scheduled archival follow-through

**Files:**
- Create: `docs/governance/gitlab-archival-checklist.md`

This task is **time-gated**: it does NOT execute archival now. It produces the checklist and the calendar trigger.

- [ ] **Step 1: Write the archival checklist**

Dispatch Sonnet subagent to write `docs/governance/gitlab-archival-checklist.md` containing:
- The 8 slug list
- Per-repo pre-archival checks (open MRs count, last-commit date, outstanding issues)
- Archival command (`glab repo archive <slug>`) or web-UI step sequence
- Post-archival verification (`glab repo view <slug> --output json | jq .archived`)
- Rollback note: archival is reversible via `glab repo unarchive`.

- [ ] **Step 2: Commit and note in tasks/todo.md**

```
git add docs/governance/gitlab-archival-checklist.md
git commit -m "docs(governance): GitLab archival checklist for 8 legacy repos"
```

Add an entry in `tasks/todo.md` under a `### Scheduled` section noting the earliest execution date from Task 3.1 Step 5.

---

## Task 4.1: Independent intent verification (codex-rescue or fallback)

**Purpose:** Acceptance criterion §11.5 — `codex:codex-rescue 독립 검증 통과`.

- [ ] **Step 1: Assemble verification packet**

Dispatch Haiku subagent to write `tasks/v1.8.x-verification-packet.md` containing:
- Final state snapshot: skills repo tags `v1.8.0..v1.8.3`, monorepo tag `v0.6.0-core-from-nexus`.
- Spec acceptance criteria §11.1–§11.5 copy-pasted verbatim.
- Per-criterion current status (MET / PARTIAL / DEFERRED-to-Task-1).
- List of commits under each tag (`git log <prev-tag>..<tag> --oneline`).

- [ ] **Step 2: Dispatch codex-rescue**

```
Agent(
  subagent_type="codex:codex-rescue",
  description="Independent Phase-4 acceptance verification",
  prompt="Read tasks/v1.8.x-verification-packet.md. For each of the 5 acceptance criteria, verify the claimed status against the actual repo state (git log, file existence, tag presence). Return GO / NO-GO + per-criterion verdict + any gaps."
)
```

If codex-rescue unavailable, fall back to:
```
Agent(
  subagent_type="Explore",
  description="Independent Phase-4 acceptance verification (fallback)",
  prompt="<same prompt>"
)
```

- [ ] **Step 3: Record verdict in tasks/todo.md**

If GO: proceed to Task 4.2.
If NO-GO with DEFERRED gaps only (tasks 1 and 2 scope): document and proceed.
If NO-GO with in-scope gaps: STOP. Write retrospective (Gate 4 trigger if a shipped tag is implicated). Fix gaps, re-run Task 4.1.

---

## Task 4.2: Plugin install dry-run harness

**Purpose:** Acceptance criterion §11.1 (partial — without 6 runners, only verifies plugin mechanics, not runner dispatch).

**Files:**
- Create: `scripts/plugin-dry-run.sh`

- [ ] **Step 1: Write dry-run script**

Dispatch Sonnet subagent to author `scripts/plugin-dry-run.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Dry-run: simulate /plugin install nexacro-fullstack-starter without modifying user state.
# - Parses plugin.json and marketplace.json
# - Verifies SKILL.md front-matter
# - Confirms matrix.json has 8 runner entries
# - Confirms 4 reference files resolve

PLUGIN_DIR="$(cd "$(dirname "$0")/../plugins/nexacro-fullstack-starter" && pwd)"
FAIL=0

check() { if [ ! -e "$1" ]; then echo "MISSING: $1"; FAIL=1; else echo "OK: $1"; fi; }

check "$PLUGIN_DIR/.claude-plugin/plugin.json"
check "$PLUGIN_DIR/SKILL.md"
check "$PLUGIN_DIR/assets/matrix.json"

# matrix.json runner count
COUNT=$(python -c "import json,sys; d=json.load(open('$PLUGIN_DIR/assets/matrix.json')); print(len(d.get('runners',[])))" 2>/dev/null || echo "?")
if [ "$COUNT" = "8" ]; then echo "OK: matrix runners = 8"; else echo "FAIL: matrix runners = $COUNT (expected 8)"; FAIL=1; fi

# marketplace inclusion
grep -q "nexacro-fullstack-starter" "$PLUGIN_DIR/../../.claude-plugin/marketplace.json" && echo "OK: marketplace registered" || { echo "FAIL: not in marketplace"; FAIL=1; }

exit $FAIL
```

- [ ] **Step 2: Run and record**

```bash
bash scripts/plugin-dry-run.sh | tee tasks/plugin-dry-run-$(date +%Y%m%d).log
```

Expected exit 0. Non-zero → investigate, do NOT proceed.

- [ ] **Step 3: Commit**

```bash
git add scripts/plugin-dry-run.sh tasks/plugin-dry-run-*.log
git commit -m "chore(verify): plugin install dry-run harness + Phase 4 baseline"
```

---

## Task 4.3: Drift test (monorepo ↔ plugin matrix sync)

**Purpose:** Acceptance criterion §11.4 — `nexacroN-fullstack 모노레포 업데이트 1회로 8 runner가 자동 반영 (drift test 통과)`.

**Files:**
- Create: `scripts/drift-check.sh`

- [ ] **Step 1: Write drift-check script**

Dispatch Sonnet subagent to author `scripts/drift-check.sh` that:
- Reads runner list from `plugins/nexacro-fullstack-starter/assets/matrix.json`
- For each runner, asserts the corresponding `samples/runners/<name>/pom.xml` exists in the sibling monorepo (`D:/AI/workspace/nexacroN-fullstack`)
- Extracts the 10 `<nexacro.*.version>` properties from the monorepo parent pom and asserts they match the versions declared in `plugins/nexacro-fullstack-starter/assets/matrix.json` (if matrix pins them)
- Flags any runner present in monorepo but absent from matrix, or vice versa

Script must print a table:
```
runner                     in-matrix  in-monorepo  status
boot-jdk17-jakarta         YES        YES          OK
boot-jdk8-javax            YES        YES          OK
mvc-jdk17-jakarta          YES        NO           DRIFT (awaiting Task 1)
...
```

- [ ] **Step 2: Run and record expected drift**

Expected at this point: 2 runners OK, 6 runners DRIFT (pending Task 1). Document this as expected state in `tasks/drift-baseline-$(date +%Y%m%d).log`.

- [ ] **Step 3: Commit**

```bash
git add scripts/drift-check.sh tasks/drift-baseline-*.log
git commit -m "chore(verify): drift-check script + baseline (2/8 runners present, 6 deferred)"
```

---

## Task 4.4: v1.9.0 closure tag (optional — conditional on Tasks 1 & 2)

**Gate 4 check:** This task MUST be deferred until Task 1 (runner porting) and Task 2 (14-endpoint alignment) are complete. Tagging v1.9.0 now would mis-claim acceptance §11.1–§11.3.

- [ ] **Step 1: Defer marker**

Dispatch Haiku subagent to append to `tasks/todo.md`:

```markdown
### Deferred — v1.9.0 closure tag
Trigger: Tasks 1 (6-runner port) + Task 2 (14-endpoint alignment) both merged to master with their own release notes. Then:
- re-run Task 4.1 (codex-rescue)
- re-run Task 4.3 (drift-check should be 8/8 OK)
- write docs/releases/v1.9.0.md citing spec acceptance §11.1–§11.5 fully met
- tag v1.9.0 (Gate 3 verification required before push)
```

- [ ] **Step 2: Commit**

```bash
git add tasks/todo.md
git commit -m "chore(tasks): defer v1.9.0 closure tag pending Tasks 1-2"
```

---

## Gate-3 Verification (Pre-Tag)

This plan itself does NOT tag. It leaves the skills repo at HEAD-of-master with:
- A new `docs/superpowers/plans/2026-04-24-plan4-phase3-phase4-closure.md` (this file)
- (After execution) `scripts/plugin-dry-run.sh`, `scripts/drift-check.sh`, `docs/governance/gitlab-archival-checklist.md`, migration-notice assets, baseline logs

Before final plan4-completion commit, dispatch independent reader:
```
Agent(
  subagent_type="Explore",
  description="Plan4 Gate-3 verification",
  prompt="Read 2026-04-24-plan4-phase3-phase4-closure.md against spec §8 Phase 3-4 and §11. Verify: (a) no task overlaps Task 1/Task 2 scope, (b) no task claims v1.8.x re-tag, (c) acceptance criteria mapping is accurate, (d) no placeholders/TBDs remain. Return GO / NO-GO."
)
```

---

## Self-Review Checklist

- [x] Every step has concrete files / commands / expected output
- [x] No placeholders (TBD/TODO/etc.)
- [x] Scope boundaries explicit — Tasks 1 & 2 excluded
- [x] Gate 4 honoured — v1.9.0 tag deferred, no re-roll of v1.8.x
- [x] Each dispatch names model tier (Haiku for mechanical, Sonnet for scripting)
- [x] Fallback paths documented (codex-rescue → Explore)
- [x] Destructive ops (GitLab archival) gated behind time window + separate task

---

## Execution Handoff

**Recommendation**: `superpowers:subagent-driven-development` — this plan has 4 independent tasks with clear boundaries, each suitable for a fresh subagent with two-stage review.

**Alternative**: Manual execution if session context budget is tight — each task stands alone and can be done across sessions.

Next concrete action: **dispatch Gate-2 intent-check once more on Task 3.1 specifically** (GitLab mutation blast radius), then begin Task 3.1 Step 1.
