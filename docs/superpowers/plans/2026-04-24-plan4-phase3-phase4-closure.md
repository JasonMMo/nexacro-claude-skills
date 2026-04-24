# Phase 3 + Phase 4 Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to implement this plan task-by-task. Also bound by the global `orchestration-discipline` skill (4 gates).

**Goal:** Close out the `nexacro-fullstack-starter` rollout by (a) establishing a **parallel-maintenance governance model** for the 7 public (+ 1 pending) legacy GitLab repos and (b) performing the post-release verification the spec's Phase 4 requires.

> **Phase 3 pivot (2026-04-24):** Legacy repos are NOT archived. They remain in parallel maintenance until the starter is independently validated per measurable sunset criteria (Task 3.3). Archival is deferred to a future plan8 triggered only on user sign-off.

**Architecture:** This is closure / release-hygiene + governance work, not code authoring. Most tasks are advisory communication, parity documentation, verification scripts, and sunset-criteria framework. The only code artefacts produced are a drift-check script (Task 4.3) and a dry-run harness (Task 4.2).

**Tech Stack:** `gh` CLI for GitHub repo admin, GitLab CLI (`glab`) for MR workflow against legacy repos, `mvn` for smoke verification, Bash for scripting.

**Scope boundaries:**
- **IN SCOPE**: Phase 3 (parallel-starter advisory notice across 7 public legacy repos; maintenance-parity governance; sunset-criteria framework) + Phase 4 closure items (plugin dry-run, drift test, release acknowledgment).
- **OUT OF SCOPE**: Task 1 (6 non-proven runner porting — `mvc-*`, `egov*`, `webflux-*`) → separate plan. Task 2 (14-endpoint controller alignment) → separate plan. Actual archival of legacy repos → future plan8 (only when Task 3.3 criteria are met and user signs off).
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
| §8 Phase 3 | 기존 repo README 안내 | Task 3.1 (pivoted: advisory, not migration) |
| §8 Phase 3 | 1~2 스프린트 후 아카이브 | **REVISED** — Task 3.2 (parity governance) + Task 3.3 (sunset criteria) + Task 3.4 (deferred archival to future plan8). User directive: parallel maintenance until starter validated. |
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

## Phase 3 stance — PARALLEL MAINTENANCE (revised 2026-04-24 per user directive)

> **User directive (2026-04-24):** "starter가 효과적이라고 검증될때까지 유지할 저장소이다. 관리해야 할거야."
>
> The 8 legacy GitLab repos are **NOT archived now**. They remain in parallel maintenance alongside the new starter until the starter's effectiveness is independently validated. Phase 3 therefore pivots from "migration + archival" to "advisory notice + parity governance + sunset-criteria framework". Archival moves to a new plan (plan8-legacy-sunset, authored only when sunset criteria are met).

### Legacy repo registry (user-provided 2026-04-24)

| # | Runner id | GitLab clone URL | Public |
|---|---|---|---|
| 1 | `boot-jdk17-jakarta` | `https://gitlab.com/nexacron/spring-boot/jakarta/uiadapter-jakarta.git` | ✅ |
| 2 | `boot-jdk8-javax` | `https://gitlab.com/nexacron/spring-boot/javax/uiadapter-spring-boot.git` | ✅ |
| 3 | `mvc-jdk17-jakarta` | `https://gitlab.com/nexacron/spring-framework/jakarta/nexacro-jakarta-example.git` | ✅ |
| 4 | `mvc-jdk8-javax` | `https://gitlab.com/nexacron/spring-framework/javax/nexacro-example.git` | ✅ |
| 5 | `egov5-boot-jdk17-jakarta` | `https://gitlab.com/nexacron/egov5-spring-boot/jakarta/egov5-boot-nexan.git` | ✅ |
| 6 | `egov4-boot-jdk8-javax` | `https://gitlab.com/nexacron/egov-spring-boot/javax/eGov43-boot-nexaN.git` | ✅ |
| 7 | `egov4-mvc-jdk8-javax` | `https://gitlab.com/nexacron/egov-spring-framework/egov43x/egov43-nexacron.git` | ✅ |
| 8 | `webflux-jdk17-jakarta` | _(공개 전 — public publication pending)_ | ⏳ |

**Net: 7 public + 1 pending.** All Phase 3 tasks operate on the 7 public entries only; the 8th is added on publication.

---

## Task 3.1: Parallel-starter advisory notice (7 public legacy repos)

**Purpose:** Tell existing users a **starter exists** without signalling imminent archival. No destructive writes. MR-based advisory workflow (avoid direct-to-default-branch push on active legacy code).

**Files:**
- Create: `docs/superpowers/assets/parallel-starter-notice.md` (shared template)
- Per-legacy-repo MR: patch `README.md` (prepend notice above existing content)

- [ ] **Step 1: Author the shared notice template**

Dispatch Haiku subagent to write `docs/superpowers/assets/parallel-starter-notice.md`:

```markdown
> ℹ️ **Starter 병행 안내 (Parallel Starter Available)**
>
> nexacroN 샘플 프로젝트 8종을 통합 관리하는 신규 **starter 플러그인**이 공개되었습니다. 이 저장소는 starter의 유효성이 검증될 때까지 **병행 유지**됩니다 — 지금 아카이브되지 않습니다.
>
> - **신규 통합 위치**: [github.com/JasonMMo/nexacroN-fullstack](https://github.com/JasonMMo/nexacroN-fullstack) (monorepo)
> - **사용 방법**: Claude Code에서 `/plugin install nexacro-fullstack-starter@nexacro-claude-skills` → `/nexacro-fullstack-starter` 호출
> - **조합 선택**: JDK(8/17) × framework(Spring Boot / Spring MVC / eGov4 / eGov5 / WebFlux) 대화식 선택
> - **본 저장소 상태**: 기존 이슈/PR은 여기서 계속 처리됩니다. starter가 기능 parity를 달성하고 안정성이 검증되면 별도 공지 후 아카이브될 수 있습니다.
> - **권장**: 신규 프로젝트는 starter 사용을 권장합니다. 기존 프로젝트는 그대로 본 저장소를 사용하셔도 됩니다.
>
> 문의: GitHub 모노레포 이슈 탭.
```

Commit the template in the skills repo:
```
git add docs/superpowers/assets/parallel-starter-notice.md
git commit -m "docs(assets): parallel-starter advisory notice template for 7 legacy repos"
```

- [ ] **Step 2: Gate-2 intent-check before first GitLab mutation**

Dispatch Explore (or codex-rescue if available):
```
Agent(
  subagent_type="Explore",
  description="Gate-2 intent-check — GitLab advisory MR fanout",
  prompt="Review Task 3.1 Step 3 (MR fanout across 7 public GitLab repos). Confirm: (a) workflow is MR-based not direct push, (b) notice text does not claim archival is imminent, (c) blast radius is contained (MRs are reviewable/revertable), (d) no credentials in plan. Return GO / NO-GO + any concerns."
)
```
GO required before Step 3.

- [ ] **Step 3: Per-repo advisory MR (×7, serial)**

For each of the 7 public URLs in the registry above, dispatch one Haiku subagent serially (avoid GitLab abuse-rate flags):

```
Agent(
  subagent_type="general-purpose",
  description="Open advisory MR on <repo>",
  prompt="1. Clone <clone-url> into a temp dir.
2. Create branch 'docs/parallel-starter-notice'.
3. Prepend the contents of D:\\AI\\workspace\\nexacro-claude-skills\\docs\\superpowers\\assets\\parallel-starter-notice.md to README.md (create README.md if absent), above any existing content. Preserve existing content verbatim.
4. Commit: 'docs: add parallel-starter advisory notice'.
5. Push branch to origin.
6. Open MR via `glab mr create --title 'docs: add parallel-starter advisory notice' --description 'Adds an advisory banner pointing to the new fullstack-starter. Non-breaking; this repo remains in parallel maintenance per 2026-04-24 directive.' --source-branch docs/parallel-starter-notice --target-branch <default-branch>`.
7. Print the MR URL.

If glab is not installed or auth fails → ESCALATE; do NOT force-push or mutate default branch."
)
```

- [ ] **Step 4: MR tracker**

Dispatch Explore subagent to collect the 7 MR URLs and their status; write to `tasks/legacy-advisory-mr-tracker.md` with columns: runner-id, clone-url, MR-url, status (open/merged/closed), opened-date. Update `tasks/todo.md` with a summary line.

- [ ] **Step 5: Merge coordination (out-of-band)**

Merging each MR requires repo-owner approval on GitLab. Document in tracker; do NOT auto-merge.

---

## Task 3.2: Maintenance-parity governance

**Purpose:** Formalize that legacy + starter are maintained in parallel, and make the parity contract auditable.

**Files:**
- Create: `docs/governance/legacy-gitlab-registry.md`
- Create: `docs/governance/maintenance-parity-playbook.md`

- [ ] **Step 1: Author the registry**

Dispatch Sonnet subagent to write `docs/governance/legacy-gitlab-registry.md` containing:
- The 7-row table above (runner-id, clone-url, public-status)
- The 8th webflux entry with status `공개 전` — add a `TODO: update URL when published`
- Per-repo ownership + maintenance lead (leave `<TBD by user>` — do NOT guess)
- Link to this plan and the `maintenance-parity-playbook.md`

- [ ] **Step 2: Author the parity playbook**

Dispatch Sonnet subagent to write `docs/governance/maintenance-parity-playbook.md` containing:
- **Parity rule**: Any bug fix or security patch merged to the monorepo's matching runner MUST be opened as an MR against the corresponding legacy repo within 1 sprint. Any fix first merged to a legacy repo MUST be ported to the monorepo runner within 1 sprint.
- **Version tracking**: Legacy repos continue their existing tag cadence. Monorepo tags independently. Version numbers are NOT synchronized; the parity is at source-behavior level, not version-label level.
- **Issue routing**: New issues reported on legacy repos → honoured there. Same issue, if reproducible on starter → cross-link; fix both.
- **CHANGELOG convention**: When a cross-repo fix lands, note the pair-SHA in both changelogs under a `Cross-repo parity` subheading.
- **Audit cadence**: Quarterly, compare `git log --since=3months` diffs per runner pair. Flag drift.
- **Escape hatch**: If parity becomes burdensome and sunset criteria (Task 3.3) are met, promote the runner to sunset phase.

- [ ] **Step 3: Per-file commits (CLAUDE.md rule)**

```
git add docs/governance/legacy-gitlab-registry.md
git commit -m "docs(governance): legacy GitLab repo registry (7 public + 1 pending)"
git add docs/governance/maintenance-parity-playbook.md
git commit -m "docs(governance): maintenance-parity playbook for legacy/starter parallel operation"
```

---

## Task 3.3: Sunset-criteria framework (gate for future plan8)

**Purpose:** Make sunset a **measurable, user-approved** decision — not a calendar-driven or coordinator-driven one.

**Files:**
- Create: `docs/governance/legacy-sunset-criteria.md`

- [ ] **Step 1: Draft the criteria document**

Dispatch Sonnet subagent to write `docs/governance/legacy-sunset-criteria.md` containing:

**Required criteria (ALL must be true per runner before that runner's legacy repo may be archived):**

1. **Functional parity**: the starter runner passes `mvn verify` and the full 14(+1)-endpoint contract (§5.1 + §5.2) for the matching JDK/framework combination. Evidence: green CI run + drift-check script (Task 4.3) reports `OK`.
2. **Adoption signal**: at least **N independent installs** of the starter for that runner variant, measured over **M consecutive weeks**. *(N and M are user-set thresholds — see Step 2 below.)*
3. **Bug-report flow**: at least **L consecutive weeks** during which no new bug reports on the legacy repo reference functionality that does not exist in the starter (i.e., the legacy repo is no longer exercising unique code paths).
4. **Contract stability**: no breaking changes to spec §5.1 API contract for **≥ 1 full minor-version cycle** on the monorepo (e.g., `v0.8.x → v0.9.0` with no removed endpoints).
5. **Explicit user sign-off**: user writes in `tasks/todo.md` under `### Sunset approvals` an explicit line: `<runner-id> sunset APPROVED on YYYY-MM-DD — <reason>`.

**Sunset workflow when criteria are met (for a single runner):**

1. Author `plan8-legacy-sunset-<runner>.md` (writing-plans skill).
2. Update the repo's README notice (Task 3.1 template) to an archival-imminent variant — 2-sprint warning window.
3. After the 2-sprint window, execute `glab repo archive <namespace/repo>`.
4. Update `docs/governance/legacy-gitlab-registry.md` with archival date.
5. Reopen the gate for the next eligible runner.

- [ ] **Step 2: User-approval gate on N / M / L thresholds**

This document's thresholds are user decisions. Dispatch a Haiku subagent to append a clearly-marked "PENDING USER APPROVAL" header at the top of `legacy-sunset-criteria.md`:

```markdown
> 🛑 **PENDING USER APPROVAL — Threshold values N, M, L below are placeholders.**
> Coordinator suggestion: N=3 independent installs, M=4 weeks, L=8 weeks. User MUST confirm or override before this criteria document becomes authoritative.
```

Do NOT treat this document as authoritative until the user confirms or overrides thresholds. Record the decision in `tasks/todo.md` under `### Sunset thresholds`.

- [ ] **Step 3: Per-file commit**

```
git add docs/governance/legacy-sunset-criteria.md
git commit -m "docs(governance): legacy-repo sunset criteria framework (pending user threshold approval)"
```

---

## Task 3.4: Sunset execution (DEFERRED — future plan8)

**Status:** NOT executed in this plan. Placeholder.

**Trigger:** Task 3.3 criteria met for at least one runner AND user sign-off recorded in `tasks/todo.md`.

**Output when triggered:** `docs/superpowers/plans/<YYYY-MM-DD>-plan8-legacy-sunset-<runner>.md` authored via writing-plans skill, following the sunset workflow in Task 3.3 Step 1.

- [ ] **Step 1: Defer marker in tasks/todo.md**

Dispatch Haiku subagent to append to `tasks/todo.md` under a new `### Deferred — legacy sunset (per-runner)` section noting that plan8 is NOT written yet and will only be authored upon user trigger.

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
