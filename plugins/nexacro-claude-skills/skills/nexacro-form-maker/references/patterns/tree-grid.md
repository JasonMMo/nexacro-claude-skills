# 복잡 화면 패턴: Tree + Grid

## 언제 이 패턴을 사용하는가

좌측에 **계층적 카테고리/메뉴**를 두고 우측에 **선택된 항목의 데이터**를 Grid로 표출:
- 부서 트리 → 소속 직원 목록
- 메뉴 분류 → 해당 분류 코드 목록
- 조직도 → 해당 조직 권한 목록

---

## 레이아웃 구조 (ASCII)

```
┌─────────────────────────────────────────────────────────────┐
│ [조회]                                                       │  divSearch (h:40)
├──────────────────┬──────────────────────────────────────────┤
│ ■ 부서 분류      │ ■ 직원 목록                    [저장]    │
│ ┌──────────────┐ │ ┌────────┬──────────┬──────────────────┐ │
│ │▶ 본사        │ │ │직원ID  │직원명    │ 직책             │ │
│ │  └ 개발팀 ◄─┼─┼─│ E001   │ 홍길동   │ 팀장             │ │
│ │  └ 기획팀    │ │ │ E002   │ 김영희   │ 대리             │ │
│ │▶ 지사        │ │ └────────┴──────────┴──────────────────┘ │
│ └──────────────┘ │                          grdContent       │
│   grdCategory    │                                           │
│  (w:280, h:100%) │                    (left:280, right:0)    │
└──────────────────┴──────────────────────────────────────────┘
```

**두 가지 left Grid 구현 방식:**

| 방식 | 적합한 경우 | 특징 |
|------|-------------|------|
| **Flat Grid** | 단순 카테고리 목록 | 구현 단순, 코드 적음 |
| **계층 Grid** (levelindex) | 2~3단계 트리 구조 | `_level_` 컬럼으로 들여쓰기 표현 |

---

## Dataset 선언 규칙

| Dataset ID   | 역할                              |
|--------------|-----------------------------------|
| `dsCategory` | 좌측 카테고리/트리 목록           |
| `dsSearch`   | 우측 Grid 조회 조건 (선택된 FK)   |
| `dsContent`  | 우측 Grid 결과 목록               |

---

## 완성 XFDL 예제 — Flat Grid (단순 카테고리)

```xml
<?xml version="1.0" encoding="utf-8"?>
<FDL version="2.1">
  <Form id="DeptEmpTree" classname="Work" titletext="부서별 직원 조회"
        left="0" top="0" width="1050" height="768" onload="form_onload">
    <Layouts>
      <Layout>

        <!-- ① 조회 조건 -->
        <Div id="divSearch" left="0" top="0" right="0" height="40">
          <Layouts><Layout>
            <Button id="btnSearch" text="조회" left="5" top="8" width="65" height="25"
                    onclick="fnSearchCategory" borderRadius="5px"/>
          </Layout></Layouts>
        </Div>

        <!-- ② 좌측: 카테고리 Grid -->
        <Div id="divLeft" left="0" top="40" width="280" bottom="0">
          <Layouts><Layout>
            <Static id="staCategoryTitle" text="■ 부서 분류" left="5" top="5"
                    width="120" height="20"/>
            <Grid id="grdCategory" left="0" top="28" right="0" bottom="0"
                  binddataset="dsCategory" autofittype="col"
                  onrowposchanged="grdCategory_onrowposchanged">
              <Formats>
                <Format id="default">
                  <Columns>
                    <Column size="240"/>
                  </Columns>
                  <Rows>
                    <Row size="25" band="head"/>
                    <Row size="30"/>
                  </Rows>
                  <Band id="head">
                    <Cell text="부서명"/>
                  </Band>
                  <Band id="body">
                    <Cell text="bind:deptNm"/>
                  </Band>
                </Format>
              </Formats>
            </Grid>
          </Layout></Layouts>
        </Div>

        <!-- ③ 우측: Content Grid -->
        <Div id="divRight" left="282" top="40" right="0" bottom="0">
          <Layouts><Layout>
            <Static id="staContentTitle" text="■ 직원 목록" left="5" top="5"
                    width="120" height="20"/>
            <Button id="btnContentSave" text="저장" right="2" top="5" width="65" height="25"
                    onclick="fnContentSave" borderRadius="5px"/>
            <Grid id="grdContent" left="0" top="28" right="0" bottom="0"
                  binddataset="dsContent" autofittype="col">
              <Formats>
                <Format id="default">
                  <Columns>
                    <Column size="80"/>
                    <Column size="150"/>
                    <Column size="120"/>
                    <Column size="100"/>
                  </Columns>
                  <Rows>
                    <Row size="25" band="head"/>
                    <Row size="30"/>
                  </Rows>
                  <Band id="head">
                    <Cell text="직원ID"/>
                    <Cell col="1" text="직원명"/>
                    <Cell col="2" text="직책"/>
                    <Cell col="3" text="입사일"/>
                  </Band>
                  <Band id="body">
                    <Cell text="bind:empId"/>
                    <Cell col="1" text="bind:empNm"  edittype="normal"/>
                    <Cell col="2" text="bind:empPos" edittype="normal"/>
                    <Cell col="3" text="bind:hireDt"/>
                  </Band>
                </Format>
              </Formats>
            </Grid>
          </Layout></Layouts>
        </Div>

      </Layout>
    </Layouts>

    <Objects>
      <Dataset id="dsCategory">
        <ColumnInfo>
          <Column id="deptId"  type="STRING" size="20"/>
          <Column id="deptNm"  type="STRING" size="100"/>
        </ColumnInfo>
      </Dataset>

      <!-- 우측 조회 조건: 카테고리 선택값(FK) 보관 -->
      <Dataset id="dsSearch">
        <ColumnInfo>
          <Column id="deptId" type="STRING" size="20"/>
        </ColumnInfo>
        <Rows><Row><Col id="deptId"/></Row></Rows>
      </Dataset>

      <Dataset id="dsContent">
        <ColumnInfo>
          <Column id="empId"  type="STRING" size="20"/>
          <Column id="deptId" type="STRING" size="20"/>
          <Column id="empNm"  type="STRING" size="50"/>
          <Column id="empPos" type="STRING" size="50"/>
          <Column id="hireDt" type="STRING" size="8"/>
        </ColumnInfo>
      </Dataset>
    </Objects>

    <Script type="xscript5.1"><![CDATA[

// ─── Form 초기화 ────────────────────────────────────────────────────────────
this.form_onload = function(obj:nexacro.Form, e:nexacro.LoadEventInfo) {
    this.gfnFormOnLoad(this);
    this.fnSearchCategory();         // 좌측 카테고리 먼저 로드
};

// ─── Callback ───────────────────────────────────────────────────────────────
this.fnCallback = function(svcID, errorCode, errorMsg) {
    if (errorCode != 0) return;

    switch(svcID) {
        case "searchCategory":
            // 카테고리 로드 완료 → 첫 행 자동 선택 → onrowposchanged 발생
            if (this.dsCategory.rowcount > 0) {
                this.dsCategory.set_rowposition(0);
            }
            break;
        case "searchContent":
            break;
        case "saveContent":
            this.gfnAlert("msg.save.success");
            this.fnSearchContent();
            break;
    }
};

// ─── 좌측: 카테고리 목록 조회 ───────────────────────────────────────────────
this.fnSearchCategory = function() {
    this.dsContent.clearData();
    this.gfnTransaction(
        "searchCategory",
        "selectDeptCategoryList.do",
        "",                          // 조건 없이 전체 카테고리 로드
        "dsCategory=output1",
        "", "fnCallback", true
    );
};

// ─── 우측: 선택된 카테고리의 Content 조회 ──────────────────────────────────
this.fnSearchContent = function() {
    var sSelectedId = this.dsCategory.getColumn(this.dsCategory.rowposition, "deptId");
    if (nexacro._isNull(sSelectedId) || sSelectedId == "") return;

    this.dsSearch.setColumn(0, "deptId", sSelectedId);

    this.gfnTransaction(
        "searchContent",
        "selectEmpListByDept.do",
        "dsSearch=dsSearch",         // 선택된 카테고리 ID 전달
        "dsContent=output1",
        "", "fnCallback", true
    );
};

// ─── 좌측 Grid 행 이동 → Content 재조회 ────────────────────────────────────
this.grdCategory_onrowposchanged = function(obj:nexacro.Grid, e:nexacro.RowposChangedEventInfo) {
    this.fnSearchContent();
};

// ─── 우측 Content 저장 ──────────────────────────────────────────────────────
this.fnContentSave = function() {
    if (!this.gfnDsIsUpdated(this.dsContent)) {
        this.gfnAlert("msg.save.nochange");
        return;
    }
    this.gfnTransaction(
        "saveContent",
        "saveEmpList.do",
        "input1=dsContent:A",
        "", "", "fnCallback"
    );
};

    ]]></Script>
  </Form>
</FDL>
```

---

## 계층 Grid 변형 (levelindex — 2단계 트리)

좌측 Grid에 부모-자식 계층이 필요한 경우 `_level_` 컬럼 + levelindex 활용:

```xml
<!-- Dataset: _level_ 컬럼 추가 -->
<Dataset id="dsCategory">
  <ColumnInfo>
    <Column id="nodeId"   type="STRING" size="20"/>
    <Column id="parentId" type="STRING" size="20"/>
    <Column id="nodeNm"   type="STRING" size="100"/>
    <Column id="_level_"  type="INT"    size="4"/>   <!-- 0=루트, 1=1단계, 2=2단계 -->
  </ColumnInfo>
</Dataset>
```

```xml
<!-- Grid: levelindex 적용으로 들여쓰기 자동 표현 -->
<Grid id="grdCategory" binddataset="dsCategory" ...>
  <Formats>
    <Format id="default">
      <Columns><Column size="240"/></Columns>
      <Rows>
        <Row size="25" band="head"/>
        <Row size="30"/>
      </Rows>
      <Band id="head"><Cell text="분류"/></Band>
      <Band id="body">
        <Cell text="bind:nodeNm" levelindex="0"
              levelstep="20"/>   <!-- levelstep: 들여쓰기 픽셀 -->
      </Band>
    </Format>
  </Formats>
</Grid>
```

> `levelstep="20"`: `_level_` 값 × 20px 들여쓰기. 루트(0)=0px, 1단계=20px, 2단계=40px.

---

## 레이아웃 분할 비율

| 화면 너비 | divLeft width | divRight left |
|-----------|---------------|---------------|
| 1050px    | 280           | 282           |
| 1280px    | 320           | 322           |
| 1600px    | 380           | 382           |

> `divRight.left = divLeft.width + 2` (2px 구분선 여백)

---

## gfnTransaction 규칙

| 단계 | inData | outData | 비고 |
|------|--------|---------|------|
| 카테고리 로드 | `""` (없음) | `"dsCategory=output1"` | 전체 카테고리 |
| Content 조회 | `"dsSearch=dsSearch"` | `"dsContent=output1"` | 선택된 FK 전달 |
| Content 저장 | `"input1=dsContent:A"` | `""` | 변경분 저장 |

---

## DB 스키마 → XFDL 변환 룰

| 조건 | 좌측 구성 |
|------|-----------|
| 코드 마스터 테이블 (2~3단계) | 계층 Grid (levelindex) |
| 단순 분류 테이블 (flat) | Flat Grid |
| FK 참조 컬럼이 코드성 | 좌측 코드 Grid, 우측 FK 연관 데이터 Grid |

---

## 생성 검증 체크리스트

- [ ] `divLeft.width`와 `divRight.left` 값이 일치(+2) 하는지 확인
- [ ] `grdCategory`에 `onrowposchanged="grdCategory_onrowposchanged"` 선언
- [ ] `fnCallback("searchCategory")`에서 `dsCategory.set_rowposition(0)` 호출 → 첫 항목 자동 조회
- [ ] `fnSearchContent()`에서 선택값 null 체크 후 `dsSearch.setColumn` 호출
- [ ] 계층 Grid 사용 시 Dataset에 `_level_` 컬럼 선언, Grid Cell에 `levelindex` 속성 추가
- [ ] 카테고리 재조회(`fnSearchCategory`) 시 `dsContent.clearData()` 먼저 호출
