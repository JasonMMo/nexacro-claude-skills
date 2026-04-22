# xadl Frame 스타일 패턴

Nexacro Application (`.xadl`) 의 **프레임 트리** 구성 방식을 두 가지 스킬 내장 스타일로 제공합니다. 스킬 실행 시 "프레임 스타일" 단계에서 선택.

## 1. Frame Tree 개념

`.xadl` 파일은 `<Application>` 밑에 `<Layout>` 을 두고, 그 안에 **하나의 `<MainFrame>`** 을 둡니다. `<MainFrame>` 의 자식으로 `<VFrameSet>` / `<HFrameSet>` / `<FrameSet>` / `<ChildFrame>` 을 조합해서 화면을 영역으로 분할합니다.

| 엘리먼트 | 의미 |
|---|---|
| `MainFrame` | 최상위 창. 타이틀바 / 스테이터스바 옵션 보유 |
| `VFrameSet` | **수직 분할** (위/아래). `separatesize="44,*,0"` = 위 44, 가운데 남은 전부, 아래 0 |
| `HFrameSet` | **수평 분할** (좌/우). `separatesize="240,*"` = 좌 240, 우 남은 전부 |
| `FrameSet` | 빈 컨테이너 (MDI 워크영역 등, 런타임 동적 프레임 할당용) |
| `ChildFrame` | 실제 `.xfdl` 폼을 로드하는 리프. `formurl="<service>::<form>.xfdl"` |

> 공식 문서:
> - Frame 개요: https://docs.tobesoft.com/development_tools_guide_nexacro_n_v24_ko/d3c24416f769f7e9#485f5f9220d8b300
> - Frame Tree: https://docs.tobesoft.com/advanced_development_guide_nexacro_n_v24_ko/9757e8a35237f855

## 2. minimal 스타일 (기본값)

단일 `ChildFrame` 만 두는 가장 단순한 형태. SPA 성격, 프레임 분할 없음.

```
MainFrame (1280×800)
└── ChildFrame childframe0 → {{FORM_PREFIX}}::main.xfdl
```

**언제 사용**
- 프로토타입 / POC
- 단일 화면 도구 (계산기, 입력 폼 하나)
- 프레임 트리가 나중에 결정될 때의 빈 출발점

**파일 구성** — `assets/skeleton/{{PROJECT_NAME}}.xadl`

## 3. packageN 스타일 (MDI / 프레임셋)

`nexacron/spring-boot/jakarta/uiadapter-jakarta` 공식 샘플의 `packageN.xadl` 프레임 트리를 베이스로 한 **업무 시스템 풀 레이아웃**. 로그인 오버레이 + 탑/좌메뉴/MDI 탭/메인/바텀 6영역 구조.

### 프레임 트리

```
MainFrame (1280×984)
└── VFrameSet [44, 0, *, 0]                          ← 수직 4단
    ├── ChildFrame frameTop    → frame::frameTop.xfdl      (헤더, 높이 44)
    ├── ChildFrame frameLogin  → 동적 할당 (frame::frameLogin.xfdl)
    ├── HFrameSet [240, *]                           ← 수평 2단
    │   ├── ChildFrame frameLeft  → frame::frameLeft.xfdl  (좌측 메뉴, 너비 240)
    │   └── VFrameSet1 [32, *, 0]                    ← 수직 3단
    │       ├── ChildFrame frameNavi  → frame::frameMDI.xfdl   (MDI 탭 바, 높이 32)
    │       ├── FrameSet framesetWork                 (빈 MDI 워크영역, 런타임 할당)
    │       └── ChildFrame frameMain  → frame::frameMain.xfdl  (메인 폼)
    └── ChildFrame frameBottom → frame::frameBottom.xfdl   (푸터)
```

### 각 프레임 역할

| Frame | 파일 | 역할 |
|---|---|---|
| `frameTop` | `frame/frameTop.xfdl` | 공통 헤더 (로고 / 사용자정보 / 로그아웃) |
| `frameLogin` | `frame/frameLogin.xfdl` | 로그인 오버레이 — `onload` 시 동적 표시, 성공 시 숨김 |
| `frameLeft` | `frame/frameLeft.xfdl` | 좌측 메뉴 트리 (leftFrame) |
| `frameNavi` | `frame/frameMDI.xfdl` | 열린 탭 바 (MDI navigation) |
| `framesetWork` | (empty FrameSet) | 사용자가 연 업무 화면이 런타임에 붙는 영역 |
| `frameMain` | `frame/frameMain.xfdl` | 기본 초기 메인 폼 (대시보드 등) |
| `frameBottom` | `frame/frameBottom.xfdl` | 공통 푸터 (상태바 / 저작권) |

### 전역 변수 (Application `<Script>`)

`Application_onload` 에서 모든 프레임 레퍼런스를 전역변수로 캐시:

```js
this.gvVFrameSet    = objApp.mainframe.VFrameSet;
this.gvLoginFrame   = objApp.mainframe.VFrameSet.frameLogin;
this.gvHFrame       = objApp.mainframe.VFrameSet.HFrameSet;
this.gvLeftFrame    = objApp.mainframe.VFrameSet.HFrameSet.frameLeft;
this.gvTopFrame     = objApp.mainframe.VFrameSet.frameTop;
this.gvWorkFrame    = objApp.mainframe.VFrameSet.HFrameSet.VFrameSet1.framesetWork;
this.gvMainFrame    = objApp.mainframe.VFrameSet.HFrameSet.VFrameSet1.frameMain;
this.gvMdiFrame     = objApp.mainframe.VFrameSet.HFrameSet.VFrameSet1.frameNavi;
```

### 필수 서비스 prefix

packageN 스타일은 `frame::` 서비스가 필수. `typedefinition.xml` 에 자동 등록됨:

```xml
<Service prefixid="frame" type="form" url="./frame/" cachelevel="session" .../>
```

### 번들된 보조 파일

| 파일 | 목적 |
|---|---|
| `frame/frameWork.xfdl` | MDI 런타임 워크 페이지 (framesetWork 에 동적 할당) |
| `frame/frameWorkTitle.xfdl` | MDI 탭 제목 바 |

이 두 파일은 `.xadl` 에서 직접 참조하지 않지만, `frameMDI.xfdl` 의 탭 스크립트가 런타임에 로드합니다.

### 언제 사용

- 업무 시스템 (ERP / 그룹웨어 / 기간계)
- 좌측 메뉴 + MDI 탭 기반 UX
- 로그인 세션 관리 포함 실전 스캐폴드
- Spring Boot / Spring WebFlux 와 연동되는 프론트 (packageN 은 `uiadapter-jakarta` 의 기본 UI)

**파일 구성** — `assets/skeleton-frames/packageN/`

## 4. 선택 기준표

| 요구사항 | minimal | packageN |
|---|---|---|
| 단일 화면 POC | ✅ | ❌ 과함 |
| 좌측 메뉴 + MDI | ❌ 부족 | ✅ |
| 로그인 오버레이 | ❌ 직접 구현 | ✅ 내장 |
| 파일 수 | 1 xadl | 1 xadl + 8 xfdl + appvariables |
| 전역변수 보일러플레이트 | 없음 | 있음 |
| 학습 난이도 | 낮음 | 중간 (`<FrameSet>` 구조 이해 필요) |
| `nexacrolib` 필요 | extPrototype 선택 | extPrototype / ListView / traceLog 필수 |

## 5. 커스터마이징 팁

**packageN 스타일 기반으로 영역 조정**
- `VFrameSet separatesize` 값만 바꾸면 각 영역 크기 조정
- 예: 좌측 메뉴 300px → `HFrameSet separatesize="300,*"`
- 바텀 숨기기 → `VFrameSet separatesize="44,0,*,0"` 을 `"44,0,*"` 로 변경 + 마지막 ChildFrame 제거

**프레임 xfdl 내용 교체**
- 각 `frame/*.xfdl` 은 그대로 사용하거나 `nexacro-form-maker` 스킬로 재작성 가능
- `frameLeft.xfdl` 의 메뉴 Dataset 은 서버에서 받아 채우는 게 일반적
