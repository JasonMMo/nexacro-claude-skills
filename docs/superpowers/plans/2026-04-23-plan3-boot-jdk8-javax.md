# Plan 3 — Second Runner: `boot-jdk8-javax` End-to-End (Dual-Lane Proof)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `samples/runners/boot-jdk8-javax/` actually run (`mvn spring-boot:run`) on **port 8081** and serve the same 5 canonical Nexacro-dataset endpoints as Plan 2, but on the **javax lane** (Spring Boot 2.7.18 / Spring 5.3.39 / jdk8 / javax servlet API). This proves the matrix's dual-lane derivation rules actually hold end-to-end.

**Architecture:**
- Spring Boot **2.7.18** on JDK **8**, **javax** servlet API, Maven jar packaging
- Port **8081** (so it can run side-by-side with Plan 2's jar on 8080 during smoke verification)
- Business tree in `samples/shared-business/jdk8-javax/` — structurally identical to `jdk17-jakarta` but with:
  - `javax.servlet.*` instead of `jakarta.servlet.*` (only matters where session/multipart are touched)
  - **Java 8 syntax** throughout (no switch expressions, no records, no `List.of`, no pattern matching)
  - mybatis-spring-boot-starter **2.3.2** (javax lane) instead of 3.0.3
- Same 5 endpoints, same wire format (JSON envelope), same HSQL seed data (single source of truth)

**Tech Stack:**
- spring-boot **2.7.18** (parent BOM)
- spring **5.3.39**
- MyBatis Spring Boot Starter **2.3.2** (javax lane)
- HSQLDB 2.7.3
- Jackson for JSON envelope serde
- Lombok for DTO boilerplate
- **jdk 1.8 target** (compiler `<source>1.8</source><target>1.8</target>`)

**Out of scope (defer to later plans):**
- XML and SSV wire formats (JSON only, same as Plan 2)
- `/excel/export.do`, `/reactive/exim_exchange.do`
- Integration tests (manual curl smoke-check only)
- Plans 4-6 (mvc-war, webflux, egov)

---

## Carry-Forward Lessons From Plan 2

These HSQL / wire-format pitfalls were discovered late in Plan 2 and MUST be baked in from Task 1:

1. **Seed-data statement separator is `^^`** (not `;`) — HSQL PSM `WHILE` loops contain internal semicolons. `application.yml` must set `spring.sql.init.separator: "^^"`. Seed SQL files are already correct (we share them via maven-resources-plugin).
2. **`LARGE_DATA` seeding uses PSM `CREATE PROCEDURE … CALL … DROP PROCEDURE`** — recursive CTE hits HSQL's recursion limit at 1000 rows. Already fixed in seed-data.
3. **CLOB columns return `JDBCClobClient`** — Jackson can't serialize. `BoardService` (and any CLOB-touching service) must call a `normalizeClobRows()` helper that reads the CLOB stream into a String before returning the row list. Same fix applies here.
4. **`maven-compiler-plugin` must be pinned** — global default may target newer bytecode. Pin `3.13.0` (or 3.11.0) with explicit `<source>1.8</source><target>1.8</target>` in both the business tree pom and the runner pom.

---

## Java 8 Syntax Rules (applied throughout all Tasks)

| Java 9+ pattern used in Plan 2 | Java 8 equivalent for Plan 3 |
|---|---|
| `List.of(a, b, c)` | `Arrays.asList(a, b, c)` |
| `Map.of("k", v)` | `Collections.singletonMap("k", v)` / `new HashMap<>()` + `put` |
| `switch (x) { case I -> foo(); }` (expression) | classic `switch(x) { case I: foo(); break; }` |
| `record DownloadInfo(File f, Map m) {}` | regular class + `private final` fields + getters + constructor |
| `if (v instanceof Number n) use(n)` | `if (v instanceof Number) { Number n = (Number) v; use(n); }` |
| `var x = new ArrayList<…>()` | `List<…> x = new ArrayList<>()` |
| Text blocks `"""…"""` | single-line `"…"` with `+` concat |

If an implementer subagent drifts into Java 9+ syntax, the spec reviewer MUST flag it and the code will fail to compile under `<target>1.8</target>` anyway — that's our safety net.

---

## File Structure (Plan 3)

**Business tree — `samples/shared-business/jdk8-javax/`:**
```
pom.xml                                  (javax lane deps, inherits parent, target 1.8)
src/main/java/com/nexacro/fullstack/business/
  xapi/
    NexacroDataset.java                  (identical structure to jakarta; Java 8 syntax)
    NexacroEnvelope.java
    RowType.java
    EnvelopeCodec.java
  uiadapter/
    NexacroController.java
    NexacroResponseBuilder.java
  domain/
    user/{UserService.java, UserDao.java, UserDao.xml}
    board/{BoardService.java, BoardDao.java, BoardDao.xml}   (classic switch)
    dept/{DeptService.java, DeptDao.java, DeptDao.xml}
    large/{LargeDataService.java, LargeDataDao.java, LargeDataDao.xml}
    file/{FileService.java, FileDao.java, FileDao.xml}       (regular class, no record)
src/main/resources/
  mybatis-config.xml
```

**Runner — `samples/runners/boot-jdk8-javax/`:**
```
pom.xml                                  (spring-boot 2.7.18, target 1.8)
src/main/java/com/nexacro/fullstack/runner/boot8/
  Application.java
  config/{WebConfig.java, MyBatisConfig.java}
  controller/{Login,Board,Dept,Large,File}Controller.java  (javax.servlet.*)
src/main/resources/
  application.yml                        (port 8081, context-path /uiadapter, separator ^^)
  logback-spring.xml                     (minimal — optional)
```

**Design decisions (locked in):**
- Port 8081 so Plan 2 (8080) and Plan 3 (8081) can coexist during verification.
- Same package prefix `com.nexacro.fullstack.business` for the business tree so scan paths line up. Runner gets its own `com.nexacro.fullstack.runner.boot8` package.
- **No cross-module reuse with jdk17-jakarta tree** — this is a deliberate duplicate. The two trees prove the matrix axiom; they are NOT meant to DRY-merge. If future plans extract a common module, that's a separate refactor.
- All file storage same as Plan 2: `./uploads/{uuid}-{original}` local filesystem.

---

## Task 1: Business tree scaffold + xapi core

**Files:**
- Create: `D:\AI\workspace\nexacroN-fullstack\samples\shared-business\jdk8-javax\pom.xml`
- Create: `.../xapi/NexacroDataset.java`
- Create: `.../xapi/NexacroEnvelope.java`
- Create: `.../xapi/RowType.java`
- Create: `.../xapi/EnvelopeCodec.java`

- [ ] **Step 1.1:** Write `pom.xml` — artifactId `shared-business-jdk8-javax`, packaging `jar`, parent is monorepo root POM. Deps: `javax.servlet-api:4.0.1` (provided), `spring-context:${spring5.version}`, `spring-web:${spring5.version}`, `spring-jdbc:${spring5.version}`, `spring-tx:${spring5.version}`, `mybatis-spring-boot-starter:2.3.2`, `hsqldb:2.7.3` (runtime), `jackson-databind` (managed by parent), `lombok` (provided), `commons-io:2.15.1`. Pin `maven-compiler-plugin:3.13.0` with `<source>1.8</source><target>1.8</target>`.

- [ ] **Step 1.2:** Write `RowType.java` — enum `N, I, U, D, O` + static `fromString(String s)` returning `O` when null/empty (tolerant, same as Plan 2). No Java 9+ features.

- [ ] **Step 1.3:** Write `NexacroDataset.java` — Lombok `@Data` POJO. Fields: `String id`, `ColumnInfo columnInfo` (nested class with `List<ConstColumn> constColumn` + `List<Column> column`), `List<Map<String,Object>> rows`. Jackson annotations: `@JsonProperty("ColumnInfo")` on columnInfo, `@JsonProperty("Rows")` on rows, `@JsonProperty("ConstColumn")` / `@JsonProperty("Column")` on the nested lists. Nested `ConstColumn(String id, String type, String size, Object value)` and `Column(String id, String type, String size)` — plain `@Data` POJOs.

- [ ] **Step 1.4:** Write `NexacroEnvelope.java` — Lombok `@Data`. Fields: `String version` (default `"1.0"`), `List<Parameter> parameters` (`@JsonProperty("Parameters")`), `List<NexacroDataset> datasets` (`@JsonProperty("Datasets")`). Nested `Parameter(String id, Object value, String type)`.

- [ ] **Step 1.5:** Write `EnvelopeCodec.java` — static methods `NexacroEnvelope decode(InputStream)` and `void encode(NexacroEnvelope, OutputStream)`. Use `private static final ObjectMapper MAPPER = new ObjectMapper().configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);` — same config as Plan 2.

- [ ] **Step 1.6:** Commit (one commit per file per repo convention):
  - `feat(business-jdk8-javax): add pom.xml (javax lane, jdk8 target)`
  - `feat(business-jdk8-javax): add xapi.RowType`
  - `feat(business-jdk8-javax): add xapi.NexacroDataset`
  - `feat(business-jdk8-javax): add xapi.NexacroEnvelope`
  - `feat(business-jdk8-javax): add xapi.EnvelopeCodec`

---

## Task 2: uiadapter base + response builder

**Files:**
- Create: `.../uiadapter/NexacroController.java`
- Create: `.../uiadapter/NexacroResponseBuilder.java`

- [ ] **Step 2.1:** Write `NexacroResponseBuilder.java` — static helpers:
  - `ok(NexacroDataset... datasets)` → envelope with `ErrorCode=0`, `ErrorMsg=""`, datasets list
  - `error(int code, String message)` → envelope with those values, empty datasets
  - `errorFromException(Throwable t)` → delegates to `error(-1, t.getMessage() != null ? t.getMessage() : t.getClass().getSimpleName())`
  - Use `Arrays.asList(...)` NOT `List.of(...)`.

- [ ] **Step 2.2:** Write `NexacroController.java` — abstract base with `@ExceptionHandler(Exception.class)` returning `NexacroResponseBuilder.errorFromException(e)`. Protected helpers:
  - `NexacroDataset datasetById(NexacroEnvelope env, String id)` — null-safe list walk
  - `Object parameterById(NexacroEnvelope env, String id)` — null-safe, returns the `value` field
  
  No `var`, no switch expressions, no records.

- [ ] **Step 2.3:** Commit (2 commits):
  - `feat(business-jdk8-javax): add uiadapter.NexacroResponseBuilder`
  - `feat(business-jdk8-javax): add uiadapter.NexacroController`

---

## Task 3: User domain (/login.do)

**Files:**
- Create: `.../domain/user/{UserService,UserDao}.java` + `UserDao.xml`

- [ ] **Step 3.1:** Write `UserDao.java` — `@Mapper` with `Map<String,Object> findById(@Param("userId") String userId)` and `int updateLastLogin(@Param("userId") String userId)` (no-op stub is OK since schema has no LAST_LOGIN column).

- [ ] **Step 3.2:** Write `UserDao.xml` at `src/main/resources/com/nexacro/fullstack/business/domain/user/UserDao.xml`. `SELECT USER_ID, USER_NAME, PASSWORD_HASH, EMAIL, ROLE, ENABLED FROM USERS WHERE USER_ID = #{userId} AND ENABLED = TRUE`. `updateLastLogin` can be a dummy `UPDATE USERS SET USER_NAME = USER_NAME WHERE USER_ID = #{userId}` (no-op write).

- [ ] **Step 3.3:** Write `UserService.java` — `@Service`. Method `NexacroDataset login(String userId, String password)`:
  - Look up user via dao. If null → throw `IllegalArgumentException("Unknown user: " + userId)`.
  - Expected hash is `"stub$" + userId` (seed convention). If mismatch → throw `IllegalArgumentException("Invalid credentials")`.
  - Build single-row dataset with columns USER_ID, USER_NAME, ROLE. Return.
  - Use `HashMap<String,Object>` + `put` — no `Map.of`.

- [ ] **Step 3.4:** Commit (3 commits — dao, xml, service).

---

## Task 4: Board domain with `_RowType_` dispatch (classic switch!)

**Files:**
- Create: `.../domain/board/{BoardService,BoardDao}.java` + `BoardDao.xml`

- [ ] **Step 4.1:** Write `BoardDao.java` — `@Mapper` with:
  - `List<Map<String,Object>> selectAll()`
  - `Map<String,Object> selectById(@Param("boardId") int boardId)`
  - `int insert(Map<String,Object> row)` — uses `useGeneratedKeys` + `keyProperty="BOARD_ID"`
  - `int update(Map<String,Object> row)`
  - `int softDelete(@Param("boardId") int boardId)`

- [ ] **Step 4.2:** Write `BoardDao.xml`. Queries:
  - `selectAll`: `SELECT BOARD_ID, TITLE, CONTENT, AUTHOR_ID, VIEW_COUNT, CREATED_AT, UPDATED_AT FROM SAMPLE_BOARD WHERE DELETED = FALSE ORDER BY BOARD_ID`
  - `insert`: `INSERT INTO SAMPLE_BOARD (TITLE, CONTENT, AUTHOR_ID, VIEW_COUNT) VALUES (#{TITLE}, #{CONTENT}, #{AUTHOR_ID}, #{VIEW_COUNT})` with `useGeneratedKeys="true" keyProperty="BOARD_ID"`
  - `update`: `UPDATE SAMPLE_BOARD SET TITLE = #{TITLE}, CONTENT = #{CONTENT}, UPDATED_AT = CURRENT_TIMESTAMP WHERE BOARD_ID = #{BOARD_ID}`
  - `softDelete`: `UPDATE SAMPLE_BOARD SET DELETED = TRUE, UPDATED_AT = CURRENT_TIMESTAMP WHERE BOARD_ID = #{boardId}`

- [ ] **Step 4.3:** Write `BoardService.java`. Key methods:
  - `NexacroDataset selectAll()` — calls dao, wraps result with `normalizeClobRows()` helper (copy the exact helper from Plan 2's BoardService), builds dataset with column metadata.
  - `@Transactional int processRows(NexacroDataset input)` — iterates `input.getRows()`, reads `_RowType_` via `RowType.fromString(...)`, dispatches with **classic switch + break**:
    ```java
    switch (rt) {
      case I: affected += dao.insert(row); break;
      case U: affected += dao.update(row); break;
      case D:
        Object idObj = row.get("BOARD_ID");
        int id = (idObj instanceof Number) ? ((Number) idObj).intValue() : Integer.parseInt(String.valueOf(idObj));
        affected += dao.softDelete(id);
        break;
      case N:
      case O:
      default:
        // skip
        break;
    }
    ```
  - `normalizeClobRows(List<Map<String,Object>>)` — iterates, for each value that `instanceof java.sql.Clob`, read via `clob.getCharacterStream()` into a `String`, put back into the map. Use the Java 8 version (no pattern matching).

- [ ] **Step 4.4:** Commit (3 commits — dao, xml, service).

---

## Task 5: Dept tree + Large paging + File upload domains

**Files:**
- Create: `.../domain/dept/{DeptService,DeptDao}.java` + `DeptDao.xml`
- Create: `.../domain/large/{LargeDataService,LargeDataDao}.java` + `LargeDataDao.xml`
- Create: `.../domain/file/{FileService,FileDao}.java` + `FileDao.xml`

- [ ] **Step 5.1:** `DeptDao.xml` — `listAll`: `SELECT DEPT_ID, DEPT_NAME, PARENT_ID, LEVEL_NO, SORT_ORDER FROM DEPT WHERE ENABLED = TRUE ORDER BY LEVEL_NO, SORT_ORDER`. `tree`: recursive CTE:
  ```sql
  WITH RECURSIVE DEPT_TREE (DEPT_ID, DEPT_NAME, PARENT_ID, LEVEL_NO, SORT_ORDER, PATH) AS (
    SELECT DEPT_ID, DEPT_NAME, PARENT_ID, 1, SORT_ORDER, CAST(DEPT_ID AS VARCHAR(500))
      FROM DEPT WHERE PARENT_ID IS NULL AND ENABLED = TRUE
    UNION ALL
    SELECT d.DEPT_ID, d.DEPT_NAME, d.PARENT_ID, t.LEVEL_NO + 1, d.SORT_ORDER,
           CAST(t.PATH || '/' || d.DEPT_ID AS VARCHAR(500))
      FROM DEPT d JOIN DEPT_TREE t ON d.PARENT_ID = t.DEPT_ID
      WHERE d.ENABLED = TRUE
  )
  SELECT * FROM DEPT_TREE ORDER BY PATH
  ```

- [ ] **Step 5.2:** `DeptService.java` — two methods `NexacroDataset listAll()` and `NexacroDataset tree()`, each building a dataset with proper column metadata (DEPT_ID, DEPT_NAME, PARENT_ID, LEVEL_NO, SORT_ORDER; `tree()` also includes PATH).

- [ ] **Step 5.3:** `LargeDataDao.xml` — `count` and `page`:
  ```sql
  SELECT ROW_ID, CATEGORY, SEQ_NO, VALUE_1, VALUE_2, VALUE_3, CREATED_AT
    FROM LARGE_DATA
    <where><if test="category != null">CATEGORY = #{category}</if></where>
    ORDER BY SEQ_NO
    OFFSET #{offset} ROWS FETCH NEXT #{limit} ROWS ONLY
  ```
  `count` with same `<where>` block.

- [ ] **Step 5.4:** `LargeDataService.java` — method `LargePageResult page(int page, int pageSize, String category)` where `LargePageResult` is a regular class (NOT a record) with two `final` fields `NexacroDataset dataset` + `long totalCount` and a constructor + getters. Page is 1-indexed; offset = `(page - 1) * pageSize`.

- [ ] **Step 5.5:** `FileDao.xml` — `insert`:
  ```sql
  INSERT INTO FILE_META (FILE_ID, ORIGINAL_NAME, STORED_PATH, CONTENT_TYPE, SIZE_BYTES, UPLOADED_BY)
  VALUES (#{FILE_ID}, #{ORIGINAL_NAME}, #{STORED_PATH}, #{CONTENT_TYPE}, #{SIZE_BYTES}, #{UPLOADED_BY})
  ```
  `findById(fileId)`: `SELECT * FROM FILE_META WHERE FILE_ID = #{fileId} AND DELETED = FALSE`
  `listAll`: `SELECT * FROM FILE_META WHERE DELETED = FALSE ORDER BY UPLOADED_AT DESC`

- [ ] **Step 5.6:** `FileService.java`:
  - `@Value("${nexacro.file.storage-dir:./uploads}") String storageDir;`
  - `Map<String,Object> upload(MultipartFile file, String uploadedBy)`:
    - Generate `UUID.randomUUID().toString()` → `fileId`
    - Compute stored filename `fileId + "-" + file.getOriginalFilename()`
    - `new File(storageDir).mkdirs();`
    - `file.transferTo(target);`
    - Build metadata map + `dao.insert(meta)`
    - Return meta
  - `DownloadInfo download(String fileId)` where `DownloadInfo` is a **regular class** (NOT a record) holding `File file` + `Map<String,Object> meta`. Throws `IllegalArgumentException` if not found.
  - `NexacroDataset list()` — returns metadata dataset.

- [ ] **Step 5.7:** Commit (9 commits — 3 domains × {dao, xml, service}).

---

## Task 6: mybatis-config.xml + compile sanity

**Files:**
- Create: `.../src/main/resources/mybatis-config.xml`

- [ ] **Step 6.1:** Write `mybatis-config.xml` — identical to Plan 2: `mapUnderscoreToCamelCase=true`, `defaultStatementTimeout=30`, `logImpl=SLF4J`.

- [ ] **Step 6.2:** With `JAVA_HOME=<jdk8>` and parent POM already in local repo (from Plan 1/2), run:
  ```
  mvn -f samples/shared-business/jdk8-javax/pom.xml compile
  ```
  Expect BUILD SUCCESS. If it fails because the parent POM isn't resolvable, run `mvn -N install` on the monorepo root first.

- [ ] **Step 6.3:** Commit (2 commits — config + any sanity tweaks):
  - `feat(business-jdk8-javax): add mybatis-config.xml`
  - (verify-only — no further commit unless fixes needed)

---

## Task 7: Runner pom.xml + Application.java + config classes

**Files:**
- Modify: `D:\AI\workspace\nexacroN-fullstack\samples\runners\boot-jdk8-javax\pom.xml` (currently placeholder README — create pom)
- Create: `.../src/main/java/com/nexacro/fullstack/runner/boot8/Application.java`
- Create: `.../config/WebConfig.java`
- Create: `.../config/MyBatisConfig.java`

- [ ] **Step 7.1:** Create runner `pom.xml` — artifactId `runner-boot-jdk8-javax`, packaging `jar`, parent is monorepo root. Deps:
  - `com.nexacro.fullstack:shared-business-jdk8-javax:0.1.0-SNAPSHOT`
  - `org.springframework.boot:spring-boot-starter-web:2.7.18`
  - `org.springframework.boot:spring-boot-starter-jdbc:2.7.18`
  - `org.mybatis.spring.boot:mybatis-spring-boot-starter:2.3.2` (pin explicitly)
  - `org.hsqldb:hsqldb:2.7.3` (runtime)
  
  Plugin: `spring-boot-maven-plugin:2.7.18` with `mainClass = com.nexacro.fullstack.runner.boot8.Application`. Pin `maven-compiler-plugin:3.13.0` with `<source>1.8</source><target>1.8</target>`.
  
  Add `maven-resources-plugin` to copy seed-data (identical config to Plan 2, just adjust the relative path — from `samples/runners/boot-jdk8-javax/` the seed is at `../../seed-data`):
  ```xml
  <directory>${project.basedir}/../../seed-data</directory>
  <includes><include>schema.sql</include><include>data.sql</include></includes>
  ```

- [ ] **Step 7.2:** Write `Application.java` — `@SpringBootApplication(scanBasePackages = {"com.nexacro.fullstack.runner.boot8", "com.nexacro.fullstack.business"})` + `main(String[] args) { SpringApplication.run(Application.class, args); }`.

- [ ] **Step 7.3:** Write `WebConfig.java` — `@Configuration` that:
  - `@Bean ObjectMapper nexacroObjectMapper()` — configured with `FAIL_ON_UNKNOWN_PROPERTIES=false` (matches EnvelopeCodec)
  - Implements `WebMvcConfigurer.configureMessageConverters(...)` OR `extendMessageConverters(...)` to inject a `MappingJackson2HttpMessageConverter` using the bean above.

- [ ] **Step 7.4:** Write `MyBatisConfig.java` — `@Configuration @MapperScan("com.nexacro.fullstack.business.domain")`. DataSource auto-configured from application.yml.

- [ ] **Step 7.5:** Commit (4 commits — pom, Application, WebConfig, MyBatisConfig).

---

## Task 8: application.yml + seed-data wiring

**Files:**
- Create: `.../src/main/resources/application.yml`

- [ ] **Step 8.1:** Write `application.yml`:
  ```yaml
  server:
    port: 8081
    servlet:
      context-path: /uiadapter
  spring:
    datasource:
      url: jdbc:hsqldb:mem:nexacro_boot8;sql.syntax_mys=true
      driver-class-name: org.hsqldb.jdbc.JDBCDriver
      username: sa
      password: ""
    sql:
      init:
        mode: always
        schema-locations: classpath:schema.sql
        data-locations: classpath:data.sql
        separator: "^^"
    servlet:
      multipart:
        enabled: true
        max-file-size: 10MB
        max-request-size: 10MB
  mybatis:
    config-location: classpath:mybatis-config.xml
    mapper-locations: classpath*:com/nexacro/fullstack/business/domain/**/*.xml
  nexacro:
    file:
      storage-dir: ./uploads
  logging:
    level:
      com.nexacro.fullstack: DEBUG
      org.springframework.jdbc: INFO
  ```
  
  Note: different HSQL db name (`nexacro_boot8`) so it doesn't collide if both runners happen to point at the same JVM. (They won't — separate processes — but belt & suspenders.)

- [ ] **Step 8.2:** Commit: `feat(runner-boot8-javax): add application.yml`.

---

## Task 9: Controllers for 5 endpoints (javax.servlet.*)

**Files:**
- Create: `.../controller/LoginController.java`
- Create: `.../controller/BoardController.java`
- Create: `.../controller/DeptController.java`
- Create: `.../controller/LargeController.java`
- Create: `.../controller/FileController.java`

All five extend `NexacroController` from the business tree. **Imports use `javax.servlet.http.HttpSession`** (NOT `jakarta.servlet.http.HttpSession`).

- [ ] **Step 9.1:** `LoginController`:
  - `@PostMapping("/login.do")` accepts `@RequestBody NexacroEnvelope input` + `HttpSession session`.
  - Extract `userId` / `password` via `parameterById(input, "userId")` / `"password"`.
  - Call `userService.login(...)` → wrap result with `NexacroResponseBuilder.ok(result)`.
  - Store `userId` in session.
  - `@PostMapping("/logout.do")` → `session.invalidate()` + `NexacroResponseBuilder.ok()`.

- [ ] **Step 9.2:** `BoardController`:
  - `/sample/board/select.do` → `boardService.selectAll()` → `ok(result)` with dataset id `"board"`.
  - `/sample/board/{insert,update,delete}.do` → all three call `boardService.processRows(datasetById(input, "input"))`, return ok with a single-row dataset `{"affected": n}`.

- [ ] **Step 9.3:** `DeptController`:
  - `/dept/list.do` → `deptService.listAll()`.
  - `/dept/tree.do` → `deptService.tree()`.

- [ ] **Step 9.4:** `LargeController`:
  - `/large/page.do` accepts envelope with Parameters `page`, `pageSize`, optional `category`.
  - Returns envelope with the dataset + a `totalCount` Parameter (use `NexacroResponseBuilder.ok(ds)` then mutate the returned envelope to add the Parameter, OR build the envelope manually).

- [ ] **Step 9.5:** `FileController`:
  - `@PostMapping(value="/file/upload.do", consumes=MediaType.MULTIPART_FORM_DATA_VALUE)` accepts `@RequestParam("file") MultipartFile file` + `@RequestParam("uploadedBy") String uploadedBy`. Returns envelope with the metadata map wrapped as a single-row dataset.
  - `@GetMapping("/file/download.do")` takes `@RequestParam("fileId") String fileId`, returns `ResponseEntity<Resource>` with `Content-Disposition: attachment; filename="..."`.

- [ ] **Step 9.6:** Commit (5 commits — one per controller).

---

## Task 10: Compile + boot + smoke test

- [ ] **Step 10.1:** From monorepo root (with `JAVA_HOME=<jdk8>`):
  ```
  mvn -f samples/shared-business/jdk8-javax/pom.xml install
  mvn -f samples/runners/boot-jdk8-javax/pom.xml package
  ```
  Expect BUILD SUCCESS on both. If Plan 2's jakarta modules got touched, they stay green because they pin their own compiler target to 17 and dependencies by version.

- [ ] **Step 10.2:** Run the runner (in a dedicated shell; leave Plan 2's runner stopped if it's still running to avoid port confusion — though 8080 vs 8081 should be fine):
  ```
  mvn -f samples/runners/boot-jdk8-javax/pom.xml spring-boot:run
  ```
  Expect: `Tomcat started on port(s): 8081 (http) with context path '/uiadapter'`.

- [ ] **Step 10.3:** Smoke test login (new shell):
  ```
  curl -X POST http://localhost:8081/uiadapter/login.do \
    -H "Content-Type: application/json" \
    -d "{\"Parameters\":[{\"id\":\"userId\",\"value\":\"admin\"},{\"id\":\"password\",\"value\":\"stub$admin\"}]}"
  ```
  Expect `ErrorCode: 0` + `output` dataset with a row (USER_ID=admin, ROLE=ADMIN).

- [ ] **Step 10.4:** Smoke test board select:
  ```
  curl -X POST http://localhost:8081/uiadapter/sample/board/select.do \
    -H "Content-Type: application/json" \
    -d "{\"Parameters\":[]}"
  ```
  Expect 5 rows, CONTENT values are plain strings (not `{writer:...}` — proves CLOB normalizer works on Java 8 too).

- [ ] **Step 10.5:** Smoke test large paging:
  ```
  curl -X POST http://localhost:8081/uiadapter/large/page.do \
    -H "Content-Type: application/json" \
    -d "{\"Parameters\":[{\"id\":\"page\",\"value\":1},{\"id\":\"pageSize\",\"value\":50}]}"
  ```
  Expect dataset with 50 rows + `totalCount: 1000` Parameter.

- [ ] **Step 10.6:** (Optional but recommended) **Dual-runner sanity** — if Plan 2's jar is available, start it on 8080 in parallel and confirm both answer independently. This proves the matrix axiom end-to-end. Kill both after.

- [ ] **Step 10.7:** Stop runner. If any smoke test failed, bugfix commits before proceeding. Commit any fixes.

- [ ] **Step 10.8:** Tag `v0.3.0-dual-lane` on the monorepo. Push tag. Update `nexacro-claude-skills` marketplace-relevant docs if needed (plugin version stays v1.8.0 unless we're shipping a scaffold template change).

---

## Self-review checklist

After all tasks complete:
- [ ] Does `mvn package` succeed for both `shared-business-jdk8-javax` and `runner-boot-jdk8-javax`?
- [ ] Does `spring-boot:run` bring up the server cleanly on port **8081** with context path `/uiadapter`?
- [ ] Do all 3 smoke tests (login, board select, large page) return ErrorCode 0 + expected payload?
- [ ] Is there **zero `jakarta.` import** in the Plan 3 source tree? (grep: `grep -r "jakarta\." samples/shared-business/jdk8-javax samples/runners/boot-jdk8-javax` should return nothing)
- [ ] Is there **zero Java 9+ syntax** — no `switch (...) -> `, no `record `, no `List.of`, no `var ` in variable decls? (grep sanity)
- [ ] Does Plan 2's jar still run clean (regression check — they must coexist)?
- [ ] Are all files committed one-per-commit?
- [ ] Is the `v0.3.0-dual-lane` tag pushed?

---

## Execution

Use **superpowers:subagent-driven-development** — dispatch a sonnet implementer subagent per task, spec-review after each, then code-quality review (with explicit "no Java 9+ syntax" check as part of the spec-reviewer prompt for every task). Tasks 1→10 are sequential; Plan 2's artifacts are already in the local Maven repo so Plan 3's business tree can resolve the parent POM on first try.

**Risk watchlist** (carry over from Plan 2):
1. Separator `^^` in application.yml — if omitted, HSQL parser blows up on PSM WHILE loop.
2. CLOB normalizer in BoardService — if omitted, Jackson serialization fails on `JDBCClobClient`.
3. Compiler target 1.8 pinned in BOTH poms — if omitted, JAVA_HOME default may produce class files the jdk8 runtime refuses.
4. javax.servlet.* imports in controllers — if an agent reflexively types `jakarta.servlet.*` (muscle memory from Plan 2), Spring Boot 2.7 + Spring 5.3 won't even start.

Spec reviewer's explicit extra check for every task: **"any `jakarta.` import? any `List.of` / `switch ->` / `record ` keyword? any `<release>17</release>` accidentally left in a pom?"** → if yes, fail the spec review.
