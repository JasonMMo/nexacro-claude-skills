# 복잡 화면 패턴: Multi-Dataset 저장 (헤더+라인)

## 언제 이 패턴을 사용하는가

**1:N 입력 전표 구조** — 헤더 정보(1행) + 라인 명세(N행)를 한 화면에서 함께 입력/저장:
- 발주서: 발주 헤더(일자, 거래처) + 발주 라인(품목, 수량, 단가)
- 계약서: 계약 헤더(계약명, 기간) + 계약 항목 명세
- 영수증: 영수증 헤더(일자, 결제자) + 결제 항목

---

## 레이아웃 구조 (ASCII)

```
┌─────────────────────────────────────────────────────────────┐
│ [발주서 조회/입력]                          [신규] [저장]    │  divHeader (h:120)
│ 발주번호: [__________]  발주일자: [________]                 │
│ 거래처:   [________] [🔍]                                   │
├─────────────────────────────────────────────────────────────┤
│ ■ 발주 라인                          [라인추가] [라인삭제]  │  divLine
│ ┌──────┬──────────┬──────────┬──────┬──────┬─────────────┐ │
│ │No    │ 품목ID   │ 품목명   │ 수량 │ 단가 │ 금액        │ │
│ ├──────┼──────────┼──────────┼──────┼──────┼─────────────┤ │
│ │  1   │ IT-001   │ 노트북   │  2   │500000│  1,000,000  │ │
│ │  2   │ IT-002   │ 마우스   │ 10   │ 15000│    150,000  │ │
│ └──────┴──────────┴──────────┴──────┴──────┴─────────────┘ │
└─────────────────────────────────────────────────────────────┘

dsHeader (BindItem) ────── 1행  ──────── Header 필드 자동 동기화
dsLine   (binddataset) ─── N행  ──────── Grid 자동 동기화
```

---

## Dataset 선언 규칙

| Dataset ID   | 역할                           | 행 수    |
|--------------|--------------------------------|----------|
| `dsSearch`   | 헤더 조회 조건                  | 1행 고정 |
| `dsHeader`   | 헤더 데이터 (PK 포함)           | 1행      |
| `dsLine`     | 라인 데이터 (FK = 헤더 PK)     | N행      |

`dsHeader` 바인딩: BindItem으로 각 Edit/Combo 필드와 1:1 연결  
`dsLine` 바인딩: `binddataset="dsLine"` Grid와 연결

---

## 완성 XFDL 예제

```xml
<?xml version="1.0" encoding="utf-8"?>
<FDL version="2.1">
  <Form id="OrderForm" classname="Work" titletext="발주서 입력"
        left="0" top="0" width="1050" height="768" onload="form_onload">
    <Layouts>
      <Layout>

        <!-- ① 헤더 영역 (BindItem 기반 Form) -->
        <Div id="divHeader" left="0" top="0" right="0" height="130">
          <Layouts><Layout>

            <!-- 조회 조건 행 -->
            <Static text="발주번호" left="5"   top="8"  width="70" height="25"
                    cssclass="sta_WF_SubTitle"/>
            <Edit id="edtSearchOrderId" left="80" top="8" width="120" height="25"/>
            <Button id="btnSearch" text="조회" left="210" top="8" width="65" height="25"
                    onclick="fnSearch" borderRadius="5px"/>
            <Button id="btnNew"    text="신규" right="70" top="8" width="65" height="25"
                    onclick="fnNew"    borderRadius="5px"/>
            <Button id="btnSave"   text="저장" right="2"  top="8" width="65" height="25"
                    onclick="fnSave"   borderRadius="5px"/>

            <!-- 헤더 입력 행 1 -->
            <Static text="발주번호" left="5"   top="42" width="70" height="25"
                    cssclass="sta_WF_SubTitle"/>
            <Edit id="edtOrderId"  left="80"  top="42" width="120" height="25" readonly="true"/>
            <Static text="발주일자" left="215" top="42" width="70" height="25"
                    cssclass="sta_WF_SubTitle"/>
            <Edit id="edtOrderDt"  left="290" top="42" width="100" height="25"/>

            <!-- 헤더 입력 행 2 -->
            <Static text="거래처"   left="5"   top="76" width="70" height="25"
                    cssclass="sta_WF_SubTitle"/>
            <Edit id="edtSupplierId" left="80"  top="76" width="100" height="25" readonly="true"/>
            <Edit id="edtSupplierNm" left="185" top="76" width="150" height="25" readonly="true"/>
            <Button id="btnSearchSupplier" text="🔍" left="340" top="76" width="30" height="25"
                    onclick="fnOpenPopupSupplier"/>
            <Static text="합계금액" left="385" top="76" width="70" height="25"
                    cssclass="sta_WF_SubTitle"/>
            <Edit id="edtTotalAmt" left="460" top="76" width="120" height="25" readonly="true"/>

          </Layout></Layouts>
        </Div>

        <!-- ② 라인 영역 (Grid) -->
        <Div id="divLine" left="0" top="132" right="0" bottom="0">
          <Layouts><Layout>
            <Static text="■ 발주 라인" left="5" top="5" width="120" height="20"/>
            <Button id="btnLineAdd" text="라인추가" right="72" top="5" width="70" height="25"
                    onclick="fnLineAdd" borderRadius="5px"/>
            <Button id="btnLineDel" text="라인삭제" right="2"  top="5" width="70" height="25"
                    onclick="fnLineDel" borderRadius="5px"/>
            <Grid id="grdLine" left="0" top="32" right="0" bottom="0"
                  binddataset="dsLine" autofittype="col">
              <Formats>
                <Format id="default">
                  <Columns>
                    <Column size="40"/>
                    <Column size="100"/>
                    <Column size="200"/>
                    <Column size="80"/>
                    <Column size="100"/>
                    <Column size="120"/>
                  </Columns>
                  <Rows>
                    <Row size="25" band="head"/>
                    <Row size="30"/>
                  </Rows>
                  <Band id="head">
                    <Cell text="No"/>
                    <Cell col="1" text="품목ID"/>
                    <Cell col="2" text="품목명"/>
                    <Cell col="3" text="수량"/>
                    <Cell col="4" text="단가"/>
                    <Cell col="5" text="금액"/>
                  </Band>
                  <Band id="body">
                    <Cell text="expr:currow+1"/>
                    <Cell col="1" text="bind:itemId"    edittype="normal"/>
                    <Cell col="2" text="bind:itemNm"    edittype="normal"/>
                    <Cell col="3" text="bind:qty"       edittype="normal"/>
                    <Cell col="4" text="bind:unitPrice" edittype="normal"/>
                    <Cell col="5" text="bind:amt"       mask="###,###,###,##0"/>
                  </Band>
                </Format>
              </Formats>
            </Grid>
          </Layout></Layouts>
        </Div>

      </Layout>
    </Layouts>

    <Objects>
      <!-- 헤더 조회 조건 -->
      <Dataset id="dsSearch">
        <ColumnInfo>
          <Column id="searchOrderId" type="STRING" size="20"/>
        </ColumnInfo>
        <Rows><Row><Col id="searchOrderId"/></Row></Rows>
      </Dataset>

      <!-- 헤더 Dataset (1행) -->
      <Dataset id="dsHeader">
        <ColumnInfo>
          <Column id="orderId"     type="STRING" size="20"/>
          <Column id="orderDt"     type="STRING" size="8"/>
          <Column id="supplierId"  type="STRING" size="20"/>
          <Column id="supplierNm"  type="STRING" size="100"/>
          <Column id="totalAmt"    type="INT"    size="4"/>
        </ColumnInfo>
      </Dataset>

      <!-- 라인 Dataset (N행) -->
      <Dataset id="dsLine">
        <ColumnInfo>
          <Column id="lineNo"     type="INT"    size="4"/>
          <Column id="orderId"    type="STRING" size="20"/>  <!-- FK -->
          <Column id="itemId"     type="STRING" size="20"/>
          <Column id="itemNm"     type="STRING" size="100"/>
          <Column id="qty"        type="INT"    size="4"/>
          <Column id="unitPrice"  type="INT"    size="4"/>
          <Column id="amt"        type="INT"    size="4"/>
        </ColumnInfo>
      </Dataset>
    </Objects>

    <Bind>
      <!-- 헤더 필드 ↔ dsHeader BindItem -->
      <BindItem id="bi_orderId"    compid="divHeader.form.edtOrderId"    propid="value"
                datasetid="dsHeader" columnid="orderId"/>
      <BindItem id="bi_orderDt"    compid="divHeader.form.edtOrderDt"    propid="value"
                datasetid="dsHeader" columnid="orderDt"/>
      <BindItem id="bi_supplierId" compid="divHeader.form.edtSupplierId" propid="value"
                datasetid="dsHeader" columnid="supplierId"/>
      <BindItem id="bi_supplierNm" compid="divHeader.form.edtSupplierNm" propid="value"
                datasetid="dsHeader" columnid="supplierNm"/>
      <BindItem id="bi_totalAmt"   compid="divHeader.form.edtTotalAmt"   propid="value"
                datasetid="dsHeader" columnid="totalAmt"/>
      <!-- 조회 조건 -->
      <BindItem id="bi_searchOrderId" compid="divHeader.form.edtSearchOrderId" propid="value"
                datasetid="dsSearch" columnid="searchOrderId"/>
    </Bind>

    <Script type="xscript5.1"><![CDATA[

// ─── Form 초기화 ────────────────────────────────────────────────────────────
this.form_onload = function(obj:nexacro.Form, e:nexacro.LoadEventInfo) {
    this.gfnFormOnLoad(this);
    this.fnNew();   // 화면 진입 시 신규 모드로 시작
};

// ─── Callback ───────────────────────────────────────────────────────────────
this.fnCallback = function(svcID, errorCode, errorMsg) {
    if (errorCode != 0) return;

    switch(svcID) {
        case "search":
            // 헤더 1행 + 라인 N행 로드 완료
            if (this.dsHeader.rowcount > 0) {
                this.dsHeader.set_rowposition(0);
            }
            break;
        case "save":
            this.gfnAlert("msg.save.success");
            // 저장 후 재조회 (서버가 생성한 orderId, amt 반영)
            this.dsSearch.setColumn(0, "searchOrderId",
                                    this.dsHeader.getColumn(0, "orderId"));
            this.fnSearch();
            break;
    }
};

// ─── 조회 ───────────────────────────────────────────────────────────────────
this.fnSearch = function() {
    this.gfnTransaction(
        "search",
        "selectOrderForm.do",           // 헤더 + 라인 동시 조회 endpoint
        "dsSearch=dsSearch",
        "dsHeader=output1 dsLine=output2",  // 두 Dataset 동시 수신
        "", "fnCallback", true
    );
};

// ─── 신규 ───────────────────────────────────────────────────────────────────
this.fnNew = function() {
    this.dsHeader.clearData();
    this.dsLine.clearData();
    var nRow = this.dsHeader.addRow();
    this.dsHeader.setColumn(nRow, "orderDt",
        nexacro.getApplication().gfnGetToday());  // 오늘 날짜 기본값
};

// ─── 라인 추가 ──────────────────────────────────────────────────────────────
this.fnLineAdd = function() {
    var nRow = this.dsLine.addRow();
    // FK 자동 세팅: 헤더 orderId를 라인에 주입
    var sOrderId = this.dsHeader.getColumn(0, "orderId");
    this.dsLine.setColumn(nRow, "orderId", sOrderId);
    this.dsLine.setColumn(nRow, "lineNo", this.dsLine.rowcount);  // 순번
};

// ─── 라인 삭제 ──────────────────────────────────────────────────────────────
this.fnLineDel = function() {
    if (this.dsLine.rowcount == 0) return;
    this.dsLine.deleteRow(this.dsLine.rowposition);
    this.fnCalcTotal();   // 삭제 후 합계 재계산
};

// ─── 합계 계산 (라인 amt 합산 → 헤더 totalAmt) ─────────────────────────────
this.fnCalcTotal = function() {
    var nTotal = 0;
    for (var i = 0; i < this.dsLine.rowcount; i++) {
        var nQty   = nexacro._toNumber(this.dsLine.getColumn(i, "qty"),       0);
        var nPrice = nexacro._toNumber(this.dsLine.getColumn(i, "unitPrice"), 0);
        var nAmt   = nQty * nPrice;
        this.dsLine.setColumn(i, "amt", nAmt);
        nTotal += nAmt;
    }
    this.dsHeader.setColumn(0, "totalAmt", nTotal);
};

// ─── 수량/단가 변경 시 금액 재계산 ─────────────────────────────────────────
this.dsLine_oncolumnchanged = function(obj:nexacro.Dataset, e:nexacro.DSColChangeEventInfo) {
    if (e.columnid == "qty" || e.columnid == "unitPrice") {
        this.fnCalcTotal();
    }
};

// ─── 저장 (헤더 + 라인 동시) ────────────────────────────────────────────────
this.fnSave = function() {
    // 헤더 필수값 검증
    if (nexacro._isNull(this.dsHeader.getColumn(0, "supplierId")) ||
        this.dsHeader.getColumn(0, "supplierId") == "") {
        this.gfnAlert("거래처를 선택해 주세요.");
        return;
    }
    if (this.dsLine.rowcount == 0) {
        this.gfnAlert("발주 라인을 1건 이상 입력해 주세요.");
        return;
    }

    this.gfnTransaction(
        "save",
        "saveOrderForm.do",
        "input1=dsHeader:A input2=dsLine:A",   // 헤더 + 라인 동시 전송
        "",
        "", "fnCallback"
    );
};

// ─── 거래처 팝업 (popup-search.md 패턴 적용) ────────────────────────────────
this.fnOpenPopupSupplier = function() {
    this.gfnOpenPopup(this, "popupSearchSupplier",
                      "cmm/popupSearchSupplier.xfdl", 800, 500,
                      null, "fnReceiveSupplier", "modal");
};

this.fnReceiveSupplier = function(oData) {
    if (nexacro._isNull(oData)) return;
    this.dsHeader.setColumn(0, "supplierId", oData.supplierId);
    this.dsHeader.setColumn(0, "supplierNm", oData.supplierNm);
};

    ]]></Script>
  </Form>
</FDL>
```

---

## gfnTransaction inData / outData 규칙

| 동작 | inData | outData |
|------|--------|---------|
| 헤더+라인 조회 | `"dsSearch=dsSearch"` | `"dsHeader=output1 dsLine=output2"` |
| 헤더+라인 저장 | `"input1=dsHeader:A input2=dsLine:A"` | `""` |
| 헤더만 저장 | `"input1=dsHeader:A"` | `""` |
| 라인만 저장 | `"input1=dsLine:A"` | `""` |

> 공백으로 구분하여 복수 Dataset 전송/수신 가능.  
> outData `output1`, `output2` 순서는 백엔드 응답 Dataset 순서와 일치해야 함.

---

## 이벤트 흐름

```
form_onload → fnNew()
    └→ dsHeader.addRow()  (1행 생성)
    └→ dsLine 초기화

사용자 입력:
    └→ BindItem 자동 동기화: Edit 값 변경 → dsHeader 자동 갱신
    └→ fnLineAdd() → dsLine.addRow() + FK(orderId) 자동 세팅
    └→ qty/unitPrice 변경 → dsLine_oncolumnchanged → fnCalcTotal()
    └→ dsHeader.totalAmt 자동 갱신 → edtTotalAmt BindItem으로 표출

fnSave() →
    └→ 헤더 필수값 검증
    └→ 라인 건수 검증 (0건 방지)
    └→ gfnTransaction("save", ..., "input1=dsHeader:A input2=dsLine:A", ...)
    └→ fnCallback("save") → fnSearch() 재조회
```

---

## DB 스키마 → XFDL 변환 룰

| 조건 | 구성 방식 |
|------|-----------|
| 테이블 A(PK) ← 테이블 B(FK) + B가 주 입력 단위 | A = 헤더, B = 라인 |
| B의 컬럼 수가 5개 이하 | Grid 편집 (라인 직접 편집) |
| B의 컬럼 수가 6개 이상 | 라인 선택 → 하단 상세 Form (Master-Detail 조합) |
| A의 PK가 자동생성(시퀀스) | 신규 저장 후 server-side orderId 반환 → 재조회 필수 |

헤더 필드 구성 기준:
- 날짜 컬럼 → `Edit` (YYYYMMDD 형식) 또는 `DatePicker`
- 코드성 FK 컬럼 → `Edit(readonly) + 팝업 버튼` (popup-search.md 패턴 조합)
- 금액/합계 컬럼 → `Edit(readonly)` + 라인 `oncolumnchanged` 계산

---

## 생성 검증 체크리스트

- [ ] `dsHeader` BindItem이 모든 헤더 Edit/Combo와 1:1 연결되어 있는지 확인
- [ ] `dsLine`에 FK 컬럼(`orderId`) 선언 및 `fnLineAdd()`에서 자동 세팅 확인
- [ ] 저장 inData: `"input1=dsHeader:A input2=dsLine:A"` (공백 구분)
- [ ] 조회 outData: `"dsHeader=output1 dsLine=output2"` (공백 구분)
- [ ] `fnSave()`에서 헤더 필수값 검증 + 라인 건수 검증 포함
- [ ] `dsLine_oncolumnchanged`에서 수량/단가 변경 시 금액 재계산 연결
- [ ] 저장 callback에서 `fnSearch()` 재조회 (서버 생성 PK 반영)
- [ ] Grid Body Cell No: `expr:currow+1` (자동 순번)
