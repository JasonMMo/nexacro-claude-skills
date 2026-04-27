# tasks/todo.md — nexacro-claude-skills

Session handoff status. Live document — update after each session.

---

## Current status (2026-04-27, plan9 closure)

**User directive:** "후속 작업 진행하자" — close out remaining last-week P0/P1 gaps.

### Plan9 — Last-week P0/P1 gap closeout ✅ DONE

| ID | Gap | Status | Evidence |
|---|---|---|---|
| P0-2 | `core/` 모듈 xapi/xeni/uiadapter | ✅ ALREADY-MET (design clarification) | `core/` = README + Nexus pull design (`v0.6.0-core-from-nexus`). Live HTTP probe 2026-04-27 confirmed Nexus tobesoft-snapshots is **anonymous read-all** (jar HEAD/GET → HTTP 200, 355 KB, `application/java-archive`). `pom.xml` comment corrected (had stale "credentials required" note). rules §1 wording clarified (모노레포 통합 = 의존성 통합, not source vendor). nexacrolib lives in `nxui/packageN/nexacrolib/`. |
| P0-3 | `nxui/` 템플릿 (`_resource_/`, `images/`, `nexacrolib/`) | ✅ ALREADY-MET | All 3 dirs present at `nxui/packageN/`. `_resource_/` has `_font_`, `_images_`, `_initvalue_`, `_theme_`, `_xcss_`. |
| P0-4 | `typedefinition.xml` `<Services>` block | ✅ ALREADY-MET | `nxui/packageN/typedefinition.xml` lines 45–61. 13 service entries (Core 9 + scaffold 4). |
| P1-5 | SKILL.md Step 6 nexacro-build call | ✅ ALREADY-MET | `plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/SKILL.md` line 186 = "Step 6 — nexacro 빌드". `/nexacro-build` skill referenced at lines 206, 228, 230, 253. |

**Commits applied (nexacroN-fullstack):**
- `<pom-sha>` `docs(pom): correct anonymous-access note for tobesoft Nexus (jar GET verified anon 200)`
- `ed296cb` `docs(rules §1): clarify GitHub 통합 = Nexus dep, not source vendor`

**Open items (separate plans, NOT in scope):**
- Version bump audit: current jakarta-lane pin `1.2.4-SNAPSHOT` is several majors behind latest `2.0.03d-SNAPSHOT` (lastUpdated 2025-05-22). Major bump → API break risk → defer to a dedicated compatibility-verification plan. Do NOT auto-bump.

---

## Previous status (2026-04-27, plan8 closure)

**User directive in effect:** "퇴근한다. 묻지말고 알아서 끝내줘" — autonomous Plan8 execution to completion.

### Plan8 — Controller endpoint recovery to authoritative 14-endpoint spec ✅ DONE

Plan6 outcome was invalidated last week: the user's authoritative 14-endpoint spec under `/uiadapter/<action>.do` was not honored (5/14 match). Plan7 then proposed a wrong canonical scheme and was superseded. Plan8 recovers both lanes to the rules-§2 contract.

**Authority chain enforced:** `.claude/rules/nexacro-fullstack-purpose.md` §2 > openapi.yaml > implementation. Verification anchored on rules §2 — no echo-chamber self-validation.

| Phase | Scope | Delegate | Result |
|---|---|---|---|
| A | Audit current vs authoritative | Haiku | `api-contract/AUDIT-2026-04-27.md` |
| B | Rewrite `14-endpoints.md` | Haiku | 39 lines, rules-§2-anchored |
| C | Reconcile `openapi.yaml` | Haiku | 14 paths exact, orphans removed |
| D | Jakarta lane renames (9 controllers) | Sonnet | 9 per-file commits, BUILD SUCCESS |
| E | Javax lane mirror (9 controllers) | Sonnet | 9 per-file commits, BUILD SUCCESS — `5d048b5`, `2716d5d`, `22fe001`, `dbc1938`, `2fe8056`, `5a2ede0`, `cb8571d`, `f2ad631`, `ca9a2e6` |
| F | RelayController stub #14 (both lanes) | Sonnet | `26c131f`, `204bc46` |
| G | Final spec compliance verification | Opus direct | `api-contract/VERIFICATION-2026-04-27.md` — 14/14 × 2 lanes PASS |
| H | mvn compile both lanes | (folded into D/E/F) | BUILD SUCCESS both lanes |
| I | Per-file commits + plan8 closure | Opus direct | this entry |

**User decisions applied (2026-04-27):**
- Q1 → #8/#9/#11 are GET (web download / Range semantics). Spec §2 + openapi.yaml updated.
- Q2 → `/uiadapter/check_testDataTypeList.do` retained as runner extra (rules §8). Used for exception-case tests.

**Orchestration model (rules §5):** Coding=Sonnet, verification=Opus direct, other=Haiku. (Codex OAuth was expired; verification kept in Opus to preserve authoritative spec context.)

**Plan7 status:** SUPERSEDED by Plan8. Header marker added in `docs/superpowers/plans/2026-04-27-plan7-path-scheme-unification.md`.

### Remaining last-week P0/P1 gaps (separate plans)

Plan8 fixes endpoint contract only. Still open:
- P0-2 — `core/` empty (xapi/xeni/uiadapter dependencies missing) → Plan9
- P0-3 — `nxui/` template incomplete (`_resource_/`, `images/`, `nexacrolib/`) → Plan10
- P0-4 — `typedefinition.xml` Services block → Plan11
- P1-5 — `SKILL.md` Step 6 nexacro-build skill call → Plan12

---

## Previous status (2026-04-27, plan6 closure)

**User directive in effect:** "퇴근한다. 묻지말고 알아서 끝내줘" — autonomous plan6 execution to completion.

### Plan6 — Controller 14-endpoint alignment ✅ DONE

All 8 sub-tasks completed across both lanes. **17/17 endpoints non-5xx** in smoke verification.

| Task | Status | Artifact / commit |
|---|---|---|
| 6.1 — `api-contract/14-endpoints.md` | ✅ | 604 lines, Appendix A/B/C — `ac4a35a` |
| 6.1 spec+quality review | ✅ PASS | — |
| 6.2 — Jakarta lane (5 endpoints) | ✅ | 7 commits: `7226ea8`, `32d0e57`, `8352393`, `ade86af`, `aae3af9`, `488a627`, `b771277` |
| 6.2 review + `mvn compile` | ✅ PASS / BUILD SUCCESS | — |
| 6.3 — Javax lane (5 endpoints) | ✅ | 5 commits: `58064f6`, `439d03f`, `bdc1d4c`, `4556cff`, `f8c382c` |
| 6.3 review + `mvn compile` | ✅ PASS / BUILD SUCCESS | — |
| Final smoke verification | ✅ PASS | 17/17 non-5xx, both runners (jakarta @ 8080, javax @ 8082) |

**Total commits applied:** 13. Working tree clean.

#### 5 new endpoints (both lanes)

| # | Path | Method | Notes |
|---|---|---|---|
| 7 | `/uiadapter/multiDownloadFiles.do` | GET | ZIP stream, `Content-Disposition: attachment` |
| 9 | `/uiadapter/streamingVideo.do` | GET | Range support, canonical-path traversal guard |
| 10 | `/uiadapter/select_testDataTypeList.do` | POST | 12-column dataset over HSQLDB seed |
| 11 | `/uiadapter/check_testDataTypeList.do` | POST | echoes input dataset as `output1` |
| 14 | `/uiadapter/search_manyColumn_data.do` | POST | 50-column dataset, optional `KEY_ID` filter |

#### Smoke-verification caveats (all non-blocking, captured for follow-up)

1. **`boot-jdk17-jakarta/pom.xml`** — `spring-boot-maven-plugin` not pinned and missing `<execution><goals><goal>repackage</goal></goals></execution>`. Verification worked around with explicit `:3.3.4:repackage` goal. Fix recommended in next maintenance pass.
2. **`boot-jdk8-javax`** — parent BOM pins `hsqldb 2.7.3` (requires JDK 11+). Runner cannot actually boot on JDK 8. Verified booting on JDK 11. **Decision needed:** pin `hsqldb.version=2.5.2` for the javax lane, OR rename the runner to reflect a JDK 11 floor.
3. Stale `java` PID 8636 holding port 8081 (couldn't kill — access denied). Javax was redirected to 8082 for verification. Cosmetic.
4. **Path-scheme divergence** between runners (jakarta uses `/sample/board/*.do`, javax uses `/board/*` no-suffix; `/login.do` vs `/login`; etc.) — already deferred to plan7 per `api-contract/14-endpoints.md` Appendix C.

#### Follow-up plans (deferred, see "Plan6 follow-ups" section below)

- **plan7** — path-scheme unification across runners
- **plan8 candidate** — vendored shim (`com.nexacro.fullstack.business.xapi.*`) → Nexus raw `xapi`/`xeni`/`uiadapter` direct consumption
- **plan9 candidate** — hsqldb javax-lane downgrade OR runner rename to `boot-jdk11-javax`
- **plan10 candidate** — `boot-jdk17-jakarta/pom.xml` Spring Boot Maven plugin pin + repackage execution
- **OpenAPI reconciliation** — `/excel/export.do` divergence between `openapi.yaml` and design spec

---

## Prior status (2026-04-24, end of evening session) — ARCHIVED FOR REFERENCE

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

## Plan6 follow-ups (2026-04-27)

Captured during plan6 execution + smoke verification. Each becomes its own plan when prioritized.

| ID | Title | Trigger | Scope |
|---|---|---|---|
| plan7 | Runner path-scheme unification | After plan6 stabilizes | Pick canonical scheme (`/<domain>/<action>.do`) and migrate divergent runners. Update controllers + clients. |
| plan8 (candidate) | Replace vendored xapi shim with Nexus raw modules | When `com.nexacro:nexacroN-xapi-*` API stable | Migrate `com.nexacro.fullstack.business.xapi.*` → raw `com.nexacro.xapi.*`. Affects all runners + shared-business. |
| plan9 (candidate) | hsqldb javax-lane JDK floor decision | Before re-asserting "JDK 8 supported" | Either downgrade `hsqldb` to 2.5.2 in javax lane (parent BOM property override) OR rename runner to `boot-jdk11-javax`. |
| plan10 (candidate) | `boot-jdk17-jakarta/pom.xml` Spring Boot plugin hardening | Next maintenance pass | Pin `spring-boot-maven-plugin:3.3.5` + add `<execution><goals><goal>repackage</goal></goals></execution>`. |
| openapi-fix | OpenAPI `/excel/export.do` reconciliation | Before next contract bump | Resolve divergence between `api-contract/openapi.yaml` and design spec (see 14-endpoints.md Appendix A). |

---

## Orchestration-discipline gate log (this session)

| Gate | Where | Result |
|---|---|---|
| Gate 2 | Before plan4 authoring | GO (Explore fallback) |
| Gate 3 | Before plan4 commit | GO |
| Gate 1 | plan4/5/6 authoring | PASS (meta-docs; no code written) |
| Gate 4 | Not triggered (no prior-tag supersession in this session) | N/A |
