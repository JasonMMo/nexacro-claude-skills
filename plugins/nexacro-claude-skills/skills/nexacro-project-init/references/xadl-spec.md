# `.xadl` Application / MainFrame / ChildFrame

애플리케이션 런타임의 **프레임 레이아웃** 과 기동 폼을 정의합니다.

## 전체 샘플 (단일 데스크톱 스크린)

```xml
<?xml version="1.0" encoding="utf-8"?>
<ADL version="2.0">
  <Application id="MyApp" screenid="Screen_D" licenseurl="NexacroN_client_license.xml">
    <Layout>
      <MainFrame id="mainframe" showtitlebar="true" showstatusbar="false"
                 width="1280" height="720" resizable="true" showtitleicon="false">
        <ChildFrame id="ChildFrame00" formurl="Base::main.xfdl"
                    showcascadetitletext="false" showtitlebar="false" showtitleicon="false"/>
      </MainFrame>
    </Layout>
    <Style url="xcssrc::app_common.xcss"/>
  </Application>
</ADL>
```

## 다국어 / 다해상도 샘플

```xml
<Application id="MyApp" screenid="Screen_D,Screen_ja,Screen_zh" licenseurl="NexacroN_client_license.xml">
```

- `screenid` 는 **콤마 구분 목록**. 런타임이 `environment.xml` 의 `<Screen>` 정의와 매칭해 자동 선택.
- 런타임 URL 파라미터 `?screenid=Screen_ja` 로 강제 지정 가능.

## 엘리먼트

| 엘리먼트 | 설명 |
|---|---|
| `<ADL>` | 루트. `version="2.0"` |
| `<Application>` | 앱 한 개 선언 |
| `<Layout>` | MainFrame 컨테이너 |
| `<MainFrame>` | 최상위 프레임. 창 제목바 / 사이즈 / 리사이즈 제어 |
| `<ChildFrame>` | MainFrame 내부의 기동 폼 로더. `formurl` 속성이 실제 진입 xfdl |
| `<Style>` | 글로벌 `.xcss` 스타일시트 (복수 선언 가능) |

## `<Application>` 핵심 속성

| 속성 | 설명 |
|---|---|
| `id` | Application 식별자 |
| `screenid` | 활성 스크린 ID (콤마 구분) |
| `licenseurl` | Nexacro N 클라이언트 라이선스 XML 경로 |

## `<MainFrame>` 핵심 속성

| 속성 | 기본 | 설명 |
|---|---|---|
| `id` | `mainframe` | 고정 관례. 런타임에서 `nexacro.getApplication().mainframe` 으로 접근 |
| `showtitlebar` | `true` | 창 제목바 표시 |
| `showstatusbar` | `false` | 하단 상태바 |
| `width` / `height` | 1280 / 720 | 초기 창 크기 |
| `resizable` | `true` | 창 리사이즈 허용 |

## `<ChildFrame>` — 기동 폼

| 속성 | 설명 |
|---|---|
| `id` | ChildFrame 식별자. 동적 생성 시 충돌 방지 위해 보통 `ChildFrame00` |
| `formurl` | 기동 시 로드할 xfdl. **서비스 prefix 사용 필수** (예: `Base::main.xfdl`) |
| `showtitlebar` | ChildFrame 자체 제목바 (MainFrame 과 별개) |

## 서비스 prefix 주의

`formurl="Base::main.xfdl"` 은 **상대경로가 아님**. `typedefinition.xml` 의 `<Service prefixid="Base" url="./Base/">` 매핑을 거친 후 해석됩니다.

→ 자세한 매핑 규칙은 `service-prefixes.md` 참조
