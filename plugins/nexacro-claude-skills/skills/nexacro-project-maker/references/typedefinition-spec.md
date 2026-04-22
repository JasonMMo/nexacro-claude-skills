# `typedefinition.xml` — Modules / Components / Services

프로젝트 런타임이 **어떤 컴포넌트 라이브러리를 로드** 하고 **어떤 prefix 가 어떤 경로로 매핑** 되는지 선언합니다.

## 3가지 최상위 섹션

```xml
<TypeDefinition version="3.0">
  <Modules>    <!-- 번들 JSON 매니페스트: 어떤 nexacro SDK 모듈을 로드? -->
  <Components> <!-- 실제 사용하는 컴포넌트 클래스 매핑 -->
  <Services>   <!-- prefix::path/file.xfdl 해석 테이블 -->
</TypeDefinition>
```

## `<Modules>` — SDK 모듈 번들

```xml
<Modules>
  <Module url="CompBase.json"/>      <!-- 필수. Form/Button/Edit 기본 컴포넌트 -->
  <Module url="ComComp.json"/>       <!-- 공용 확장 컴포넌트 -->
  <Module url="Grid.json"/>          <!-- Grid 별도 번들 (용량 큼) -->
  <Module url="DeviceAPI.json"/>     <!-- 카메라/GPS/로컬스토리지 -->
  <Module url="ListView.json"/>      <!-- 모바일식 ListView -->
  <Module url="Graphics.json"/>      <!-- 그래픽 프리미티브 -->
  <Module url="MobileComp.json"/>    <!-- 모바일 전용 컴포넌트 -->
</Modules>
```

- 필요 없는 모듈은 제거해도 동작 (전송 용량 감소). `CompBase.json` 은 삭제 금지.
- 각 `.json` 은 SDK 설치본의 `nexacrolib/` 에 존재하며 배포 시 함께 딸려감.

## `<Components>` — 사용 컴포넌트 선언

```xml
<Component type="JavaScript" id="Button" classname="nexacro.Button"/>
<Component type="JavaScript" id="Grid"   classname="nexacro.Grid"/>
<Component type="JavaScript" id="Dataset" classname="nexacro.NormalDataset"/>
```

- `id` = xfdl 안에서 쓰는 엘리먼트명 (`<Button>`, `<Grid>`, `<Dataset>`).
- `classname` = 런타임 JS 클래스명.
- **xfdl 에서 쓰기 전에 이 섹션에 등록 필수**. 누락 시 "component not defined" 런타임 에러.

### 자주 쓰는 매핑 (v24 샘플 기준 13종)

| id | classname | 용도 |
|---|---|---|
| `Button` | `nexacro.Button` | 버튼 |
| `Edit` | `nexacro.Edit` | 단일행 입력 |
| `MaskEdit` | `nexacro.MaskEdit` | 마스크 입력 |
| `TextArea` | `nexacro.TextArea` | 멀티라인 입력 |
| `Combo` | `nexacro.Combo` | 드롭다운 |
| `Radio` | `nexacro.Radio` | 라디오 그룹 |
| `CheckBox` | `nexacro.CheckBox` | 체크박스 |
| `Calendar` | `nexacro.Calendar` | 달력 (인라인) |
| `DateField` | `nexacro.DateField` | 날짜 입력 + 드롭다운 |
| `Static` | `nexacro.Static` | 텍스트 라벨 |
| `Div` | `nexacro.Div` | 컨테이너 (내부 레이아웃) |
| `Grid` | `nexacro.Grid` | 데이터 그리드 |
| `Dataset` | `nexacro.NormalDataset` | 비가시 Dataset (데이터 바인딩 소스) |

→ 엘리먼트별 속성/이벤트는 `nexacro-xfdl-author` skill 의 `references/components/*.md` 참조

## `<Services>` — URL prefix 매핑

→ 별도 문서: `service-prefixes.md`

## `<Protocols>` / `<Update>` / `<Deploy>`

| 섹션 | 필수? | 용도 |
|---|---|---|
| `<Protocols>` | 선택 | 커스텀 통신 프로토콜 등록 (일반 HTTP 는 불필요) |
| `<Update>` | 선택 | 런타임 자동 업데이트 URL + OS 별 테마/엔진 버전 |
| `<Deploy>` | 선택 | 빌드 대상 OS 목록 |

스캐폴드에서는 최소 `<Os name="Windows"/>` 만 박아두고 실제 배포 시 필요에 따라 확장.
