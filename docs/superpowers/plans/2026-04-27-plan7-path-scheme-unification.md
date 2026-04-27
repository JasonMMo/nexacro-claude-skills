# Plan7: Runner Path-Scheme Unification — **SUPERSEDED**

> **⚠️ SUPERSEDED 2026-04-27:** This plan adopted the wrong canonical scheme (`/<domain>/<action>.do`). User's authoritative 14-endpoint spec requires `/uiadapter/<action>.do` prefix on ALL endpoints. Replaced by Plan8 (Controller endpoint recovery). Do NOT execute this plan.

> **For agentic workers:** Small follow-up plan from plan6 closure. Single canonical scheme applied across both runners. 5 file edits total. Execute inline (subagent overhead not justified).

**Goal:** Eliminate path-scheme divergence between `boot-jdk17-jakarta` and `boot-jdk8-javax` by adopting a single canonical scheme `/<domain>/<action>.do`.

**Architecture:** All HTTP endpoints across both runners conform to `/<domain>/<action>.do`. No `/sample/` prefix. `.do` suffix universal. Auth and uiadapter contract paths preserved as-is (already aligned).

**Canonical scheme decision (resolves `14-endpoints.md` Appendix C, Option 1):**

| Domain | Pattern | Notes |
|---|---|---|
| Auth | `/login.do`, `/logout.do` | Top-level (no domain prefix), follows legacy convention |
| Board | `/board/{select,insert,update,delete}.do` | Drop `/sample/` prefix (jakarta anomaly) |
| Dept | `/dept/{list,tree}.do` | Already aligned |
| File | `/file/{upload,download,list}.do` | Already aligned |
| Large | `/large/page.do` | javax adds `.do` |
| Uiadapter | `/uiadapter/<action>.do` | 5 plan6 endpoints, already aligned |

**Rationale:** Option 1 (Appendix C) wins. `.do` is established Nexacro convention, already used by uiadapter/dept/file/large in jakarta. `/sample/` prefix on jakarta board is an anomaly — dropping it minimizes churn (1 jakarta edit) versus adding `/sample/` everywhere (8+ edits). Final delta: 1 jakarta file + 4 javax files = 5 edits.

**Tech stack:** Spring `@RequestMapping`/`@PostMapping`/`@GetMapping` annotation rewrites only. No business logic changes.

---

### Task 7.1 — Jakarta: drop `/sample/` from BoardController

**Files:**
- Modify: `samples/runners/boot-jdk17-jakarta/src/main/java/com/nexacro/fullstack/runner/boot17/controller/BoardController.java:14`

- [ ] **Step 1: Edit class-level mapping**

`@RequestMapping("/sample/board")` → `@RequestMapping("/board")`

- [ ] **Step 2: Verify compile**

`mvn -pl samples/runners/boot-jdk17-jakarta -am -DskipTests compile -q` → BUILD SUCCESS expected

### Task 7.2 — Javax: add `.do` to BoardController

**Files:**
- Modify: `samples/runners/boot-jdk8-javax/src/main/java/com/nexacro/fullstack/runner/boot8/controller/BoardController.java:23,28`

- [ ] **Step 1: select**

`@PostMapping("/select")` → `@PostMapping("/select.do")`

- [ ] **Step 2: insert/update/delete**

`@PostMapping({"/insert", "/update", "/delete"})` → `@PostMapping({"/insert.do", "/update.do", "/delete.do"})`

### Task 7.3 — Javax: add `.do` to LargeDataController

**Files:**
- Modify: `samples/runners/boot-jdk8-javax/src/main/java/com/nexacro/fullstack/runner/boot8/controller/LargeDataController.java:23`

- [ ] **Step 1:** `@PostMapping("/page")` → `@PostMapping("/page.do")`

### Task 7.4 — Javax: add `.do` to LoginController

**Files:**
- Modify: `samples/runners/boot-jdk8-javax/src/main/java/com/nexacro/fullstack/runner/boot8/controller/LoginController.java:23,34`

- [ ] **Step 1: login** → `@PostMapping("/login.do")`
- [ ] **Step 2: logout** → `@PostMapping("/logout.do")`

### Task 7.5 — Update `api-contract/14-endpoints.md` Appendix C

**Files:**
- Modify: `api-contract/14-endpoints.md` (Appendix C section)

- [ ] **Step 1:** Replace "Deferred to plan7" wording with "Resolved in plan7 (2026-04-27)". Document final canonical scheme. Mark Option 1 as adopted.

### Task 7.6 — Build + smoke verification

- [ ] **Step 1: mvn compile both runners**

```
mvn -pl samples/runners/boot-jdk17-jakarta -am -DskipTests compile -q
mvn -pl samples/runners/boot-jdk8-javax  -am -DskipTests compile -q
```

Expected: BUILD SUCCESS for both.

- [ ] **Step 2: Boot both runners, curl 17 endpoints with new canonical paths**

Pass criteria: 17/17 non-5xx per runner. The previously divergent paths (jakarta `/sample/board/*`, javax `/board/*`, `/login`, `/logout`, `/large/page`) must now be unreachable on both runners — only the canonical `/<domain>/<action>.do` paths respond.

### Task 7.7 — Commit per file (per CLAUDE.md rule)

- [ ] One commit per modified file:
  1. `samples/runners/boot-jdk17-jakarta/.../BoardController.java`
  2. `samples/runners/boot-jdk8-javax/.../BoardController.java`
  3. `samples/runners/boot-jdk8-javax/.../LargeDataController.java`
  4. `samples/runners/boot-jdk8-javax/.../LoginController.java`
  5. `api-contract/14-endpoints.md`

### Task 7.8 — Update `tasks/todo.md`

- [ ] Mark plan7 closed in nexacro-claude-skills repo `tasks/todo.md`. Remove plan7 entry from "Plan6 follow-ups" table. Record outcome.

---

## Rollback note

If a smoke endpoint regresses to 5xx, revert the offending controller edit only. The 5 edits are independent — no inter-file dependencies, so partial rollback is safe.

## Out of scope (deferred to other plans)

- plan8: vendored shim → Nexus raw modules
- plan9: hsqldb javax-lane JDK floor
- plan10: jakarta pom.xml `spring-boot-maven-plugin` pin
- OpenAPI `/excel/export.do` reconciliation
