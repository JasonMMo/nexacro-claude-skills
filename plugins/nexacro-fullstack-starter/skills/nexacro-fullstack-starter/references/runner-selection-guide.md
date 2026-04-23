# Runner Selection Guide

어떤 runner를 골라야 할지 모를 때 보는 의사결정 가이드.

## Decision tree

```
Q1. JDK 버전이 17 이상인가?
├── Yes (17+) ──► servletApi = jakarta
│   │
│   Q2. WebFlux reactive 구현이 필요한가?
│   ├── Yes ──► webflux-jdk17-jakarta
│   └── No
│       │
│       Q3. eGov 표준프레임워크 사용?
│       ├── Yes ──► egov5-boot-jdk17-jakarta  (eGov 5.x)
│       └── No
│           │
│           Q4. war 패키징(전통 MVC) 필요?
│           ├── Yes ──► mvc-jdk17-jakarta
│           └── No  ──► boot-jdk17-jakarta   ★ 대부분 이것
│
└── No (8/11) ──► servletApi = javax
    │
    Q2'. eGov 표준프레임워크 사용?
    ├── Yes
    │   │
    │   Q3'. war 패키징?
    │   ├── Yes ──► egov4-mvc-jdk8-javax
    │   └── No  ──► egov4-boot-jdk8-javax
    │
    └── No
        │
        Q3'. war 패키징?
        ├── Yes ──► mvc-jdk8-javax
        └── No  ──► boot-jdk8-javax
```

## "어떤 걸 고를지 모르겠다" — 기본값 추천

| 상황 | 추천 runner | 이유 |
|---|---|---|
| 신규 프로젝트, 제약 없음 | `boot-jdk17-jakarta` | 최신 스택, 가장 간단한 실행 (`mvn spring-boot:run`) |
| 기존 jdk8 환경 유지 필요 | `boot-jdk8-javax` | javax 기반 레거시 호환 |
| 공공기관 프로젝트 | `egov5-boot-jdk17-jakarta` | 표준프레임워크 최신 |
| 공공기관 jdk8 필수 | `egov4-boot-jdk8-javax` | 표준프레임워크 4.x |
| 레거시 war 배포 서버 | `mvc-jdk{8|17}-{javax|jakarta}` | 전통 Tomcat war |
| 대용량 비동기 / 스트리밍 | `webflux-jdk17-jakarta` | Reactive, 단 학습 곡선 있음 |

## WebFlux 를 고르기 전 체크리스트

WebFlux는 개발 진입장벽이 있으니 아래를 확인하세요:

- [ ] 반드시 비동기/논블로킹 필요한가? (대부분의 CRUD 업무는 Boot로 충분)
- [ ] 팀이 `Mono<>`/`Flux<>` 패턴에 익숙한가?
- [ ] MyBatis 사용 고수? (WebFlux + MyBatis 는 동기 래핑 한계 존재)
- [ ] 예외 처리, 트랜잭션 재설계 시간이 있는가?

하나라도 "아니오" 면 `boot-jdk17-jakarta` 가 안전합니다.

## 호환성 미매치 사례

### "egov-mvc + jdk17" 를 시도한 경우

→ Step 2 에서 거부됨. 이유: eGov4 MVC + jdk17/jakarta 공식 샘플 미존재.
→ 대안 추천: `egov5-boot-jdk17-jakarta` (eGov 최신 + Boot 3)

### "webflux + jdk8" 를 시도한 경우

→ Step 2 에서 거부됨. 이유: WebFlux는 Spring 6/jakarta/jdk17+ 조합만 지원.
→ 대안 추천: `boot-jdk8-javax` (동기 Boot 2)

## 추후 지원 예정

- `nexacro17-fullstack` — nexacro17 버전 (별도 repo)
- `nexacro14-fullstack` — nexacro14 버전 (별도 repo)
- `egov4-mvc-jdk17-jakarta` — 요청 받으면 추가 검토
- R2DBC 기반 reactive — `webflux-jdk17-jakarta-r2dbc` 신규 runner로 추가
