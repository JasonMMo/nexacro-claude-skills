---
name: nexacro-form-maker
description: Nexacro N v24 Form (.xfdl) 작성 헬퍼. Form 골격 + 43종 컴포넌트 블록 + Dataset/BindItem 바인딩 패턴을 레퍼런스로 제공합니다. 사용 트리거 — "nexacro 폼 만들어", "xfdl 만들어", "nexacro form maker", "Grid 블록 만들어줘", "Dataset 바인딩", "nexacro component", "xfdl form authoring"
---

# Nexacro Form Maker

Nexacro N v24 `.xfdl` (Form 정의 XML) 파일을 **블록 조립 방식** 으로 작성합니다.

- Form 골격(skeleton) 1개 + 컴포넌트 블록 **43종** (코어 13 + 확장 30).
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

## Step 2 — 컴포넌트 블록 카탈로그 (43종)

`<Layout>` 안에 배치하는 **UI 컴포넌트** 들. 각 파일은 최소 구성 + 이벤트 + 바인딩 변형을 포함합니다.

### 코어 13종 (v1 — 가장 자주 쓰임)

#### 기본 입력

| 컴포넌트 | 레퍼런스 | 주요 속성 |
|---|---|---|
| Button | `references/components/button.md` | `text`, `onclick` |
| Edit | `references/components/edit.md` | `value`, `onkeyup`, `onchange` — 바인딩 가능 |
| MaskEdit | `references/components/maskedit.md` | `mask`, `type` |
| TextArea | `references/components/textarea.md` | `value`, `wordwrap` |
| Combo | `references/components/combo.md` | `codecolumn`, `datacolumn`, `innerdataset` |

#### 선택 / 날짜

| 컴포넌트 | 레퍼런스 | 주요 속성 |
|---|---|---|
| Radio | `references/components/radio.md` | `innerdataset`, `codecolumn`, `onitemchanged` |
| CheckBox | `references/components/checkbox.md` | `truevalue`, `falsevalue` |
| Calendar | `references/components/calendar.md` | `value` (YYYYMMDD), `dateformat` |
| DateField | `references/components/datefield.md` | `value`, `inputtype`, `dropdowntype` |
| Static | `references/components/static.md` | `text`, `expr` |

#### 레이아웃 / 복합

| 컴포넌트 | 레퍼런스 | 주요 속성 |
|---|---|---|
| Div | `references/components/div.md` | 컨테이너 (`<Layouts>` 내부 재귀) 또는 서브폼 (`url`) |
| Grid | `references/components/grid.md` | `binddataset`, `<Format>`/`<Columns>`/`<Rows>`/`<Band>`/`<Cell>` |
| Dataset | `references/components/dataset.md` | `<ColumnInfo>` + `<Rows>` — `<Objects>` 하위 비가시 객체 |

### 확장 30종 (v2 — 사용 빈도 중간~낮음)

#### 모던 입력 + 선택 확장

| 컴포넌트 | 레퍼런스 | 용도 |
|---|---|---|
| TextField | `references/components/textfield.md` | 모던 스타일 단일행 입력 (Edit 대체) |
| MultiLineTextField | `references/components/multilinetextfield.md` | 모던 스타일 멀티라인 (TextArea 대체) |
| Spin | `references/components/spin.md` | 숫자 스피너 |
| ListBox | `references/components/listbox.md` | 펼친 리스트 (Combo 대체) |
| CheckBoxSet | `references/components/checkboxset.md` | Dataset 기반 다중 체크박스 |
| MultiCombo | `references/components/multicombo.md` | 다중 선택 가능한 Combo |

#### 날짜 확장 + 내비게이션

| 컴포넌트 | 레퍼런스 | 용도 |
|---|---|---|
| DateRangePicker | `references/components/daterangepicker.md` | 시작~끝 날짜 범위 |
| PopupDateRangePicker | `references/components/popupdaterangepicker.md` | 범위 선택 드롭다운 버전 |
| Tab | `references/components/tab.md` | 탭 컨테이너 (`<Tabpage>` 자식 트리) |
| GroupBox | `references/components/groupbox.md` | 제목 있는 그룹 컨테이너 |
| Menu | `references/components/menu.md` | 수평 메뉴바 (`<Menuitem>` 트리) |
| PopupMenu | `references/components/popupmenu.md` | 우클릭 컨텍스트 메뉴 |
| PopupDiv | `references/components/popupdiv.md` | 띄워놓는 Div (`trackpopup` API) |
| Panel | `references/components/panel.md` | 경량 컨테이너 (Div 대안) |

#### 디스플레이 + 파일 I/O

| 컴포넌트 | 레퍼런스 | 용도 |
|---|---|---|
| ImageViewer | `references/components/imageviewer.md` | 이미지 표시 (`imagerc::`) |
| ProgressBar | `references/components/progressbar.md` | 진행률 바 |
| ListView | `references/components/listview.md` | 모바일식 리스트 (템플릿 기반) |
| VirtualFile | `references/components/virtualfile.md` | 메모리 파일 핸들 |
| FileDialog | `references/components/filedialog.md` | OS 파일 선택 대화상자 |
| FileDownload | `references/components/filedownload.md` | UI 포함 다운로드 |
| FileUpload | `references/components/fileupload.md` | UI 포함 업로드 |
| FileDownTransfer | `references/components/filedowntransfer.md` | 비UI 다운로드 (URL 기반) |
| FileUpTransfer | `references/components/fileuptransfer.md` | 비UI 업로드 (URL 기반) |

#### 미디어 / 플러그인 / 데이터

| 컴포넌트 | 레퍼런스 | 용도 |
|---|---|---|
| Plugin | `references/components/plugin.md` | 외부 플러그인 로더 (레거시) |
| WebBrowser | `references/components/webbrowser.md` | 임베디드 웹 브라우저 |
| Sketch | `references/components/sketch.md` | 캔버스 드로잉 |
| GoogleMap | `references/components/googlemap.md` | 구글맵 임베디드 (API 키 필요) |
| VideoPlayer | `references/components/videoplayer.md` | 비디오 재생 |
| Graphics | `references/components/graphics.md` | SVG 유사 도형 |
| DataObject | `references/components/dataobject.md` | 바이너리 데이터 핸들 |

> ⚠️ **주의**: 확장 30종 중 일부(`Sketch`/`Graphics`/`Plugin` 등)는 공식 샘플이 없어 최소 엔트리 수준의 레퍼런스만 제공. 공식 문서([온라인 도움말](https://docs.tobesoft.com/nexacro_n_v24_ko) / [워크북](https://docs.tobesoft.com/developer_guide_nexacro_n_v24_ko))로 보강 필요.

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
| 빈 프로젝트 스캐폴드 | `nexacro-project-maker` |
| xfdl → xjs 빌드 / 배포 | `nexacro-build` |
| 서버 통신 XML / SSV / JSON | `nexacro-data-format` |
| Spring WebFlux 백엔드 포팅 | `nexacro-webflux-port` (별도 플러그인) |

## 외부 공식 참고자료

| 자료 | URL |
|---|---|
| 공개 샘플 프로젝트 (컴포넌트 실전 용례) | https://github.com/TOBESOFT-DOCS/sample_Nexacro_N_V24 |
| Nexacro N v24 온라인 도움말 | https://docs.tobesoft.com/nexacro_n_v24_ko |
| 컴포넌트 활용 워크북 (Developer Guide) | https://docs.tobesoft.com/developer_guide_nexacro_n_v24_ko |
