# Controller 14-Endpoint Contract Alignment Implementation Plan

> **Scope decision 2026-04-24 (user):**
> - Task 6.1 path = default (markdown-only contract doc, no `NexacroApi` Java interface module).
> - Runner coverage scope-narrowed to match plan5: Tasks 6.2 (boot-jdk17-jakarta), 6.3 (boot-jdk8-javax), plus Tasks 6.4 (mvc-jdk17-jakarta), 6.5 (mvc-jdk8-javax). Tasks for egov4/egov5/webflux are DEFERRED until those runners are re-opened.

> **For agentic workers:** REQUIRED SUB-SKILL: `superpowers:subagent-driven-development`. Bound by `orchestration-discipline` 4 gates.

**Goal:** Align every runner's controllers to the spec §5.1 common 14-endpoint contract (currently only 5 controllers exist across proven runners). Ensure identical API surface so the same `packageN` nxui works against any runner.

**Architecture:** The 14 common endpoints live as `@RestController` methods on shared controller classes inside each runner's controller package. Boot/MVC runners share signatures; WebFlux runner wraps return types in `Mono`/`Flux`. The controllers delegate to shared-business services — controller code is just HTTP framing.

**Tech Stack:** Spring `@RestController` (MVC/Boot), `@RestController` + `WebFlux` (reactive), `NexacroDataSet`/`NexacroResult` transport types (from xapi), existing shared-business services + mappers.

---

## Implementation directive — legacy source reference + Nexus-resolved module consumption (2026-04-24 user)

> User directive: "endpoint 맞추면서 service 및 serviceImpl 구현할때 gitlab에 있는 소스 참조해서 pom.xml설정에 따라 가져온 xapi, xeni, uiadapter 모듈을 사용하도록 지침을 주고 구현하도록 하고 검증도 진행해."

**Source-of-truth rules for every endpoint implementation:**

1. **Business logic (Controller → Service → ServiceImpl → Mapper) reference source = legacy GitLab repos.**
   Port the logic from the matching legacy repo (see mapping below). Do NOT fabricate service behavior. If a legacy repo lacks the endpoint, ESCALATE to user — do not improvise.
2. **Framework plumbing (NexacroDataSet, NexacroResult, view resolvers, argument resolvers, excel servlet) consumed via Maven-resolved artifacts from tobesoft Nexus** — already declared in v1.8.3 runner pom.xml. DO NOT vendor `xapi` / `xeni` / `uiadapter` source into the monorepo; DO NOT copy framework classes. The runner must resolve them as jar dependencies.
3. **Service / ServiceImpl land in `samples/shared-business/<variant>/` — NOT in the runner module.** The runner's controller is a thin HTTP shim that delegates to `shared-business` services. This matches the existing 5-endpoint structure.
4. **Per-variant sourcing:**

   | Runner | Legacy GitLab reference (service/mapper source) | shared-business tree | Nexus deps |
   |---|---|---|---|
   | `boot-jdk17-jakarta` | `gitlab.com/nexacron/spring-boot/jakarta/uiadapter-jakarta.git` (+ `nexacro-jakarta-example.git` for MVC-layer patterns if needed) | `samples/shared-business/jdk17-jakarta/` | `nexacroN-xapi-jakarta`, `nexacroN-xeni-jakarta`, `uiadapter-jakarta-{core,dataaccess,excel}` |
   | `boot-jdk8-javax` | `gitlab.com/nexacron/spring-boot/javax/uiadapter-spring-boot.git` (+ `nexacro-example.git`) | `samples/shared-business/jdk8-javax/` | `nexacroN-xapi`, `nexacroN-xeni`, `uiadapter-spring-{core,dataaccess,excel}` |

5. **Forbidden patterns:**
   - `<systemPath>` / local jar references in pom.xml (v1.8.2 pattern, superseded)
   - `import com.nexacro.xapi.*` or `com.nexacro.uiadapter.*` classes added as source files under `samples/` (these MUST come from jars)
   - Copy-pasting entire classes from legacy repos without attribution comment citing the source URL + commit SHA
6. **Porting protocol (per endpoint):**
   - Read the legacy controller method + service interface + impl + mapper XML.
   - Copy the **domain logic** (DTOs, SQL, business rules). Attribution header: `// Ported from <legacy-repo>/<path>@<sha> on 2026-04-24`.
   - Adapt framework imports: `javax.*` ↔ `jakarta.*` as needed. Spring MVC 5 ↔ 6 signatures.
   - Register the service bean in the runner's Spring context if the legacy one relied on component-scan paths that differ.
   - Exercise: the endpoint compiles and a smoke curl against the runner returns non-5xx.

**Gate implication:** spec-compliance review (Gate 1 per task) must verify NO framework source was vendored, NO placeholder service methods remain, and every new service method has an attribution comment pointing to the legacy source.

---

## Prerequisite

- [ ] **P.1** Dispatch Explore subagent to extract the exact 14 endpoint signatures from spec §5.1 and any openapi.yaml if present at `api-contract/openapi.yaml` in the monorepo. Produce `tasks/api-contract-14-endpoints.md` listing for each endpoint: HTTP verb, path, request dataset name/columns, response dataset name/columns, error cases. This document is the single source of truth for alignment.

- [ ] **P.2** Dispatch Explore subagent to audit the CURRENT implemented endpoints in the two proven runners (`samples/runners/boot-jdk17-jakarta` + `samples/runners/boot-jdk8-javax`). Produce `tasks/api-contract-current-state.md` showing which of the 14 are implemented and which are missing. Also enumerate existing services in `samples/shared-business/jdk17-jakarta/` and `samples/shared-business/jdk8-javax/` so porting targets are known. Expected gap: ~9 missing per runner (survey said 5 present).

- [ ] **P.3** Dispatch Explore subagent to clone the 4 relevant legacy repos (boot-jakarta, boot-javax, mvc-jakarta example, mvc-javax example) into a temp workspace `C:\tmp\legacy-refs\` and catalog per-repo: (a) service interfaces + impls matching the 14 endpoint domains (board, dept, login, file, large-data, + the missing 9), (b) mapper XMLs, (c) DTOs. Produce `tasks/legacy-source-catalog.md` with per-endpoint mapping: `endpoint → legacy-repo/path/ClassName.java@SHA`. If `glab` or `git clone` fails, ESCALATE — do not proceed to 6.2/6.3 without this catalog.

Gate 2 (intent-check) between P.1/P.2/P.3 and Task 6.1: independent reviewer confirms (a) the 14-endpoint list matches spec §5.1 verbatim, (b) the legacy source catalog covers all 14 endpoints across both jakarta and javax lanes, (c) no framework-class vendoring is being proposed. If openapi.yaml disagrees with spec, ESCALATE. If a legacy repo lacks any of the 14 endpoints, ESCALATE with the specific missing list.

---

## Task 6.1: Extract shared controller signatures

**Purpose:** Define the 14-endpoint contract as a shared set of `@interface`-like marker artifacts so each runner implements the same shape.

**Files:**
- Create (optional, if user approves API-contract module): `api-contract/src/main/java/com/nexacro/fullstack/contract/NexacroApi.java` — 14 abstract methods with full `@RequestMapping` / `@PostMapping` annotations, request/response types.

- [ ] **Step 1**: Dispatch Sonnet subagent with path (b) per user decision 2026-04-24 — document the 14 signatures as a markdown reference at `api-contract/14-endpoints.md` (monorepo). No Java interface module. The markdown is authoritative; runners implement against it without compile-time binding.

- [ ] **Step 2**: Spec-compliance review against `tasks/api-contract-14-endpoints.md`.

- [ ] **Step 3**: Per-file commits.

---

## Task 6.2: Implement missing endpoints — `boot-jdk17-jakarta`

**Files:**
- Modify: `samples/runners/boot-jdk17-jakarta/src/main/java/com/nexacro/fullstack/runner/boot17/controller/*.java`
  - Likely new files: expand from 5 to 14 endpoints. Group by business domain (login, board, dept, large-data, file, plus the missing 9).
- Modify: `samples/shared-business/jdk17-jakarta/src/main/java/.../service/**` + `.../mapper/**` + `src/main/resources/mapper/**/*.xml`
  - Port service interfaces, ServiceImpls, DTOs, mapper XMLs from legacy GitLab repos (per the catalog from P.3). **SHARED-BUSINESS AUTHORING IS IN SCOPE** for this task (scope change 2026-04-24 per user directive). When an endpoint's service does not yet exist in `shared-business/jdk17-jakarta/`, port it from the legacy repo. Only escalate if the legacy repo ALSO lacks it.

**Steps (canonical, repeats per runner):**

- [ ] **Step 1**: Sonnet subagent dispatch. Prompt must include:
  - Full `tasks/api-contract-14-endpoints.md`
  - Full `tasks/api-contract-current-state.md`
  - Full `tasks/legacy-source-catalog.md`
  - Current runner controller file list + current `shared-business/jdk17-jakarta` service list
  - The "Implementation directive" section (legacy-source-ref + Nexus-module-consumption + forbidden patterns)
  - Explicit instruction: (a) for each missing endpoint port the legacy service/impl/mapper per the catalog, (b) add attribution comments `// Ported from <legacy-repo>/<path>@<sha> on 2026-04-24`, (c) adapt javax↔jakarta as needed, (d) NEVER add `com.nexacro.xapi.*` or `com.nexacro.uiadapter.*` classes under `samples/` — those must resolve from jars.

- [ ] **Step 2**: `mvn -pl samples/runners/boot-jdk17-jakarta -am compile` → BUILD SUCCESS. If a compile error references a missing jar class, STOP: the Nexus dep is probably mis-declared; re-check pom.xml vs v1.8.3 baseline. Do NOT add the missing class as source under `samples/`.

- [ ] **Step 3**: Unit smoke: Haiku subagent runs `mvn -pl samples/runners/boot-jdk17-jakarta spring-boot:run` in background, curls each of the 14 endpoints with fixture payloads (payloads captured from legacy-repo integration tests where possible), asserts non-5xx. Produce `tasks/controller-smoke-boot-jdk17-jakarta.log`.

- [ ] **Step 4**: Spec-compliance review against §5.1. Reviewer MUST also verify: (a) every new service method has a legacy attribution comment, (b) no `com.nexacro.xapi` or `com.nexacro.uiadapter` source files appeared under `samples/`, (c) pom.xml still uses bare `groupId:artifactId` (v1.8.3 Nexus pattern), no `<systemPath>`.

- [ ] **Step 5**: Code-quality review.

- [ ] **Step 6**: Per-file commits.

---

## Task 6.3: Implement missing endpoints — `boot-jdk8-javax`

Same shape as 6.2 with:
- `shared-business/jdk8-javax` as backing tree
- javax-flavoured imports (`javax.servlet.*`)
- Spring Boot 2.7 / MVC 5 signatures
- Legacy reference: `gitlab.com/nexacron/spring-boot/javax/uiadapter-spring-boot.git` (+ `nexacro-example.git` for example-layer patterns)
- Nexus artifacts: `nexacroN-xapi`, `nexacroN-xeni`, `uiadapter-spring-{core,dataaccess,excel}` (bare, no `-jakarta` suffix)
- Same "Implementation directive" rules apply: NO framework-class vendoring; attribution comments mandatory; service/impl/mapper ported from legacy under `samples/shared-business/jdk8-javax/`.

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
