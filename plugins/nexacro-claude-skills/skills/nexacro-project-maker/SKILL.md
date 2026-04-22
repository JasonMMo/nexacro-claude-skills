---
name: nexacro-project-maker
description: Nexacro N v24 프로젝트 스캐폴드 생성기. 빈 디렉터리에 .xprj / .xadl / typedefinition / environment / appvariables / bootstrap / Base/main.xfdl 을 플레이스홀더 치환으로 생성하며, 프레임 스타일(minimal / packageN MDI)을 선택할 수 있습니다. 사용 트리거 — "nexacro 프로젝트 만들어", "nexacro 프로젝트 생성", "xprj 만들어", "nexacro 스캐폴드", "nexacro project maker", "nexacro project scaffold", "packageN 스타일", "MDI 프레임"
---

# Nexacro Project Maker

빈 디렉터리에 Nexacro N v24 **flat-layout** 프로젝트를 스캐폴드합니다.
(참고: Nexacro 24 공식 샘플 `sample_Nexacro_N_V24` + `nexacron/uiadapter-jakarta/packageN` 구조를 베이스로 단순화)

## 생성되는 파일 구조

**minimal 스타일 (기본, 7 파일)**

```
<target-dir>/
├── <PROJECT_NAME>.xprj       # 프로젝트 엔트리
├── <PROJECT_NAME>.xadl       # Application/MainFrame 선언 (단일 ChildFrame)
├── typedefinition.xml        # 컴포넌트 모듈 + 서비스 prefix
├── environment.xml           # 테마 / 스크린 / 쿠키
├── appvariables.xml          # 앱 전역 변수
├── bootstrap.xml             # HTML 로더 템플릿 (공식 템플릿 그대로)
└── Base/
    └── main.xfdl             # 기동 확인용 최소 폼 (Hello, Nexacro!)
```

**packageN 스타일 (MDI / 프레임셋, 15 파일)**

```
<target-dir>/
├── <PROJECT_NAME>.xprj
├── <PROJECT_NAME>.xadl       # VFrameSet + HFrameSet MDI 레이아웃
├── typedefinition.xml        # frame:: 서비스 prefix 포함
├── environment.xml
├── appvariables.xml          # 메뉴/세션 전역변수 포함 (packageN 기반)
├── bootstrap.xml
├── Base/main.xfdl            # (보조) 기동 확인용
└── frame/                    # ← packageN 스타일 전용 폼 8개
    ├── frameTop.xfdl         # 헤더
    ├── frameLogin.xfdl       # 로그인 오버레이
    ├── frameLeft.xfdl        # 좌측 메뉴 (leftFrame)
    ├── frameMDI.xfdl         # MDI 탭 바
    ├── frameMain.xfdl        # 메인 콘텐츠
    ├── frameBottom.xfdl      # 푸터
    ├── frameWork.xfdl        # MDI 워크페이지
    └── frameWorkTitle.xfdl   # MDI 탭 제목
```

→ 프레임 트리 상세 비교 및 선택 기준 → `references/xadl-frame-patterns.md`

## Step 1 — 파라미터 수집

사용자에게 아래 항목을 **순서대로** 묻습니다. 기본값이 있는 항목은 엔터로 기본값 사용.

| # | 질문 | 기본값 | 설명 |
|---|---|---|---|
| 1 | 프로젝트 이름 (`PROJECT_NAME`) | `MyNexacroApp` | `.xprj` / `.xadl` 파일명 + 폼 titletext 에 사용. 공백/한글 금지 권장 |
| 2 | 애플리케이션 ID (`APPLICATION_ID`) | `PROJECT_NAME` 과 동일 | `<Application id="...">` 의 속성값 |
| 3 | 생성 대상 디렉터리 | (현재 경로) | 기존 파일이 있으면 덮어쓰기 여부 재확인 |
| 4 | 업무 모듈 prefix (`FORM_PREFIX`) | `Sample` | `Base` 외 추가할 서비스 prefix. 동일 이름 디렉터리도 함께 생성 |
| 5 | 테마 ID (`THEME_ID`) | `default` | `theme::<THEME_ID>` 형태로 environment.xml 에 박힘. `_resource_/_theme_/<THEME_ID>/` 이 있어야 런타임 동작 |
| 6 | 프레임 스타일 (`FRAME_STYLE`) | `minimal` | `minimal` / `packageN` 택1. `packageN` 은 MDI·프레임셋 풀레이아웃 (로그인 + 좌측메뉴 + MDI 탭 + 헤더/푸터). 선택 기준 → `references/xadl-frame-patterns.md` |

## Step 2 — 스켈레톤 치환

선택한 `FRAME_STYLE` 에 따라 스켈레톤 소스가 달라집니다.

| FRAME_STYLE | 스켈레톤 경로 |
|---|---|
| `minimal` | `{SKILL_BASE_PATH}/assets/skeleton/` |
| `packageN` | `{SKILL_BASE_PATH}/assets/skeleton/` (공통 파일) + `{SKILL_BASE_PATH}/assets/skeleton-frames/packageN/` (덮어쓰기) |

### 공통 플레이스홀더

| 플레이스홀더 | 치환값 |
|---|---|
| `{{PROJECT_NAME}}` | Step 1-①, 파일명은 파일 자체의 이름도 재명명 |
| `{{APPLICATION_ID}}` | Step 1-② |
| `{{FORM_PREFIX}}` | Step 1-④ |
| `{{THEME_ID}}` | Step 1-⑤ |
| `{{PROJECT_TITLE}}` | Step 1-① (`PROJECT_NAME` 을 그대로 titletext 로 사용) |

⚠️ 파일명 자체가 `{{PROJECT_NAME}}.xprj` / `{{PROJECT_NAME}}.xadl` 이므로 **복사 후 이름 변경** 필수.

### 치환 순서 — `minimal`

1. 디렉터리 생성
   ```
   mkdir -p <target>/Base <target>/<FORM_PREFIX> \
            <target>/_resource_/_theme_ <target>/_resource_/_images_ <target>/_resource_/_xcss_
   ```
2. `assets/skeleton/` 의 모든 파일을 `<target>/` 로 복사하면서 플레이스홀더 치환:
   - `{{PROJECT_NAME}}.xprj` → `<PROJECT_NAME>.xprj`
   - `{{PROJECT_NAME}}.xadl` → `<PROJECT_NAME>.xadl`
   - `typedefinition.xml` (치환만)
   - `environment.xml` (치환만)
   - `appvariables.xml` (치환 없음)
   - `bootstrap.xml` (치환 없음)
   - `Base/main.xfdl` (치환)

### 치환 순서 — `packageN`

1. 디렉터리 생성
   ```
   mkdir -p <target>/Base <target>/<FORM_PREFIX> <target>/frame \
            <target>/_resource_/_theme_ <target>/_resource_/_images_ <target>/_resource_/_xcss_ <target>/_resource_/_font_
   ```
2. **1단계 — 공통 파일** — `assets/skeleton/` 에서 아래 파일만 복사 + 치환:
   - `{{PROJECT_NAME}}.xprj` → `<PROJECT_NAME>.xprj`
   - `environment.xml`
   - `bootstrap.xml`
   - `Base/main.xfdl` (packageN 에서는 보조 기동 확인용)
3. **2단계 — packageN 덮어쓰기/추가** — `assets/skeleton-frames/packageN/` 에서 복사 + 치환:
   - `{{PROJECT_NAME}}.xadl` → `<PROJECT_NAME>.xadl` (VFrameSet/HFrameSet MDI 레이아웃)
   - `typedefinition.xml` (`frame::` 서비스 prefix 포함, `{{FORM_PREFIX}}` 치환)
   - `appvariables.xml` (치환 없음, 공식 packageN 샘플 그대로)
   - `frame/frameTop.xfdl` ~ `frame/frameWorkTitle.xfdl` (8 파일, 치환 없음)

## Step 3 — 검증

생성 직후 아래 체크를 출력합니다 (파일 수와 서비스 목록은 `FRAME_STYLE` 에 따라 달라짐).

**minimal 스타일**

```
✅ 프로젝트 생성 완료 — <target-dir>
─────────────────────────────────
프레임 스타일 : minimal
파일 수       : 7
엔트리        : <PROJECT_NAME>.xprj
기동 폼       : Base/main.xfdl
서비스        : Base, <FORM_PREFIX>, theme, imagerc, xcssrc, font
테마          : theme::<THEME_ID>  (⚠️ _resource_/_theme_/<THEME_ID>/ 디렉터리 미배치 상태 — 실행 전 테마 자산 필요)
─────────────────────────────────
다음 단계:
  1. Nexacro Studio 에서 <PROJECT_NAME>.xprj 열기
  2. 테마 자산 (_resource_/_theme_/<THEME_ID>/) 복사 또는 Studio 에서 import
  3. 폼 추가는 `nexacro-form-maker` skill 사용
```

**packageN 스타일**

```
✅ 프로젝트 생성 완료 — <target-dir>
─────────────────────────────────
프레임 스타일 : packageN (MDI / VFrameSet + HFrameSet)
파일 수       : 15  (공통 6 + frame/*.xfdl 8 + packageN.xadl 1)
엔트리        : <PROJECT_NAME>.xprj
메인 xadl     : <PROJECT_NAME>.xadl  (MainFrame → VFrameSet[44,0,*,0] → HFrameSet[240,*] → VFrameSet1[32,*,0])
프레임 폼     : frame/frameTop.xfdl, frameLogin.xfdl, frameLeft.xfdl, frameMDI.xfdl,
               frameMain.xfdl, frameBottom.xfdl, frameWork.xfdl, frameWorkTitle.xfdl
서비스        : Base, <FORM_PREFIX>, frame, theme, imagerc, xcssrc, font, extPrototype, lib, svcurl
테마          : theme::<THEME_ID>  (⚠️ _resource_/_theme_/<THEME_ID>/ 디렉터리 미배치 상태)
추가 필요     : nexacrolib/ (extPrototype / ListView / traceLog 모듈), _resource_/_font_/
─────────────────────────────────
다음 단계:
  1. Nexacro Studio 에서 <PROJECT_NAME>.xprj 열기
  2. 공식 샘플에서 _resource_/ + nexacrolib/ 복사 (→ Step 4 안내 참조)
  3. frame/frameLogin.xfdl / frameLeft.xfdl 의 메뉴 Dataset 을 서비스와 연동
  4. 업무 폼은 `nexacro-form-maker` skill 로 `<FORM_PREFIX>/` 아래에 추가
```

## Step 4 — 안 하는 것 (의도적 제외)

| 제외 항목 | 이유 |
|---|---|
| `_resource_/_theme_/<THEME_ID>/` 실제 테마 파일 | 라이선스 · 용량 문제. Nexacro SDK 설치본 또는 [공식 공개 샘플 저장소](https://github.com/TOBESOFT-DOCS/sample_Nexacro_N_V24) 의 `_resource_/` 디렉터리를 복사해서 사용 |
| `_resource_/_images_` / `_resource_/_xcss_` / `_resource_/_font_` / `_resource_/_stringrc_` | 위와 동일. 공개 샘플 저장소의 동일 경로에서 필요한 자산만 선택 복사 |
| `NexacroN_client_license.xml` | 고객사별 라이선스 파일. 배치는 사용자 책임 |
| `nexacrolib/` 프레임워크 JS | v24 flat 레이아웃은 SDK 가 런타임에 주입 |
| `*.xfont` 사용자 폰트 | 프로젝트별 결정 |
| `macros.xml` | 초기엔 불필요. 매크로 추가 시 `nexacro-form-maker` 참조 |
| 다국어 Screen (`Screen_ja` / `Screen_zh`) | 단일 desktop 로케일만 셋업. 다국어는 environment.xml 수동 추가 |

### 공식 공개 샘플 프로젝트 (테마/리소스 소스)

- **GitHub**: https://github.com/TOBESOFT-DOCS/sample_Nexacro_N_V24
- 위 저장소의 `_resource_/_theme_/`, `_resource_/_images_/`, `_resource_/_xcss_/`, `_resource_/_font_/` 를 그대로 가져와 본 스캐폴드의 동일 경로에 배치하면 Studio 실행이 바로 가능.
- 테마 ID 를 기본값 `default` 외 다른 값 (`blue`, `blue_ja`, `blue_zh` 등) 으로 바꾼 경우엔 해당 테마 폴더만 선택 복사.

## 자주 묻는 레퍼런스

- `.xprj` 엘리먼트 레퍼런스 → `references/xprj-spec.md`
- `.xadl` Application/MainFrame/ChildFrame → `references/xadl-spec.md`
- `typedefinition.xml` Modules/Components/Services → `references/typedefinition-spec.md`
- 서비스 prefix 규칙 (`Base::`, `imagerc::`, `theme::`, `frame::` 등) → `references/service-prefixes.md`
- xadl 프레임 스타일 (minimal vs packageN) 비교 → `references/xadl-frame-patterns.md`

## 확장 가이드 (스캐폴드 이후)

| 하고 싶은 것 | 참조 |
|---|---|
| 폼 파일 추가 | `nexacro-form-maker` skill |
| xfdl → xjs 빌드/배포 | `nexacro-build` skill |
| 서버 통신 포맷 (XML/SSV/JSON) | `nexacro-data-format` skill |
| Spring WebFlux 백엔드 포팅 | `nexacro-webflux-port` plugin |

## 외부 공식 참고자료

| 자료 | URL |
|---|---|
| 공개 샘플 프로젝트 (테마/리소스 소스) | https://github.com/TOBESOFT-DOCS/sample_Nexacro_N_V24 |
| Nexacro N v24 온라인 도움말 | https://docs.tobesoft.com/nexacro_n_v24_ko |
| 컴포넌트 활용 워크북 (Developer Guide) | https://docs.tobesoft.com/developer_guide_nexacro_n_v24_ko |
