# tasks/todo.md — nexacro-claude-skills

Session handoff status. Live document — update after each session.

---

## Current status (2026-04-24, end of afternoon session)

**User directive in effect:** "3번 - 1번 - 2번 순서로 진행하자" (proceed Task 3 → Task 1 → Task 2).

### Task 3 — Design-spec plan creation ✅ DONE

- Plan artifact committed: `docs/superpowers/plans/2026-04-24-plan4-phase3-phase4-closure.md`
- Commit: `2d0ac0f`
- Scope: Phase 3 (GitLab archival) + Phase 4 closure (verification scripts, deferred v1.9.0 tag)
- Gate 2 intent-check: Explore-subagent fallback (codex-rescue unavailable) — GO
- Gate 3 pre-commit verification: Explore — GO with 3 non-blocking observations

### Task 1 — Six runner porting ⏸ PLAN READY, EXECUTION BLOCKED (partial)

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

## Scheduled — GitLab archival (plan4 Task 3.2)

Blocking: plan4 Task 3.1 must complete first (migration-notice README patch on 8 legacy repos).
Earliest archival execution: 2 sprints after Task 3.1 completion.

---

## Deferred — v1.9.0 closure tag (plan4 Task 4.4)

Trigger: Tasks 1 + 2 both merged with their own release notes.
Pre-requisites before tagging:
- rerun plan4 Task 4.1 (codex-rescue or Explore fallback)
- rerun plan4 Task 4.3 (drift-check should be 8/8 OK; currently 2/8 expected)
- author `docs/releases/v1.9.0.md` citing spec acceptance §11.1–§11.5 fully met
- Gate 3 verification required before push

---

## Open questions for user

1. Task 1 blocker decision (a / b / c above).
2. Task 2's plan6 Task 6.1 optional path (shared `NexacroApi` Java interface module vs. markdown-only contract doc) — default is markdown unless user prefers compile-time contract enforcement.
3. GitLab legacy repo namespace confirmation (plan4 Task 3.1 Step 1) — glab query will list candidates but user should validate the slug pattern.

---

## Orchestration-discipline gate log (this session)

| Gate | Where | Result |
|---|---|---|
| Gate 2 | Before plan4 authoring | GO (Explore fallback) |
| Gate 3 | Before plan4 commit | GO |
| Gate 1 | plan4/5/6 authoring | PASS (meta-docs; no code written) |
| Gate 4 | Not triggered (no prior-tag supersession in this session) | N/A |
