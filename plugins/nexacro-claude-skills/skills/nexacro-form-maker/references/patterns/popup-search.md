# 복잡 화면 패턴: Popup 검색

## 언제 이 패턴을 사용하는가

입력 필드에서 **참조 데이터를 검색하여 선택**할 때:
- 사원 코드 입력 옆 돋보기 버튼 → 사원 검색 팝업 → 선택 → 코드/이름 자동 입력
- 거래처 조회, 품목 조회, 부서 조회 등 코드성 Lookup

---

## 구조 개요

```
[부모 폼]                           [팝업 폼]
  Edit: empId [________] [🔍]  →→   조회 조건 + Grid
  Edit: empNm [________]            [선택] 버튼 클릭
                          ←←    fnReceivePopupData(data) 호출
  empId, empNm 자동 입력
```

**두 개의 독립된 XFDL 파일:**
1. **부모 폼** — 입력 필드 + 팝업 열기 버튼
2. **팝업 폼** — 검색 UI + Grid + 선택/닫기 버튼 (`cmm/popupSearch{Target}.xfdl`)

---

## 부모 폼 — 관련 부분 (스니펫)

### Layout (팝업 버튼 포함 입력 영역)

```xml
<!-- 부모 폼의 divForm 안 -->
<Static text="사원" left="10" top="40" width="60" height="25"/>
<Edit id="edtEmpId" left="75" top="40" width="120" height="25" readonly="true"/>
<Edit id="edtEmpNm" left="200" top="40" width="150" height="25" readonly="true"/>
<Button id="btnSearchEmp" text="🔍" left="355" top="40" width="30" height="25"
        onclick="fnOpenPopupEmp" cssclass="btn_WF_Search"/>
```

### Script (부모 폼)

```javascript
// ─── 팝업 열기 ──────────────────────────────────────────────────────────────
this.fnOpenPopupEmp = function() {
    // 팝업에 초기 조건 전달 (선택)
    var oArgs = {
        searchEmpNm: this.edtEmpNm.value   // 현재 입력값을 초기 조건으로
    };
    this.gfnOpenPopup(
        this,                              // opener (this 폼)
        "popupSearchEmp",                  // 팝업 인스턴스 ID
        "cmm/popupSearchEmp.xfdl",         // 팝업 XFDL 경로
        800,                               // width
        500,                               // height
        oArgs,                             // args (팝업에 전달할 초기값)
        "fnReceivePopupData",              // 팝업이 데이터 반환 시 호출될 콜백
        "modal"                            // 모달 팝업
    );
};

// ─── 팝업으로부터 데이터 수신 ────────────────────────────────────────────────
// 팝업 폼에서 this.opener.fnReceivePopupData(data) 호출 시 실행
this.fnReceivePopupData = function(oData) {
    if (nexacro._isNull(oData)) return;

    this.edtEmpId.set_value(oData.empId);
    this.edtEmpNm.set_value(oData.empNm);

    // Dataset에 세팅하는 경우 (Grid 행에 입력 시)
    // var nRow = this.dsList.rowposition;
    // this.dsList.setColumn(nRow, "empId", oData.empId);
    // this.dsList.setColumn(nRow, "empNm", oData.empNm);
};
```

---

## 팝업 폼 — 완성 XFDL (`cmm/popupSearchEmp.xfdl`)

```xml
<?xml version="1.0" encoding="utf-8"?>
<FDL version="2.1">
  <Form id="popupSearchEmp" classname="Popup" titletext="사원 검색"
        left="0" top="0" width="800" height="500" onload="form_onload">
    <Layouts>
      <Layout>

        <!-- ① 조회 조건 -->
        <Div id="divSearch" left="0" top="0" right="0" height="44">
          <Layouts><Layout>
            <Static text="사원명" left="5" top="10" width="60" height="25"
                    cssclass="sta_WF_SubTitle"/>
            <Edit id="edtSearchEmpNm" left="70" top="10" width="150" height="25"
                  onkeyup="edtSearchEmpNm_onkeyup"/>
            <Button id="btnSearch" text="조회" left="230" top="10" width="65" height="25"
                    onclick="fnSearch" borderRadius="5px"/>
          </Layout></Layouts>
        </Div>

        <!-- ② 결과 Grid -->
        <Grid id="grdResult" left="0" top="44" right="0" bottom="44"
              binddataset="dsResult" autofittype="col"
              ondblclick="grdResult_ondblclick">
          <Formats>
            <Format id="default">
              <Columns>
                <Column size="100"/>
                <Column size="200"/>
                <Column size="150"/>
                <Column size="150"/>
              </Columns>
              <Rows>
                <Row size="25" band="head"/>
                <Row size="30"/>
              </Rows>
              <Band id="head">
                <Cell text="사원ID"/>
                <Cell col="1" text="사원명"/>
                <Cell col="2" text="부서명"/>
                <Cell col="3" text="직책"/>
              </Band>
              <Band id="body">
                <Cell text="bind:empId"/>
                <Cell col="1" text="bind:empNm"/>
                <Cell col="2" text="bind:deptNm"/>
                <Cell col="3" text="bind:empPos"/>
              </Band>
            </Format>
          </Formats>
        </Grid>

        <!-- ③ 하단 버튼 -->
        <Div id="divBottom" left="0" right="0" bottom="0" height="44">
          <Layouts><Layout>
            <Button id="btnSelect" text="선택" right="72" top="10" width="65" height="25"
                    onclick="fnSelect" borderRadius="5px"/>
            <Button id="btnClose"  text="닫기" right="2"  top="10" width="65" height="25"
                    onclick="fnClose"  borderRadius="5px"/>
          </Layout></Layouts>
        </Div>

      </Layout>
    </Layouts>

    <Objects>
      <Dataset id="dsSearch">
        <ColumnInfo>
          <Column id="searchEmpNm" type="STRING" size="50"/>
        </ColumnInfo>
        <Rows><Row><Col id="searchEmpNm"/></Row></Rows>
      </Dataset>

      <Dataset id="dsResult">
        <ColumnInfo>
          <Column id="empId"  type="STRING" size="20"/>
          <Column id="empNm"  type="STRING" size="50"/>
          <Column id="deptNm" type="STRING" size="100"/>
          <Column id="empPos" type="STRING" size="50"/>
        </ColumnInfo>
      </Dataset>
    </Objects>

    <Bind>
      <BindItem id="bi_searchEmpNm" compid="divSearch.form.edtSearchEmpNm"
                propid="value" datasetid="dsSearch" columnid="searchEmpNm"/>
    </Bind>

    <Script type="xscript5.1"><![CDATA[

// ─── 팝업 초기화 ────────────────────────────────────────────────────────────
this.form_onload = function(obj:nexacro.Form, e:nexacro.LoadEventInfo) {
    this.gfnFormOnLoad(this);

    // 부모 폼이 전달한 초기 조건 수신
    var oArgs = this.parent.popupArguments;   // 프레임워크별 args 접근 방식
    if (!nexacro._isNull(oArgs) && !nexacro._isNull(oArgs["searchEmpNm"])) {
        this.dsSearch.setColumn(0, "searchEmpNm", oArgs["searchEmpNm"]);
    }

    this.fnSearch();   // 팝업 진입 즉시 조회
};

// ─── Callback ───────────────────────────────────────────────────────────────
this.fnCallback = function(svcID, errorCode, errorMsg) {
    if (errorCode != 0) return;
    // searchResult 완료 후 특별 처리 없음
};

// ─── 조회 ───────────────────────────────────────────────────────────────────
this.fnSearch = function() {
    this.gfnTransaction(
        "searchResult",
        "selectEmpSearchList.do",
        "dsSearch=dsSearch",
        "dsResult=output1",
        "", "fnCallback", true
    );
};

// ─── Enter 키 조회 ───────────────────────────────────────────────────────────
this.edtSearchEmpNm_onkeyup = function(obj:nexacro.Edit, e:nexacro.KeyEventInfo) {
    if (e.keycode == 13) {   // Enter
        this.fnSearch();
    }
};

// ─── Grid 더블클릭 → 즉시 선택 ─────────────────────────────────────────────
this.grdResult_ondblclick = function(obj:nexacro.Grid, e:nexacro.GridClickEventInfo) {
    this.fnSelect();
};

// ─── 선택 버튼 → 부모 폼에 데이터 전달 ────────────────────────────────────
this.fnSelect = function() {
    var nRow = this.dsResult.rowposition;
    if (nRow < 0 || this.dsResult.rowcount == 0) {
        this.gfnAlert("선택된 항목이 없습니다.");
        return;
    }

    // 반환할 데이터 객체 구성
    var oData = {
        empId : this.dsResult.getColumn(nRow, "empId"),
        empNm : this.dsResult.getColumn(nRow, "empNm"),
        deptNm: this.dsResult.getColumn(nRow, "deptNm"),
        empPos: this.dsResult.getColumn(nRow, "empPos")
    };

    // 부모 폼 콜백 호출
    this.opener.fnReceivePopupData(oData);

    // 팝업 닫기
    this.close();
};

// ─── 닫기 버튼 ──────────────────────────────────────────────────────────────
this.fnClose = function() {
    this.close();
};

    ]]></Script>
  </Form>
</FDL>
```

---

## 데이터 흐름 다이어그램

```
[부모 폼]                                    [팝업 폼]
btnSearchEmp.onclick
    └→ fnOpenPopupEmp()
            └→ gfnOpenPopup(this, ..., oArgs, "fnReceivePopupData")
                                                  └→ form_onload(oArgs)
                                                          └→ fnSearch()
                                                                  └→ Grid 표출

                                         사용자 더블클릭 / [선택] 클릭
                                                  └→ fnSelect()
                                                          └→ oData = {empId, empNm, ...}
                                                          └→ this.opener.fnReceivePopupData(oData)
    fnReceivePopupData(oData) ←←←←←←←←←←←←←←←←←←←←←←←
        └→ edtEmpId.set_value(oData.empId)
        └→ edtEmpNm.set_value(oData.empNm)
                                                          └→ this.close()
```

---

## gfnTransaction 규칙 (팝업 폼 내부)

| 상황 | inData | outData |
|------|--------|---------|
| 팝업 내 조회 | `"dsSearch=dsSearch"` | `"dsResult=output1"` |

팝업 폼은 **조회 전용**이 원칙. 저장 로직은 부모 폼에서 처리.

---

## 파일 위치 규칙

```
packageN/
├── cmm/                         ← 공통 팝업 폼 위치
│   ├── popupSearchEmp.xfdl      ← 사원 검색
│   ├── popupSearchDept.xfdl     ← 부서 검색
│   └── popupSearchCode.xfdl     ← 공통 코드 검색
└── service/
    └── empMgmt.xfdl             ← 부모 폼
```

팝업 URL 경로: `"cmm/popupSearch{Target}.xfdl"` 형식.

---

## gfnOpenPopup 파라미터 정리

```javascript
this.gfnOpenPopup(
    this,                          // ① opener: 부모 폼 참조 (항상 this)
    "popupSearchEmp",              // ② 팝업 인스턴스 고유 ID (중복 방지)
    "cmm/popupSearchEmp.xfdl",     // ③ 팝업 XFDL 상대 경로
    800,                           // ④ 팝업 width (px)
    500,                           // ⑤ 팝업 height (px)
    oArgs,                         // ⑥ 전달 args 객체 (없으면 null)
    "fnReceivePopupData",          // ⑦ 데이터 반환 시 호출될 부모 함수명
    "modal"                        // ⑧ "modal" | "modeless" (기본: modal)
);
```

---

## Grid 행에 팝업 결과 입력 (변형)

Grid Cell에서 팝업을 열고 해당 행에 값을 채우는 경우:

```javascript
// 부모 폼: 팝업 열 때 현재 Grid rowposition 저장
this.fnOpenPopupEmp = function() {
    this._nTargetRow = this.dsList.rowposition;  // 대상 행 저장
    this.gfnOpenPopup(this, "popupSearchEmp", "cmm/popupSearchEmp.xfdl",
                      800, 500, null, "fnReceivePopupData", "modal");
};

// 부모 폼: 수신 시 저장된 행에 세팅
this.fnReceivePopupData = function(oData) {
    if (nexacro._isNull(oData)) return;
    this.dsList.setColumn(this._nTargetRow, "empId", oData.empId);
    this.dsList.setColumn(this._nTargetRow, "empNm", oData.empNm);
};
```

---

## 생성 검증 체크리스트

**부모 폼:**
- [ ] 팝업 버튼 `onclick` → `fnOpenPopupEmp` 연결
- [ ] `fnReceivePopupData(oData)` 함수 선언, null 체크 포함
- [ ] `gfnOpenPopup` 7~8번째 인자 (callback 함수명, modal 타입) 누락 없음

**팝업 폼:**
- [ ] `form_onload`에서 `popupArguments` 수신 및 null 체크
- [ ] Grid에 `ondblclick="grdResult_ondblclick"` 선언 (더블클릭 선택 지원)
- [ ] `fnSelect()`에서 `rowcount == 0` 및 `rowposition < 0` 체크
- [ ] 반환 데이터 오브젝트의 키 이름이 부모 폼 `fnReceivePopupData`와 일치
- [ ] `this.opener.fnReceivePopupData(oData)` 호출 후 반드시 `this.close()`
- [ ] 팝업 파일 경로가 `cmm/` 디렉터리 하위인지 확인
