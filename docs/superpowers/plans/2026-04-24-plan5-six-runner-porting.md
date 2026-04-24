# Runner Porting Implementation Plan (Scoped: 2 MVC runners)

> **Scope update 2026-04-24 (user decision):** Option (b) — Task 1 restricted to the 2 `mvc-*` runners. eGov and WebFlux variants **deferred until explicit user request** (egov environment에서 reactive 기능은 요청 시 추가). Original plan text below is preserved; ignore tasks 5.3–5.6 unless/until re-opened.

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development`. Bound by `orchestration-discipline` 4 gates. Each runner is ONE task — dispatch a fresh Sonnet subagent per runner, with two-stage review.

**Goal:** Port the 6 non-proven runner stubs in `nexacroN-fullstack/samples/runners/` into fully-buildable runners matching the spec's 8-runner matrix (§2.1), leveraging the 2 proven runners as templates.

**Architecture:** Thin bootstrap pattern — each runner is a thin HTTP adapter that delegates to shared-business modules. Controllers implement the 14-endpoint common API contract. Packaging, servlet-api lane, and framework flavour diverge per cell; everything else reuses shared-business.

**Tech Stack:** Maven, Spring Boot 2/3 (boot runners), Spring MVC 5/6 (mvc runners), eGov 4/5 (egov runners), Spring WebFlux (webflux runner). MyBatis 2.3.2 (javax) / 3.0.3 (jakarta). HSQLDB in-memory.

---

## Scope Boundaries

**IN SCOPE** — 6 runners (all stubs already scaffolded as empty directories with README.md only):

| # | runner | packaging | framework | lane | base biz tree |
|---|---|---|---|---|---|
| 1 | `mvc-jdk17-jakarta` | war | Spring MVC 6 | jakarta | `shared-business/jdk17-jakarta` |
| 2 | `mvc-jdk8-javax` | war | Spring MVC 5 | javax | `shared-business/jdk8-javax` |
| 3 | `egov5-boot-jdk17-jakarta` | jar | eGov 5 / Boot 3 | jakarta | `shared-business-egov5/jdk17-jakarta` |
| 4 | `egov4-boot-jdk8-javax` | jar | eGov 4 / Boot 2 | javax | `shared-business-egov4/jdk8-javax` |
| 5 | `egov4-mvc-jdk8-javax` | war | eGov 4 / Spring 5 | javax | `shared-business-egov4/jdk8-javax` |
| 6 | `webflux-jdk17-jakarta` | jar | Boot 3 + WebFlux | jakarta | `shared-business-reactive/jdk17-mybatis` |

**OUT OF SCOPE**:
- 14-endpoint controller alignment (currently 5 endpoints in proven runners) → Task 2 plan6.
- shared-business-egov4/5 and shared-business-reactive **module authoring** if those trees don't yet exist in monorepo → escalate to user before porting egov*/webflux runners.
- Integration tests / e2e nxui smoke tests → Phase 4 plan4.

---

## Prerequisites

**Before starting any runner task:**

- [ ] **P.1**: Dispatch Explore subagent to verify these shared-business trees exist in `D:\AI\workspace\nexacroN-fullstack\shared-business*`:
  - `shared-business/jdk17-jakarta` (required by #1)
  - `shared-business/jdk8-javax` (required by #2)
  - `shared-business-egov5/jdk17-jakarta` (required by #3)
  - `shared-business-egov4/jdk8-javax` (required by #4, #5)
  - `shared-business-reactive/jdk17-mybatis` (required by #6)

  For each missing tree → **HALT** and escalate. Do not author runner against a non-existent biz dependency.

- [ ] **P.2**: Confirm parent pom version props for egov and webflux lanes exist. If `<egov.version>`, `<spring.webflux.version>`, etc. are absent, that's a pre-requisite blocker → escalate.

---

## Per-Runner Task Template

Each of the 6 runners follows the same 8-step task shape. Only the VARIABLES differ.

### Task <N>: Port runner `<runner-name>`

**Files to create:**
- `samples/runners/<runner-name>/pom.xml`
- `samples/runners/<runner-name>/src/main/java/com/nexacro/fullstack/runner/<pkg>/Application.java` (boot/webflux) OR `src/main/webapp/WEB-INF/web.xml` (mvc/war)
- `samples/runners/<runner-name>/src/main/java/com/nexacro/fullstack/runner/<pkg>/controller/*.java` (copy from proven runner, adapt namespace)
- `samples/runners/<runner-name>/src/main/resources/application.yml` (boot) OR `application-context.xml` (mvc)
- `samples/runners/<runner-name>/src/main/resources/mybatis-config.xml` (if needed)
- `samples/runners/<runner-name>/README.md` (replace stub)

**Variables:**

| var | #1 mvc-jakarta | #2 mvc-javax | #3 egov5-boot | #4 egov4-boot | #5 egov4-mvc | #6 webflux |
|---|---|---|---|---|---|---|
| `packaging` | war | war | jar | jar | war | jar |
| `java.version` | 17 | 1.8 | 17 | 1.8 | 1.8 | 17 |
| `spring.boot.version` | — | — | 3.3.5 | 2.7.18 | — | 3.3.5 |
| `spring.framework.version` | 6.1.14 | 5.3.39 | (via boot) | (via boot) | 5.3.39 | (via boot) |
| `egov.version` | — | — | 5.x | 4.x | 4.x | — |
| `nexacro.xapi.artifactId` | `nexacroN-xapi-jakarta` | `nexacroN-xapi` | `nexacroN-xapi-jakarta` | `nexacroN-xapi` | `nexacroN-xapi` | `nexacroN-xapi-jakarta` |
| `uiadapter.artifactId` (stem) | `uiadapter-jakarta-*` | `uiadapter-spring-*` | `uiadapter-jakarta-*` | `uiadapter-spring-*` | `uiadapter-spring-*` | `uiadapter-jakarta-*` |
| `biz-tree` | `jdk17-jakarta` | `jdk8-javax` | `egov5/jdk17-jakarta` | `egov4/jdk8-javax` | `egov4/jdk8-javax` | `reactive/jdk17-mybatis` |
| `template` (copy-from) | `boot-jdk17-jakarta` + strip boot + add war | `boot-jdk8-javax` + strip boot + add war | `boot-jdk17-jakarta` + add egov | `boot-jdk8-javax` + add egov | `mvc-jdk8-javax` (Task 2) + add egov | `boot-jdk17-jakarta` + swap web-mvc → webflux |

**Steps** (repeated per runner, instantiated with the variables above):

- [ ] **Step 1: Dispatch Sonnet subagent for the runner**

Template prompt (substitute `<runner-name>` and variable block):
```
Agent(
  subagent_type="general-purpose",
  model="sonnet",
  description="Port runner <runner-name>",
  prompt="""
    Port a new runner under samples/runners/<runner-name>/ based on the proven template samples/runners/<template>/.

    Variables:
      packaging: <packaging>
      java.version: <java.version>
      spring.boot.version: <spring.boot.version or 'n/a'>
      spring.framework.version: <spring.framework.version>
      egov.version: <egov.version or 'n/a'>
      nexacro.xapi.artifactId: <nexacro.xapi.artifactId>
      uiadapter stem: <uiadapter.artifactId stem>
      shared-business path: <biz-tree>

    Requirements:
      1. pom.xml: inherit from ../../pom.xml, packaging <packaging>, dependencies only on shared-business/<biz-tree> + the 5 nexacro artifacts (use bare <dependency> — no versions, parent BOM manages).
      2. For war packaging: add maven-war-plugin, create src/main/webapp/WEB-INF/web.xml with DispatcherServlet + spring-web-mvc root-context. Copy <application-context.xml> pattern from comparable existing mvc runner IF one was previously completed; otherwise derive from Spring Framework 5/6 reference.
      3. For boot/webflux packaging: add spring-boot-maven-plugin, create Application.java with @SpringBootApplication (and @EnableWebFlux for #6), copy application.yml from template.
      4. For egov runners: add egov-framework-common BOM import + egov-framework-web, keep Boot/MVC base intact.
      5. Copy 5 controller classes from template into com.nexacro.fullstack.runner.<pkg>.controller (renaming package). For #6 webflux, convert controller signatures to Mono<ResponseEntity<?>>.
      6. Build: run `mvn -pl samples/runners/<runner-name> -am compile` from monorepo root. Fix any failures autonomously (common: missing @EnableWebMvc for mvc runners, missing servlet-api scope=provided for war).
      7. Print BUILD SUCCESS or BUILD FAILURE + last 30 lines of mvn log.

    Return DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED per orchestration-discipline.
  """
)
```

- [ ] **Step 2: Spec-compliance review**

Dispatch Explore subagent:
```
Agent(
  subagent_type="Explore",
  description="Spec-compliance review of <runner-name>",
  prompt="Review samples/runners/<runner-name>/ against spec §2.1 matrix row for this runner and the proven template pom.xml. Verify: packaging matches, java.version matches, 5 bare nexacro deps present (no versions, no systemPath), controllers under correct package, for war: web.xml exists and maven-war-plugin is configured. Return PASS / FAIL + specific gaps."
)
```

- [ ] **Step 3: If FAIL, loop implementer fix + re-review until PASS**

- [ ] **Step 4: Code-quality review**

Dispatch Explore subagent with focus on code-quality (naming, DRY, pattern consistency with the template).

- [ ] **Step 5: Per-file commits (CLAUDE.md rule)**

For each created file, individual commit:
```bash
git add samples/runners/<runner-name>/pom.xml
git commit -m "feat(runner): <runner-name> pom.xml (<packaging>, <lane>, <framework>)"
# ... repeat per file ...
```

- [ ] **Step 6: Drift-check rerun**

Run `scripts/drift-check.sh` (from plan4 Task 4.3). Expected: this runner flips from DRIFT → OK.

- [ ] **Step 7: Update CHANGELOG [Unreleased] section** with `- Added \`<runner-name>\` runner (packaging=<packaging>, framework=<framework>, lane=<lane>)`.

- [ ] **Step 8: Mark complete in tasks/todo.md**

---

## Execution Order (ACTIVE — scope-narrowed)

1. **Task 5.1** ✅ active: `mvc-jdk17-jakarta` — war transform of boot-jakarta. Backed by `samples/shared-business/jdk17-jakarta` (exists).
2. **Task 5.2** ✅ active: `mvc-jdk8-javax` — war transform of boot-javax. Backed by `samples/shared-business/jdk8-javax` (exists).

Tasks 5.3–5.6 (webflux + egov4/5) **DEFERRED** per user decision 2026-04-24. Shared-business-egov4/egov5/reactive trees are empty; re-open only on explicit user request, then author a follow-up plan (plan7) for the missing shared-business trees first.

Do NOT parallelise Sonnet subagents across Task 5.1 and 5.2 — keep serial to avoid parent-pom contention and to make each spec-review focused.

---

## Gate Enforcement Summary

- **Gate 1**: Opus authors this plan; each runner port is dispatched to Sonnet.
- **Gate 2**: Codex-rescue (or Explore fallback) intent-check EACH task's variable block against spec §2.1 before Step 1 dispatch. Prevents mismatched artefact names.
- **Gate 3**: Before tagging the completion release (proposed monorepo tag `v0.7.0-all-runners`), dispatch codex-rescue with the 6-runner diff + release notes draft.
- **Gate 4**: If any prior tag (v0.5.0-core, v0.6.0-core-from-nexus) is threatened by a runner port (e.g., needing a parent-pom property change that breaks existing runners), STOP and retrospect.

---

## Self-Review

- [x] Every runner cell has a concrete variable assignment — no TBD
- [x] Template source identified per runner
- [x] Blocker paths (missing shared-business trees, missing version props) explicit
- [x] Out-of-scope cleanly labelled (controller 14-endpoint expansion → plan6)
- [x] Per-file commit discipline preserved (CLAUDE.md)
- [x] Gate 2 and Gate 3 dispatch points named

---

## Execution Handoff

Recommended: `superpowers:subagent-driven-development`. 6 tasks are independent (after the template transforms are validated in 5.1 and 5.2), each suitable for fresh-context Sonnet dispatch.

Next concrete action on task 1 pickup: Prerequisite P.1 (verify shared-business trees). If any tree is missing, HALT and escalate before spending Sonnet cycles on a doomed port.
