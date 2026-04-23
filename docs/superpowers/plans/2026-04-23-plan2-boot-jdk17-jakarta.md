# Plan 2 — Flagship Runner: `boot-jdk17-jakarta` End-to-End

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `samples/runners/boot-jdk17-jakarta/` actually run (`mvn spring-boot:run`) and serve 5 canonical Nexacro-dataset endpoints (login, board CRUD with `_RowType_` dispatch, dept tree, large-data paging, file upload/download) backed by the `samples/shared-business/jdk17-jakarta/` business tree and the HSQL seed DB from Plan 1.

**Architecture:**
- Spring Boot 3.3.x on JDK 17, jakarta servlet API, Maven jar packaging
- Controllers in the runner are thin HTTP adapters; all logic lives in the business tree (xapi core + uiadapter handlers + services + DAOs against HSQL)
- Nexacro wire format: **JSON only for Plan 2** (XML/SSV deferred to later plan). Uses the `NexacroDatasetEnvelope` contract from `api-contract/openapi.yaml`.
- HSQL in-memory from seed-data loaded automatically at boot via `spring.sql.init.mode=always`.

**Tech Stack:**
- spring-boot 3.3.5 (parent BOM)
- spring 6.1.x
- MyBatis Spring Boot Starter 3.0.x (jakarta lane)
- HSQLDB 2.7.3
- Jackson for JSON envelope serde
- Lombok for DTO boilerplate

**Out of scope (defer to later plans):**
- XML and SSV wire formats (JSON only for now)
- `/excel/export.do` (needs xeni work)
- `/reactive/exim_exchange.do` (webflux-only)
- Integration tests (manual curl smoke-check only)
- The other 7 runners + business trees (Plans 3-6)

---

## File Structure (Plan 2)

**Business tree — `samples/shared-business/jdk17-jakarta/`:**
```
pom.xml                                  (jakarta lane deps, inherits parent)
src/main/java/com/nexacro/fullstack/business/
  xapi/
    NexacroDataset.java                  (dataset POJO — columns + rows)
    NexacroEnvelope.java                 (top-level: parameters + datasets list)
    RowType.java                         (enum N/I/U/D/O)
    EnvelopeCodec.java                   (JSON encode/decode via Jackson)
  uiadapter/
    NexacroController.java               (@RestController base + error wrapper)
    NexacroResponseBuilder.java          (builds error/ok envelopes)
  domain/
    user/
      UserService.java
      UserDao.java                       (@Mapper)
      UserDao.xml                        (login/select SQL)
    board/
      BoardService.java                  (dispatches _RowType_)
      BoardDao.java                      (@Mapper)
      BoardDao.xml
    dept/
      DeptService.java
      DeptDao.java
      DeptDao.xml                        (WITH RECURSIVE for tree)
    large/
      LargeDataService.java
      LargeDataDao.java
      LargeDataDao.xml                   (OFFSET/FETCH paging)
    file/
      FileService.java                   (local filesystem under ./uploads/)
      FileDao.java
      FileDao.xml
src/main/resources/
  mybatis-config.xml
```

**Runner — `samples/runners/boot-jdk17-jakarta/`:**
```
pom.xml                                  (inherits parent, depends on business tree, spring-boot-starter-web)
src/main/java/com/nexacro/fullstack/runner/boot17/
  Application.java                       (@SpringBootApplication main)
  config/
    WebConfig.java                       (context path /uiadapter, JSON message converter)
    MyBatisConfig.java                   (mapper scan, datasource)
  controller/
    LoginController.java                 (/login.do, /logout.do)
    BoardController.java                 (/sample/board/{select,insert,update,delete}.do)
    DeptController.java                  (/dept/{list,tree}.do)
    LargeController.java                 (/large/page.do)
    FileController.java                  (/file/upload.do, /file/download.do)
src/main/resources/
  application.yml                        (port 8080, context-path /uiadapter, HSQL, seed-data paths)
  logback-spring.xml                     (minimal console logger)
```

**Design decisions locked in:**
- `NexacroDataset` and `NexacroEnvelope` are plain POJOs with Lombok `@Data`. Deliberately NOT using MapStruct — keeps the business tree dependency footprint minimal for this flagship.
- `_RowType_` dispatch lives in `BoardService` for now (generic `AbstractRowTypeDispatcher` extracted in a later plan if duplication emerges).
- File storage is local-filesystem (`./uploads/`) — no S3 adapter for Plan 2.
- No Spring Security. Login is a stub that checks `PASSWORD_HASH LIKE 'stub$%'` against the seed row. Session is stored in HttpSession only.
- Errors return `{"Parameters":[{"id":"ErrorCode","value":-1},{"id":"ErrorMsg","value":"..."}]}` per Nexacro convention.

---

## Task 1: Business tree scaffold + xapi core

**Files:**
- Create: `D:\AI\workspace\nexacroN-fullstack\samples\shared-business\jdk17-jakarta\pom.xml`
- Create: `.../xapi/NexacroDataset.java`
- Create: `.../xapi/NexacroEnvelope.java`
- Create: `.../xapi/RowType.java`
- Create: `.../xapi/EnvelopeCodec.java`

- [ ] **Step 1.1:** Write `pom.xml` — artifactId `shared-business-jdk17-jakarta`, packaging `jar`, parent is the monorepo root POM (`com.nexacro.fullstack:nexacroN-fullstack-parent:0.1.0-SNAPSHOT`). Deps: `jakarta.servlet-api` (provided), `spring-context`, `spring-jdbc`, `mybatis-spring-boot-starter`, `hsqldb` (runtime), `jackson-databind`, `lombok` (provided), `commons-io`.

- [ ] **Step 1.2:** Write `RowType.java` — enum with values `N, I, U, D, O` and a static `fromString(String)` tolerant of null/empty.

- [ ] **Step 1.3:** Write `NexacroDataset.java` — Lombok `@Data` POJO: `String id`, `List<ConstColumn> constColumns`, `List<Column> columns`, `List<Map<String,Object>> rows`. Nested classes `ConstColumn(id, type, size, value)` and `Column(id, type, size)`. Row `_RowType_` is stored in the map.

- [ ] **Step 1.4:** Write `NexacroEnvelope.java` — Lombok `@Data` POJO: `String version` (default "1.0"), `List<Parameter> parameters`, `List<NexacroDataset> datasets`. Nested `Parameter(id, value, type)`.

- [ ] **Step 1.5:** Write `EnvelopeCodec.java` — Jackson-based encode/decode. Two static methods: `NexacroEnvelope decode(InputStream)` and `void encode(NexacroEnvelope, OutputStream)`. Use `ObjectMapper` configured with `FAIL_ON_UNKNOWN_PROPERTIES=false`. Handle the `Parameters`/`Datasets` key-case from the wire spec (capitals) via `@JsonProperty`.

- [ ] **Step 1.6:** Commit. Message: `feat(business-jdk17-jakarta): add xapi core (envelope, dataset, rowtype, codec)`.

---

## Task 2: uiadapter base + response builder

**Files:**
- Create: `.../uiadapter/NexacroController.java`
- Create: `.../uiadapter/NexacroResponseBuilder.java`

- [ ] **Step 2.1:** Write `NexacroResponseBuilder.java` — static helpers: `ok(NexacroDataset... datasets)`, `error(int code, String message)`, `errorFromException(Throwable t)`. Each returns a `NexacroEnvelope` with proper Parameters (ErrorCode, ErrorMsg) pre-populated.

- [ ] **Step 2.2:** Write `NexacroController.java` — abstract base with `@ExceptionHandler(Exception.class)` that returns `NexacroResponseBuilder.errorFromException(...)`. Protected helper `datasetById(NexacroEnvelope, String id)` to look up input datasets by id.

- [ ] **Step 2.3:** Commit. Message: `feat(business-jdk17-jakarta): add uiadapter base controller + response builder`.

---

## Task 3: User domain (for /login.do)

**Files:**
- Create: `.../domain/user/UserService.java`
- Create: `.../domain/user/UserDao.java`
- Create: `.../domain/user/UserDao.xml`

- [ ] **Step 3.1:** Write `UserDao.java` — `@Mapper` interface. Methods: `Map<String,Object> findById(String userId)`, `int updateLastLogin(String userId)`.

- [ ] **Step 3.2:** Write `UserDao.xml` — MyBatis mapper. `SELECT USER_ID, USER_NAME, PASSWORD_HASH, EMAIL, ROLE, ENABLED FROM USERS WHERE USER_ID = #{userId} AND ENABLED = TRUE`. For now the update method is a no-op INSERT/UPDATE stub (Plan 2 does not add a LAST_LOGIN column).

- [ ] **Step 3.3:** Write `UserService.java` — `@Service` with method `NexacroDataset login(String userId, String password)`. Looks up user, compares `PASSWORD_HASH` against `"stub$" + userId` (seed-data convention), returns a single-row dataset with USER_ID + USER_NAME + ROLE on success, or throws `IllegalArgumentException` on failure.

- [ ] **Step 3.4:** Commit. Message: `feat(business-jdk17-jakarta): add user domain (login stub)`.

---

## Task 4: Board domain with `_RowType_` dispatch (/sample/board/*)

**Files:**
- Create: `.../domain/board/BoardService.java`
- Create: `.../domain/board/BoardDao.java`
- Create: `.../domain/board/BoardDao.xml`

- [ ] **Step 4.1:** Write `BoardDao.java` — `@Mapper` with `selectAll`, `selectById(int)`, `insert(Map)`, `update(Map)`, `softDelete(int)`.

- [ ] **Step 4.2:** Write `BoardDao.xml` — SQL for each. Soft delete sets `DELETED = TRUE, UPDATED_AT = CURRENT_TIMESTAMP`. Insert relies on `GENERATED BY DEFAULT AS IDENTITY` and returns the key via `useGeneratedKeys="true" keyProperty="BOARD_ID"`.

- [ ] **Step 4.3:** Write `BoardService.java` — `@Service`. Method `NexacroDataset selectAll()` for queries. Method `int processRows(NexacroDataset input)` that iterates rows, reads `_RowType_`, dispatches: `N/O` → skip (N=new stub, O=original — ignored), `I` → `dao.insert`, `U` → `dao.update`, `D` → `dao.softDelete`. Returns count of affected rows. Wrapped in `@Transactional`.

- [ ] **Step 4.4:** Commit. Message: `feat(business-jdk17-jakarta): add board domain with _RowType_ dispatch`.

---

## Task 5: Dept tree + Large paging + File upload domains

**Files:**
- Create: `.../domain/dept/{DeptService,DeptDao}.java` + `DeptDao.xml`
- Create: `.../domain/large/{LargeDataService,LargeDataDao}.java` + `LargeDataDao.xml`
- Create: `.../domain/file/{FileService,FileDao}.java` + `FileDao.xml`

- [ ] **Step 5.1:** Write Dept mapper — `listAll` (flat SELECT ordered by LEVEL_NO, SORT_ORDER), `tree` (CTE `WITH RECURSIVE` building a materialized path + level).

- [ ] **Step 5.2:** Write `DeptService` — returns NexacroDataset with columns DEPT_ID, DEPT_NAME, PARENT_ID, LEVEL_NO, SORT_ORDER.

- [ ] **Step 5.3:** Write Large mapper — `count()` and `page(int offset, int limit, String category)`. Use HSQL `OFFSET ? ROWS FETCH NEXT ? ROWS ONLY`.

- [ ] **Step 5.4:** Write `LargeDataService` — accepts page (1-indexed) + pageSize, returns dataset + total count as Parameters.

- [ ] **Step 5.5:** Write File mapper — `insert(Map)`, `findById(String)`, `listAll()`.

- [ ] **Step 5.6:** Write `FileService` — `upload(MultipartFile, String uploadedBy)` stores to `./uploads/{uuid}-{original}`, records metadata via dao.insert. `download(String fileId)` returns `Resource` + metadata. `list()` returns full metadata dataset.

- [ ] **Step 5.7:** Commit. Message: `feat(business-jdk17-jakarta): add dept/large/file domains`.

---

## Task 6: mybatis-config.xml + build sanity

**Files:**
- Create: `.../src/main/resources/mybatis-config.xml`

- [ ] **Step 6.1:** Write `mybatis-config.xml` — `<settings>` with `mapUnderscoreToCamelCase=true`, `defaultStatementTimeout=30`. No type aliases needed yet.

- [ ] **Step 6.2:** Run `mvn -pl samples/shared-business/jdk17-jakarta -am compile` from monorepo root. Expect BUILD SUCCESS. If the parent POM isn't aggregator (it isn't), use `mvn -f samples/shared-business/jdk17-jakarta/pom.xml compile`.

- [ ] **Step 6.3:** Commit. Message: `feat(business-jdk17-jakarta): add mybatis-config + verify compile`.

---

## Task 7: Runner pom.xml + Application.java + config classes

**Files:**
- Modify: `D:\AI\workspace\nexacroN-fullstack\samples\runners\boot-jdk17-jakarta\pom.xml` (currently just README — create pom)
- Create: `.../src/main/java/com/nexacro/fullstack/runner/boot17/Application.java`
- Create: `.../config/WebConfig.java`
- Create: `.../config/MyBatisConfig.java`

- [ ] **Step 7.1:** Create runner `pom.xml` — artifactId `runner-boot-jdk17-jakarta`, packaging `jar`, parent is monorepo root. Deps: `shared-business-jdk17-jakarta` (same groupId), `spring-boot-starter-web`, `spring-boot-starter-jdbc`, `mybatis-spring-boot-starter`. Plugin: `spring-boot-maven-plugin` with `mainClass` = `com.nexacro.fullstack.runner.boot17.Application`.

- [ ] **Step 7.2:** Write `Application.java` — `@SpringBootApplication(scanBasePackages={"com.nexacro.fullstack.runner.boot17","com.nexacro.fullstack.business"})` with `main`.

- [ ] **Step 7.3:** Write `WebConfig.java` — `@Configuration`. Registers a `MappingJackson2HttpMessageConverter` with the shared `ObjectMapper` used by `EnvelopeCodec`. No CORS for Plan 2 (same-origin).

- [ ] **Step 7.4:** Write `MyBatisConfig.java` — `@Configuration`, `@MapperScan("com.nexacro.fullstack.business.domain")`. DataSource is auto-configured by Spring Boot from application.yml.

- [ ] **Step 7.5:** Commit. Message: `feat(runner-boot17-jakarta): add pom + Application + configs`.

---

## Task 8: application.yml + seed-data wiring

**Files:**
- Create: `.../src/main/resources/application.yml`
- Create: `.../src/main/resources/schema.sql` (symlink or copy pointer — see step 8.2)
- Create: `.../src/main/resources/data.sql`

- [ ] **Step 8.1:** Write `application.yml`:
```yaml
server:
  port: 8080
  servlet:
    context-path: /uiadapter
spring:
  datasource:
    url: jdbc:hsqldb:mem:nexacro;sql.syntax_mys=true
    driver-class-name: org.hsqldb.jdbc.JDBCDriver
    username: sa
    password: ""
  sql:
    init:
      mode: always
      schema-locations: classpath:schema.sql
      data-locations: classpath:data.sql
  servlet:
    multipart:
      max-file-size: 10MB
      max-request-size: 10MB
mybatis:
  config-location: classpath:mybatis-config.xml
  mapper-locations: classpath*:com/nexacro/fullstack/business/domain/**/*.xml
logging:
  level:
    com.nexacro.fullstack: DEBUG
    org.springframework.jdbc: INFO
```

- [ ] **Step 8.2:** Copy (not symlink — Windows) `samples/seed-data/schema.sql` and `samples/seed-data/data.sql` into `.../src/main/resources/` via maven-resources-plugin in the runner pom. Add plugin config:
```xml
<plugin>
  <artifactId>maven-resources-plugin</artifactId>
  <executions>
    <execution>
      <id>copy-seed-data</id>
      <phase>generate-resources</phase>
      <goals><goal>copy-resources</goal></goals>
      <configuration>
        <outputDirectory>${project.build.outputDirectory}</outputDirectory>
        <resources>
          <resource>
            <directory>${project.basedir}/../../seed-data</directory>
            <includes><include>schema.sql</include><include>data.sql</include></includes>
          </resource>
        </resources>
      </configuration>
    </execution>
  </executions>
</plugin>
```
(No physical copies in git — seed-data stays single-source.)

- [ ] **Step 8.3:** Commit. Message: `feat(runner-boot17-jakarta): add application.yml + seed-data wiring`.

---

## Task 9: Controllers for 5 endpoints

**Files:**
- Create: `.../controller/LoginController.java`
- Create: `.../controller/BoardController.java`
- Create: `.../controller/DeptController.java`
- Create: `.../controller/LargeController.java`
- Create: `.../controller/FileController.java`

- [ ] **Step 9.1:** `LoginController` — `POST /login.do` accepts `NexacroEnvelope`, pulls `userId`/`password` from Parameters, delegates to `UserService.login`, returns envelope with `output` dataset. `POST /logout.do` invalidates HttpSession, returns empty-ok envelope.

- [ ] **Step 9.2:** `BoardController` — four endpoints:
  - `POST /sample/board/select.do` → `boardService.selectAll()` → dataset `board`
  - `POST /sample/board/insert.do` → `boardService.processRows(input.dataset("input"))`
  - `POST /sample/board/update.do` → same dispatcher
  - `POST /sample/board/delete.do` → same dispatcher
  (All four actions use the same `processRows` — the URL is informational; Nexacro client sends the envelope with mixed `_RowType_` rows.)

- [ ] **Step 9.3:** `DeptController` — `POST /dept/list.do` (flat), `POST /dept/tree.do` (recursive CTE result with computed LEVEL_NO).

- [ ] **Step 9.4:** `LargeController` — `POST /large/page.do` accepts Parameters `page`, `pageSize`, optional `category`. Returns dataset + `totalCount` parameter.

- [ ] **Step 9.5:** `FileController` — `POST /file/upload.do` accepts `multipart/form-data` (NOT envelope) with fields `file` + `uploadedBy`. Returns envelope with file metadata. `GET /file/download.do?fileId=...` returns the binary with Content-Disposition.

- [ ] **Step 9.6:** Commit (5 commits — one per controller file per the repo's `Git Commit Rules`).

---

## Task 10: Compile + boot + smoke test

- [ ] **Step 10.1:** From monorepo root:
```
mvn -f samples/shared-business/jdk17-jakarta/pom.xml install
mvn -f samples/runners/boot-jdk17-jakarta/pom.xml package
```
Expect BUILD SUCCESS on both.

- [ ] **Step 10.2:** Run the runner:
```
mvn -f samples/runners/boot-jdk17-jakarta/pom.xml spring-boot:run
```
Expect startup log showing `Tomcat started on port(s): 8080 (http) with context path '/uiadapter'`.

- [ ] **Step 10.3:** Smoke test with curl (new shell):
```
curl -X POST http://localhost:8080/uiadapter/login.do \
  -H "Content-Type: application/json" \
  -d '{"Parameters":[{"id":"userId","value":"admin"},{"id":"password","value":"stub$admin"}]}'
```
Expect `ErrorCode: 0` and `output` dataset with a row.

- [ ] **Step 10.4:** Smoke test board select:
```
curl -X POST http://localhost:8080/uiadapter/sample/board/select.do \
  -H "Content-Type: application/json" \
  -d '{"Parameters":[]}'
```
Expect 5 rows.

- [ ] **Step 10.5:** Smoke test large paging:
```
curl -X POST http://localhost:8080/uiadapter/large/page.do \
  -H "Content-Type: application/json" \
  -d '{"Parameters":[{"id":"page","value":1},{"id":"pageSize","value":50}]}'
```
Expect 50 rows + `totalCount: 1000`.

- [ ] **Step 10.6:** Stop runner. If any smoke test failed, bugfix commit(s) before proceeding.

- [ ] **Step 10.7:** Commit any fixes. Tag `v0.2.0-flagship` on the monorepo. Push tag.

---

## Self-review checklist

After all tasks complete:
- [ ] Does `mvn package` succeed for both modules?
- [ ] Does `spring-boot:run` bring up the server cleanly on port 8080 with context path `/uiadapter`?
- [ ] Do all 5 smoke tests return ErrorCode 0 + expected payload?
- [ ] Are all files committed with file-per-commit granularity?
- [ ] Is the `v0.2.0-flagship` tag pushed?

## Execution

Use **superpowers:subagent-driven-development** — dispatch a sonnet implementer subagent per task, spec-review after each, then code-quality review. Tasks 1→10 are sequential (later tasks depend on earlier compile artifacts). Tasks 3-5 can conceptually parallelize but we serialize to keep commit history clean.
