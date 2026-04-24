# Controller 14-Endpoint Contract Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: `superpowers:subagent-driven-development`. Bound by `orchestration-discipline` 4 gates.

**Goal:** Align every runner's controllers to the spec §5.1 common 14-endpoint contract (currently only 5 controllers exist across proven runners). Ensure identical API surface so the same `packageN` nxui works against any runner.

**Architecture:** The 14 common endpoints live as `@RestController` methods on shared controller classes inside each runner's controller package. Boot/MVC runners share signatures; WebFlux runner wraps return types in `Mono`/`Flux`. The controllers delegate to shared-business services — controller code is just HTTP framing.

**Tech Stack:** Spring `@RestController` (MVC/Boot), `@RestController` + `WebFlux` (reactive), `NexacroDataSet`/`NexacroResult` transport types (from xapi), existing shared-business services + mappers.

---

## Prerequisite

- [ ] **P.1** Dispatch Explore subagent to extract the exact 14 endpoint signatures from spec §5.1 and any openapi.yaml if present at `api-contract/openapi.yaml` in the monorepo. Produce `tasks/api-contract-14-endpoints.md` listing for each endpoint: HTTP verb, path, request dataset name/columns, response dataset name/columns, error cases. This document is the single source of truth for alignment.

- [ ] **P.2** Dispatch Explore subagent to audit the CURRENT implemented endpoints in the two proven runners (`samples/runners/boot-jdk17-jakarta` + `samples/runners/boot-jdk8-javax`). Produce `tasks/api-contract-current-state.md` showing which of the 14 are implemented and which are missing. Expected gap: ~9 missing per runner (survey said 5 present).

Gate 2 (intent-check) between P.1/P.2 and Task 6.1: independent reviewer confirms the 14-endpoint list matches spec §5.1 verbatim. If openapi.yaml disagrees with spec, ESCALATE — do not silently pick one.

---

## Task 6.1: Extract shared controller signatures

**Purpose:** Define the 14-endpoint contract as a shared set of `@interface`-like marker artifacts so each runner implements the same shape.

**Files:**
- Create (optional, if user approves API-contract module): `api-contract/src/main/java/com/nexacro/fullstack/contract/NexacroApi.java` — 14 abstract methods with full `@RequestMapping` / `@PostMapping` annotations, request/response types.

- [ ] **Step 1**: Dispatch Sonnet subagent to either:
  - (a) author the `NexacroApi` interface as a new module `api-contract/` in the monorepo, OR
  - (b) document the 14 signatures as a markdown reference only (no Java module)

  Default to (b) unless the user has previously requested a shared interface module. A Java interface forces compile-time contract alignment but adds a new monorepo module — intent-check with user before doing (a).

- [ ] **Step 2**: Spec-compliance review against `tasks/api-contract-14-endpoints.md`.

- [ ] **Step 3**: Per-file commits.

---

## Task 6.2: Implement missing endpoints — `boot-jdk17-jakarta`

**Files:**
- Modify: `samples/runners/boot-jdk17-jakarta/src/main/java/com/nexacro/fullstack/runner/boot17/controller/*.java`
  - Likely new files: expand from 5 to 14 endpoints. Group by business domain (login, board, dept, large-data, file, plus the missing 9).

**Steps (canonical, repeats per runner):**

- [ ] **Step 1**: Sonnet subagent dispatch. Prompt must include:
  - Full `tasks/api-contract-14-endpoints.md`
  - Current controller file list
  - Shared-business service/mapper catalog for `shared-business/jdk17-jakarta`
  - Instruction: for each missing endpoint, locate the corresponding shared-business service method. If the service does not exist yet, HALT and escalate (shared-business authoring is out of scope for this plan — belongs in a follow-up plan7 or equivalent).

- [ ] **Step 2**: `mvn -pl samples/runners/boot-jdk17-jakarta -am compile` → BUILD SUCCESS.

- [ ] **Step 3**: Unit smoke: Haiku subagent runs `mvn -pl samples/runners/boot-jdk17-jakarta spring-boot:run` in background, curls each of the 14 endpoints with fixture payloads, asserts non-5xx. Produce `tasks/controller-smoke-boot-jdk17-jakarta.log`.

- [ ] **Step 4**: Spec-compliance review against §5.1.

- [ ] **Step 5**: Code-quality review.

- [ ] **Step 6**: Per-file commits.

---

## Task 6.3: Implement missing endpoints — `boot-jdk8-javax`

Same shape as 6.2 with:
- `shared-business/jdk8-javax` as backing tree
- javax-flavoured imports (`javax.servlet.*`)
- Spring Boot 2.7 / MVC 5 signatures

---

## Task 6.4 through 6.8: One task per `mvc-*`, `egov*`, `webflux-*` runner

Deferred to after plan5 (six-runner porting) completes. Template identical to 6.2/6.3 except:
- **mvc runners**: classic `@Controller` + war packaging, same 14 signatures
- **egov runners**: may add eGov-specific annotations (e.g., `@RequestMapping` on egov RestMapper base class if present in shared-business-egov*)
- **webflux-jdk17-jakarta**: signatures return `Mono<NexacroResult>` or `Flux<NexacroRow>` — this is the §5.2 "WebFlux 전용 + 대체 구현" endpoint variance. Verify the spec's 15th endpoint (webflux-only) is implemented here.

Each runner gets its own independent subagent task with full two-stage review.

---

## Dependency / Scheduling

```
P.1, P.2  →  6.1  →  6.2 (jakarta-boot proven) ↗  6.4..6.8 (blocked by plan5)
                 ↘  6.3 (javax-boot proven)  ↗
```

- 6.2 and 6.3 can run in parallel **only if** no shared file is touched in both (controller packages are disjoint — safe).
- 6.4–6.8 require the respective runners from plan5 to be compiling first.

---

## Release Binding

On completion of ALL 6.2–6.8 tasks:
- Aggregate release notes: `docs/releases/v1.9.0.md` citing spec acceptance §11.1, §11.2, §11.3.
- Monorepo tag: `v0.8.0-contract-complete`.
- Skills tag: `v1.9.0`.
- Gate 3 pre-tag verification mandatory.
- Deletes the "DEFERRED" marker in plan4 Task 4.4.

---

## Gate Enforcement

- **Gate 1**: Opus plans; Sonnet executes; Explore/codex reviews.
- **Gate 2**: Pre-dispatch intent-check for each runner task confirming its 14 signatures match the master contract doc.
- **Gate 3**: Pre-tag independent verification before `v1.9.0`.
- **Gate 4**: If any earlier tag's contract claim is invalidated (e.g., plan2/plan3 claimed 5 endpoints cover "common contract" but spec demands 14), update lessons.md and retrospect before proceeding.

---

## Out of Scope

- Authoring new shared-business service methods — if an endpoint has no backing service, ESCALATE.
- WebFlux reactive mapper conversion (R2DBC) — spec §1.3 non-goal.
- Spring Security — spec §1.3 non-goal.
- nxui integration smoke — Phase 4 plan4 scope.

---

## Self-Review

- [x] 14-endpoint source of truth artifact specified
- [x] Per-runner task structure explicit
- [x] Parallelisation rules stated
- [x] Escalation triggers named (missing services, spec↔openapi disagreement)
- [x] Release tagging gated on codex (Gate 3)
- [x] Task 1 dependency (plan5) tracked

---

## Execution Handoff

Recommended: `superpowers:subagent-driven-development`. Start with P.1 + P.2 serially, then 6.1, then 6.2/6.3 (in parallel if file-disjoint), then block on plan5 for 6.4–6.8.
