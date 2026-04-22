---
name: nexacro-xfdl-author
description: Nexacro N v24 xfdl 폼 작성 헬퍼. Form 골격 + 13종 코어 컴포넌트 블록 + Dataset/BindItem 바인딩 패턴을 레퍼런스로 제공합니다. 사용 트리거 — "xfdl 만들어", "nexacro 폼 작성", "Grid 블록 만들어줘", "Dataset 바인딩", "nexacro component", "xfdl form authoring"
---

# Nexacro XFDL Author

Nexacro N v24 `.xfdl` (Form 정의 XML) 파일을 **블록 조립 방식** 으로 작성합니다.

- Form 골격(skeleton) 1개 + 컴포넌트 블록 13종을 조합.
- 컴포넌트별 레퍼런스는 `references/components/<name>.md` 에 개별 분리.
- 데이터 바인딩 패턴 (Dataset + BindItem) 은 `references/binding-patterns.md` 에 통합.

## Step 1 — 폼 스켈레톤

모든 xfdl 은 아래 형태에서 출발:

```xml
<?xml version="1.0" encoding="utf-8"?>
<FDL version="2.1">
  <Form id="<FORM_ID>" width="<W>" height="<H>" titletext="<TITLE>">
    <Layouts>
      <Layout width="<W>" height="<H>">
        <!-- 여기에 컴포넌트 블록 삽입 -->
      </Layout>
    </Layouts>
    <Objects>
      <!-- 비가시 객체 (Dataset 등) -->
    </Objects>
    <Script type="xscript5.1"><![CDATA[
      // 이벤트 핸들러 스크립트
    ]]></Script>
  </Form>
</FDL>
```

복사 베이스: `{SKILL_BASE_PATH}/assets/form-skeleton.xfdl`

→ 구조 상세 + `<Layouts>` 다중 해상도 패턴 → `references/form-structure.md`

## Step 2 — 컴포넌트 블록 13종

`<Layout>` 안에 배치하는 **UI 컴포넌트** 들. 각 파일은 최소 구성 + 이벤트 + 바인딩 변형을 포함합니다.

### 입력

| 컴포넌트 | 레퍼런스 | 주요 속성 |
|---|---|---|
| Button | `references/components/button.md` | `text`, `onclick` |
| Edit | `references/components/edit.md` | `value`, `onkeyup`, `onchange` — 바인딩 가능 |
| MaskEdit | `references/components/maskedit.md` | `mask`, `type` |
| TextArea | `references/components/textarea.md` | `value`, `wordwrap` |
| Combo | `references/components/combo.md` | `codecolumn`, `datacolumn`, `innerdataset` |

### 선택 / 날짜

| 컴포넌트 | 레퍼런스 | 주요 속성 |
|---|---|---|
| Radio | `references/components/radio.md` | `innerdataset`, `codecolumn`, `onitemchanged` |
| CheckBox | `references/components/checkbox.md` | `truevalue`, `falsevalue` |
| Calendar | `references/components/calendar.md` | `value` (YYYYMMDD), `dateformat` |
| DateField | `references/components/datefield.md` | `value`, `inputtype`, `dropdowntype` |
| Static | `references/components/static.md` | `text`, `expr` |

### 레이아웃 / 복합

| 컴포넌트 | 레퍼런스 | 주요 속성 |
|---|---|---|
| Div | `references/components/div.md` | 컨테이너 (`<Layouts>` 내부 재귀) 또는 서브폼 (`url`) |
| Grid | `references/components/grid.md` | `binddataset`, `<Format>`/`<Columns>`/`<Rows>`/`<Band>`/`<Cell>` |
| Dataset | `references/components/dataset.md` | `<ColumnInfo>` + `<Rows>` — `<Objects>` 하위 비가시 객체 |

## Step 3 — 데이터 바인딩

Dataset + Edit/Combo/Grid 바인딩은 전용 문서로 통합:

→ `references/binding-patterns.md`

## Step 4 — 스크립트 블록

`<Script type="xscript5.1"><![CDATA[ ... ]]></Script>` 영역의 관례:

- 핸들러 함수명 규칙: `this.<컴포넌트id>_<이벤트명> = function(obj, e) { ... };`
- Form 생명주기: `this.Form_onload = function(obj, e){ ... };`
- Dataset 이벤트: `this.dsCustomer_oncolumnchanged = function(obj, e){ ... };`
- `this.alert(...)`, `this.getOwnerFrame()`, `this.parent.xxx` 등 Form 컨텍스트.

→ 복잡한 스크립트 예시는 각 컴포넌트 `.md` 의 "이벤트" 섹션 참고.

## Step 5 — 실행 체크리스트

새 xfdl 을 프로젝트에 투입할 때:

1. 파일 저장 위치가 `typedefinition.xml` 의 서비스 prefix 디렉터리 안인지 확인
   - 예: `Sample::customer.xfdl` 쓰려면 파일은 `./Sample/customer.xfdl`
2. 사용한 컴포넌트가 `typedefinition.xml` 의 `<Components>` 에 등록되어 있는지 확인
3. 실행 파일 빌드: `nexacro-build` skill 사용
4. 런타임 통신 포맷 결정 시: `nexacro-data-format` skill 참조

## 관련 skill

| 하고 싶은 것 | 참조 |
|---|---|
| 빈 프로젝트 스캐폴드 | `nexacro-project-init` |
| xfdl → xjs 빌드 / 배포 | `nexacro-build` |
| 서버 통신 XML / SSV / JSON | `nexacro-data-format` |
| Spring WebFlux 백엔드 포팅 | `nexacro-webflux-port` (별도 플러그인) |
