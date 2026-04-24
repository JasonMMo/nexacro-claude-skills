# tasks/todo.md — nexacro-claude-skills

Session handoff status. Live document — update after each session.

---

## Current status (2026-04-24, end of evening session)

**User directive in effect:** "3번 - 1번 - 2번 순서로 진행하자" (proceed Task 3 → Task 1 → Task 2).

### Task 3 — Design-spec plan creation ✅ DONE

- Plan artifact committed: `docs/superpowers/plans/2026-04-24-plan4-phase3-phase4-closure.md`
- Commit: `2d0ac0f`
- Scope: Phase 3 (GitLab archival) + Phase 4 closure (verification scripts, deferred v1.9.0 tag)
- Gate 2 intent-check: Explore-subagent fallback (codex-rescue unavailable) — GO
- Gate 3 pre-commit verification: Explore — GO with 3 non-blocking observations

### Task 1 — Runner porting (scoped to 2 MVC runners per user decision) ⏸ PLAN READY, EXECUTION PENDING

- Plan artifact committed: `docs/superpowers/plans/2026-04-24-plan5-six-runner-porting.md` (`7674c75`)
- Prerequisite P.1 scan result:
  - ✅ `samples/shared-business/jdk17-jakarta/` — pom + src present
  - ✅ `samples/shared-business/jdk8-javax/` — pom + src present
  - 🛑 `samples/shared-business-egov4/jdk8-javax/` — empty directory (no pom, no src)
  - 🛑 `samples/shared-business-egov5/jdk17-jakarta/` — empty directory
  - 🛑 `samples/shared-business-reactive/jdk17-mybatis/` — empty directory
- **Unblocked (2/6)**: `mvc-jdk17-jakarta`, `mvc-jdk8-javax` (Tasks 5.1 and 5.2 in plan5) — can dispatch immediately.
- **Blocked (4/6)**: `egov5-boot-jdk17-jakarta`, `egov4-boot-jdk8-javax`, `egov4-mvc-jdk8-javax`, `webflux-jdk17-jakarta` — require shared-business-egov4/egov5/reactive authoring first.
- **Blocker resolution options** for user decision:
  - (a) author the 3 missing shared-business trees (new plan7) before Task 5.3–5.6
  - (b) re-scope Task 1 to the 2 unblocked runners only, defer egov/webflux to follow-up
  - (c) pivot the 4 blocked runners to reuse `samples/shared-business/jdk{17,8}-*` (drop the egov-/reactive-specific business split) — requires spec amendment

### Task 2 — Controller 14-endpoint alignment ⏸ PLAN READY

- Plan artifact committed: `docs/superpowers/plans/2026-04-24-plan6-controller-14-endpoint-alignment.md` (`001d78f`)
- Prerequisites reusable: `api-contract/openapi.yaml` exists in monorepo (single source of truth, per plan6 P.1).
- Current endpoint count: 5 per proven runner (LoginController, BoardController, DeptController, LargeDataController, FileController).
- Expected gap: ~9 missing endpoints per runner to reach §5.1's 14-endpoint common contract.
- Depends on: Task 1's unblocked runners being current shape (Task 2 will re-touch them).

---

## Recommended next-session sequence

1. User decision on Task 1 blocker options (a / b / c above).
2. If (b) chosen (2-runner scope): dispatch Sonnet on plan5 Task 5.1 (mvc-jdk17-jakarta), then 5.2 (mvc-jdk8-javax). Expected ~2 hours with reviews.
3. After Task 1 runners compile: begin plan6 (controller alignment) with prerequisites P.1 + P.2.
4. On completion of Tasks 1 + 2: return to plan4 Task 4.4 (deferred v1.9.0 closure tag).

---

## Phase 3 — PARALLEL MAINTENANCE (revised 2026-04-24)

**User directive:** "starter가 효과적이라고 검증될때까지 유지할 저장소이다. 관리해야 할거야."

Legacy repos are NOT archived. Plan4 Phase 3 pivoted from migration+archival to:
- Task 3.1: advisory MR (non-destructive) on 7 public legacy repos
- Task 3.2: maintenance-parity governance (`legacy-gitlab-registry.md` + `maintenance-parity-playbook.md`)
- Task 3.3: sunset-criteria framework (PENDING user approval of N / M / L thresholds)
- Task 3.4: deferred archival (future plan8, user-triggered only)

### Legacy repo registry (7 public + 1 pending)

| # | runner-id | GitLab clone URL | public |
|---|---|---|---|
| 1 | boot-jdk17-jakarta | gitlab.com/nexacron/spring-boot/jakarta/uiadapter-jakarta.git | ✅ |
| 2 | boot-jdk8-javax | gitlab.com/nexacron/spring-boot/javax/uiadapter-spring-boot.git | ✅ |
| 3 | mvc-jdk17-jakarta | gitlab.com/nexacron/spring-framework/jakarta/nexacro-jakarta-example.git | ✅ |
| 4 | mvc-jdk8-javax | gitlab.com/nexacron/spring-framework/javax/nexacro-example.git | ✅ |
| 5 | egov5-boot-jdk17-jakarta | gitlab.com/nexacron/egov5-spring-boot/jakarta/egov5-boot-nexan.git | ✅ |
| 6 | egov4-boot-jdk8-javax | gitlab.com/nexacron/egov-spring-boot/javax/eGov43-boot-nexaN.git | ✅ |
| 7 | egov4-mvc-jdk8-javax | gitlab.com/nexacron/egov-spring-framework/egov43x/egov43-nexacron.git | ✅ |
| 8 | webflux-jdk17-jakarta | _(공개 전)_ | ⏳ |

### Sunset thresholds — PENDING USER APPROVAL

Coordinator suggestion (to be confirmed or overridden by user):
- **N** = 3 independent installs of the starter for a given runner variant
- **M** = 4 consecutive weeks of the N-install window
- **L** = 8 consecutive weeks with no legacy-unique bug reports

### Sunset approvals

_(None yet. Add one line per runner when approved: `<runner-id> sunset APPROVED on YYYY-MM-DD — <reason>`)_

### Deferred — legacy sunset (per-runner)

plan8 is NOT written yet. It is authored per-runner only when Task 3.3 criteria are fully met AND user signs off under `### Sunset approvals`.

---

## Deferred — v1.9.0 closure tag (plan4 Task 4.4)

Trigger: Tasks 1 + 2 both merged with their own release notes.
Pre-requisites before tagging:
- rerun plan4 Task 4.1 (codex-rescue or Explore fallback)
- rerun plan4 Task 4.3 (drift-check should be 8/8 OK; currently 2/8 expected)
- author `docs/releases/v1.9.0.md` citing spec acceptance §11.1–§11.5 fully met
- Gate 3 verification required before push

---

## Resolved decisions (2026-04-24, user)

1. **Task 1 scope** = option (b): restrict to 2 `mvc-*` runners (`mvc-jdk17-jakarta`, `mvc-jdk8-javax`). egov4/egov5/webflux variants DEFERRED until explicit re-request ("egov 환경에서 reactive 기능은 요청 시 추가"). plan5 updated with scope banner; Tasks 5.3–5.6 parked.
2. **plan6 Task 6.1** = default (markdown-only contract doc at `api-contract/14-endpoints.md`). No `NexacroApi` Java interface module. plan6 updated.

## Still open

3. ~~GitLab legacy repo existence + slugs~~ — **RESOLVED 2026-04-24**. User provided 7 public clone URLs (see Phase 3 registry table above); 8th webflux pending publication. Phase 3 pivoted to parallel-maintenance model per user directive.

4. **Sunset thresholds N / M / L** (plan4 Task 3.3 Step 2) — coordinator suggests N=3, M=4 wks, L=8 wks. Awaiting explicit user confirmation or override. Until set, `docs/governance/legacy-sunset-criteria.md` carries a PENDING USER APPROVAL banner.

5. **Task 1 execution** — user-chosen option (b) 2-runner scope. Next-session dispatch: plan5 Task 5.1 (`mvc-jdk17-jakarta`) → Task 5.2 (`mvc-jdk8-javax`).

6. **Task 2 execution** — blocks on Task 1 runners compiling. Then plan6 P.1 + P.2 → 6.1 → 6.2/6.3 (+ 6.4/6.5 for the two mvc runners from plan5).

---

## Orchestration-discipline gate log (this session)

| Gate | Where | Result |
|---|---|---|
| Gate 2 | Before plan4 authoring | GO (Explore fallback) |
| Gate 3 | Before plan4 commit | GO |
| Gate 1 | plan4/5/6 authoring | PASS (meta-docs; no code written) |
| Gate 4 | Not triggered (no prior-tag supersession in this session) | N/A |
