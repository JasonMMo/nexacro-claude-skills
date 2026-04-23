# Compatibility Matrix Reference

Derivation rules and the current 8-runner matrix for `nexacroN-fullstack`.

## Derivation rules

User picks 4 values. Everything else is derived.

```
User picks:  nexacroVersion (= nexacroN), jdk, framework, projectName

Derived:
  servletApi   = (jdk >= 17) ? "jakarta" : "javax"
  springMajor  = (servletApi == "jakarta") ? 6 : 5
  bootMajor    = framework ∈ {spring-boot, egov-boot, webflux}
                   ? (servletApi == "jakarta" ? 3 : 2)
                   : null
  egovMajor    = (framework == "egov-boot")
                   ? (servletApi == "jakarta" ? 5 : 4)
                   : (framework == "egov-mvc") ? 4 : null
  packaging    = framework ∈ {spring-mvc, egov-mvc} ? "war" : "jar"
```

## 8-runner matrix (nexacroN)

| # | runner key | jdk | servletApi | framework | springMajor | bootMajor | egovMajor | packaging |
|---|---|---|---|---|---|---|---|---|
| 1 | `boot-jdk17-jakarta` | 17 | jakarta | spring-boot | 6 | 3 | — | jar |
| 2 | `boot-jdk8-javax` | 8 | javax | spring-boot | 5 | 2 | — | jar |
| 3 | `mvc-jdk17-jakarta` | 17 | jakarta | spring-mvc | 6 | — | — | war |
| 4 | `mvc-jdk8-javax` | 8 | javax | spring-mvc | 5 | — | — | war |
| 5 | `egov5-boot-jdk17-jakarta` | 17 | jakarta | egov-boot | 6 | 3 | 5 | jar |
| 6 | `egov4-boot-jdk8-javax` | 8 | javax | egov-boot | 5 | 2 | 4 | jar |
| 7 | `egov4-mvc-jdk8-javax` | 8 | javax | egov-mvc | 5 | — | 4 | war |
| 8 | `webflux-jdk17-jakarta` | 17 | jakarta | webflux | 6 | 3 | — | jar |

## Business tree sharing

Runners share JVM source where structure is identical.

| Business tree | Shared by runners |
|---|---|
| `samples/shared-business/jdk8-javax` | `boot-jdk8-javax`, `mvc-jdk8-javax` |
| `samples/shared-business/jdk17-jakarta` | `boot-jdk17-jakarta`, `mvc-jdk17-jakarta` |
| `samples/shared-business-egov4/jdk8-javax` | `egov4-boot-jdk8-javax`, `egov4-mvc-jdk8-javax` |
| `samples/shared-business-egov5/jdk17-jakarta` | `egov5-boot-jdk17-jakarta` |
| `samples/shared-business-reactive/jdk17-mybatis` | `webflux-jdk17-jakarta` |

→ 5 trees, 8 runners. Edit business logic once, all matching runners pick it up.

## Rejected combinations

Checked in Step 2 of SKILL.md.

| Input | Reason | Alternative |
|---|---|---|
| `framework=egov-mvc + jdk=17` | eGov4 MVC jdk17/jakarta sample does not exist | `egov5-boot-jdk17-jakarta` |
| `framework=webflux + jdk=8` | WebFlux requires jdk17+ jakarta | `boot-jdk8-javax` |
| `nexacroVersion ≠ nexacroN` | Only nexacroN is implemented in v0.1.0 | wait for `nexacro17-fullstack` / `nexacro14-fullstack` (future) |

## servletApi cross-reference

| jdk | servlet-api | javax → jakarta import changes |
|---|---|---|
| 8, 11 | `javax.servlet.*` | uses `javax.servlet.http.HttpServletRequest` |
| 17+ | `jakarta.servlet.*` | uses `jakarta.servlet.http.HttpServletRequest` |

This alone forces per-JDK business trees (cannot share source across `javax`/`jakarta`).
