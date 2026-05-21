# 복잡 화면 패턴: Master-Detail

## 언제 이 패턴을 사용하는가

DB 스키마에서 **FK 관계**가 감지되면 Master-Detail 패턴을 적용한다:

```
DEPT (deptId PK) ← EMP (deptId FK)
→ DEPT = Master Grid (상단)
→ EMP  = Detail Grid (하단)
```

판별 규칙:
- **Master 테이블** = FK로 참조되는 테이블 (PK 보유)
- **Detail 테이블** = FK 컬럼을 보유한 테이블
- Detail 행이 여러 개 → **Grid 변형** (1:N)
- Detail 행이 항상 1개 → **Form 변형** (1:1, BindItem 기반)

---

## 레이아웃 구조 (ASCII)

```
┌─────────────────────────────────────────────────────────────┐
│ [조회조건]  부서명: [________]  [조회]                       │  divSearch (h:40)
├─────────────────────────────────────────────────────────────┤
│ ■ 부서 목록                          [추가] [삭제] [저장]    │  divMaster
│ ┌──────┬────────────┬────────────────────────────────────┐  │  (h:360)
│ │부서ID│ 부서명     │ 부서설명                            │  │
│ ├──────┼────────────┼────────────────────────────────────┤  │
│ │ 001  │ 개발팀     │ ...                                 │◄─┼── grdMaster
│ │ 002  │ 기획팀     │ ...                                 │  │   onrowposchanged
│ └──────┴────────────┴────────────────────────────────────┘  │   → fnSearchDetail()
├─────────────────────────────────────────────────────────────┤
│ ■ 직원 목록                          [추가] [삭제] [저장]    │  divDetail
│ ┌──────┬────────────┬────────────┬──────────────────────┐  │  (bottom:0)
│ │직원ID│ 직원명     │ 직책       │ 입사일               │  │
│ ├──────┼────────────┼────────────┼──────────────────────┤  │
│ │ E01  │ 홍길동     │ 팀장       │ 20200101             │◄─┼── grdDetail
│ └──────┴────────────┴────────────┴──────────────────────┘  │   binddataset="dsDetail"
└─────────────────────────────────────────────────────────────┘
```

---

## Dataset 선언 규칙

| Dataset ID      | 역할                         | 위치          |
|-----------------|------------------------------|---------------|
| `dsSearchMaster`| Master 조회 조건 (검색 키워드)| `<Objects>`   |
| `dsMaster`      | Master 결과 목록              | `<Objects>`   |
| `dsSearchDetail`| Detail 조회 조건 (Master FK) | `<Objects>`   |
| `dsDetail`      | Detail 결과 목록              | `<Objects>`   |

`dsSearchDetail` 필수 패턴:
```xml
<Dataset id="dsSearchDetail">
  <ColumnInfo>
    <Column id="deptId" type="STRING" size="20"/>  <!-- Master PK와 동일 타입 -->
  </ColumnInfo>
  <Rows><Row><Col id="deptId"/></Row></Rows>
</Dataset>
```

---

## 완성 XFDL 예제 — Grid 변형 (1:N)

```xml
<?xml version="1.0" encoding="utf-8"?>
<FDL version="2.1">
  <Form id="DeptEmpMgmt" classname="Work" titletext="부서/직원 관리"
        left="0" top="0" width="1050" height="768" onload="form_onload">
    <Layouts>
      <Layout>

        <!-- ① 조회 조건 영역 -->
        <Div id="divSearch" left="0" top="0" right="0" height="40">
          <Layouts><Layout>
            <Static id="staSearchDeptNm" text="부서명" left="5" top="8"
                    width="60" height="25" cssclass="sta_WF_SubTitle"/>
            <Edit id="edtSearchDeptNm" left="70" top="8" width="150" height="25"/>
            <Button id="btnSearch" text="조회" left="230" top="8" width="65" height="25"
                    onclick="fnSearchMaster" borderRadius="5px"/>
          </Layout></Layouts>
        </Div>

        <!-- ② Master 영역 (상단 50%) -->
        <Div id="divMaster" left="0" top="40" right="0" height="360">
          <Layouts><Layout>
            <Static id="staMasterTitle" text="■ 부서 목록" left="5" top="5"
                    width="120" height="20"/>
            <Button id="btnMasterAdd"  text="추가" right="140" top="5" width="65" height="25"
                    onclick="fnMasterAdd"  borderRadius="5px"/>
            <Button id="btnMasterDel"  text="삭제" right="70"  top="5" width="65" height="25"
                    onclick="fnMasterDel"  borderRadius="5px"/>
            <Button id="btnMasterSave" text="저장" right="2"   top="5" width="65" height="25"
                    onclick="fnMasterSave" borderRadius="5px"/>
            <Grid id="grdMaster" left="0" top="32" right="0" bottom="0"
                  binddataset="dsMaster" autofittype="col"
                  onrowposchanged="grdMaster_onrowposchanged">
              <Formats>
                <Format id="default">
                  <Columns>
                    <Column size="80"/>
                    <Column size="200"/>
                    <Column size="400"/>
                  </Columns>
                  <Rows>
                    <Row size="25" band="head"/>
                    <Row size="30"/>
                  </Rows>
                  <Band id="head">
                    <Cell text="부서ID"/>
                    <Cell col="1" text="부서명"/>
                    <Cell col="2" text="부서설명"/>
                  </Band>
                  <Band id="body">
                    <Cell text="bind:deptId"/>
                    <Cell col="1" text="bind:deptNm"   edittype="normal"/>
                    <Cell col="2" text="bind:deptDesc" edittype="normal"/>
                  </Band>
                </Format>
              </Formats>
            </Grid>
          </Layout></Layouts>
        </Div>

        <!-- ③ Detail 영역 (하단, 나머지 공간) -->
        <Div id="divDetail" left="0" top="400" right="0" bottom="0">
          <Layouts><Layout>
            <Static id="staDetailTitle" text="■ 직원 목록" left="5" top="5"
                    width="120" height="20"/>
            <Button id="btnDetailAdd"  text="추가" right="140" top="5" width="65" height="25"
                    onclick="fnDetailAdd"  borderRadius="5px"/>
            <Button id="btnDetailDel"  text="삭제" right="70"  top="5" width="65" height="25"
                    onclick="fnDetailDel"  borderRadius="5px"/>
            <Button id="btnDetailSave" text="저장" right="2"   top="5" width="65" height="25"
                    onclick="fnDetailSave" borderRadius="5px"/>
            <Grid id="grdDetail" left="0" top="32" right="0" bottom="0"
                  binddataset="dsDetail" autofittype="col">
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
      <!-- 조회 조건 -->
      <Dataset id="dsSearchMaster">
        <ColumnInfo>
          <Column id="searchDeptNm" type="STRING" size="100"/>
        </ColumnInfo>
        <Rows><Row><Col id="searchDeptNm"/></Row></Rows>
      </Dataset>

      <!-- Master 결과 -->
      <Dataset id="dsMaster">
        <ColumnInfo>
          <Column id="deptId"   type="STRING" size="20"/>
          <Column id="deptNm"   type="STRING" size="100"/>
          <Column id="deptDesc" type="STRING" size="200"/>
        </ColumnInfo>
      </Dataset>

      <!-- Detail 조회 조건 (Master FK 전달용) -->
      <Dataset id="dsSearchDetail">
        <ColumnInfo>
          <Column id="deptId" type="STRING" size="20"/>
        </ColumnInfo>
        <Rows><Row><Col id="deptId"/></Row></Rows>
      </Dataset>

      <!-- Detail 결과 -->
      <Dataset id="dsDetail">
        <ColumnInfo>
          <Column id="empId"  type="STRING" size="20"/>
          <Column id="deptId" type="STRING" size="20"/>
          <Column id="empNm"  type="STRING" size="50"/>
          <Column id="empPos" type="STRING" size="50"/>
          <Column id="hireDt" type="STRING" size="8"/>
        </ColumnInfo>
      </Dataset>
    </Objects>

    <Bind>
      <!-- 조회 조건 바인딩 -->
      <BindItem id="bi_searchDeptNm" compid="divSearch.form.edtSearchDeptNm"
                propid="value" datasetid="dsSearchMaster" columnid="searchDeptNm"/>
    </Bind>

    <Script type="xscript5.1"><![CDATA[

// ─── Form 초기화 ────────────────────────────────────────────────────────────
this.form_onload = function(obj:nexacro.Form, e:nexacro.LoadEventInfo) {
    this.gfnFormOnLoad(this);
    this.fnSearchMaster();           // 진입 시 Master 자동 조회
};

// ─── Callback ───────────────────────────────────────────────────────────────
this.fnCallback = function(svcID, errorCode, errorMsg) {
    if (errorCode != 0) return;

    switch(svcID) {
        case "searchMaster":
            // Master 조회 완료 → 첫 행 선택 → onrowposchanged → fnSearchDetail 자동 호출
            if (this.dsMaster.rowcount > 0) {
                this.dsMaster.set_rowposition(0);
            } else {
                this.dsDetail.clearData();
            }
            break;
        case "searchDetail":
            break;
        case "saveMaster":
            this.gfnAlert("msg.save.success");
            this.fnSearchMaster();
            break;
        case "saveDetail":
            this.gfnAlert("msg.save.success");
            this.fnSearchDetail();
            break;
    }
};

// ─── Master 조회 ────────────────────────────────────────────────────────────
this.fnSearchMaster = function() {
    this.dsDetail.clearData();       // Detail 초기화
    this.gfnTransaction(
        "searchMaster",              // svcID
        "selectDeptList.do",         // URL (.do 규칙)
        "dsSearchMaster=dsSearchMaster",  // inData: 조회조건 Dataset 전송
        "dsMaster=output1",          // outData: 결과 Dataset 수신
        "",                          // args
        "fnCallback",                // callback
        true                         // async
    );
};

// ─── Detail 조회 (Master PK → dsSearchDetail 세팅 후 호출) ─────────────────
this.fnSearchDetail = function() {
    var sMasterPk = this.dsMaster.getColumn(this.dsMaster.rowposition, "deptId");
    if (nexacro._isNull(sMasterPk) || sMasterPk == "") {
        this.dsDetail.clearData();
        return;
    }
    // FK 값을 dsSearchDetail에 세팅
    this.dsSearchDetail.setColumn(0, "deptId", sMasterPk);

    this.gfnTransaction(
        "searchDetail",
        "selectEmpList.do",
        "dsSearchDetail=dsSearchDetail",  // inData: FK 조건 전송
        "dsDetail=output1",               // outData: Detail 결과 수신
        "",
        "fnCallback",
        true
    );
};

// ─── Master Grid 행 이동 이벤트 → Detail 재조회 ─────────────────────────────
this.grdMaster_onrowposchanged = function(obj:nexacro.Grid, e:nexacro.RowposChangedEventInfo) {
    this.fnSearchDetail();
};

// ─── Master CRUD ────────────────────────────────────────────────────────────
this.fnMasterAdd = function() {
    this.dsMaster.addRow();
};

this.fnMasterDel = function() {
    if (this.dsMaster.rowcount == 0) return;
    this.dsMaster.deleteRow(this.dsMaster.rowposition);
};

this.fnMasterSave = function() {
    if (!this.gfnDsIsUpdated(this.dsMaster)) {
        this.gfnAlert("msg.save.nochange");
        return;
    }
    this.gfnTransaction(
        "saveMaster",
        "saveDeptList.do",
        "input1=dsMaster:A",   // :A = 변경된 행(Insert/Update/Delete) 모두 전송
        "",
        "",
        "fnCallback"
    );
};

// ─── Detail CRUD ────────────────────────────────────────────────────────────
this.fnDetailAdd = function() {
    var nRow = this.dsDetail.addRow();
    // FK 자동 세팅 (신규 행에 Master PK 주입)
    var sMasterPk = this.dsMaster.getColumn(this.dsMaster.rowposition, "deptId");
    this.dsDetail.setColumn(nRow, "deptId", sMasterPk);
};

this.fnDetailDel = function() {
    if (this.dsDetail.rowcount == 0) return;
    this.dsDetail.deleteRow(this.dsDetail.rowposition);
};

this.fnDetailSave = function() {
    if (!this.gfnDsIsUpdated(this.dsDetail)) {
        this.gfnAlert("msg.save.nochange");
        return;
    }
    this.gfnTransaction(
        "saveDetail",
        "saveEmpList.do",
        "input1=dsDetail:A",
        "",
        "",
        "fnCallback"
    );
};

    ]]></Script>
  </Form>
</FDL>
```

---

## gfnTransaction inData / outData 규칙 (Master-Detail 전용)

| 상황 | inData 형식 | outData 형식 |
|------|-------------|--------------|
| Master 조회 | `"dsSearchMaster=dsSearchMaster"` | `"dsMaster=output1"` |
| Detail 조회 (FK 전달) | `"dsSearchDetail=dsSearchDetail"` | `"dsDetail=output1"` |
| Master 저장 (변경분) | `"input1=dsMaster:A"` | `""` |
| Detail 저장 (변경분) | `"input1=dsDetail:A"` | `""` |
| Master+Detail 동시 저장 | `"input1=dsMaster:A input2=dsDetail:A"` | `""` |

`:A` 접미사 의미:
- `:A` = 추가/수정/삭제된 모든 행 전송 (저장 시 항상 사용)
- 없음 = 전체 행 전송 (조회 조건 Dataset은 접미사 없이)

---

## 이벤트 흐름 다이어그램

```
form_onload
    └→ fnSearchMaster()
            └→ gfnTransaction("searchMaster", ...)
                    └→ fnCallback("searchMaster")
                            └→ dsMaster.set_rowposition(0)
                                    └→ [onrowposchanged 발생]
                                            └→ grdMaster_onrowposchanged()
                                                    └→ fnSearchDetail()
                                                            └→ dsSearchDetail.setColumn(0, "deptId", masterPk)
                                                            └→ gfnTransaction("searchDetail", ...)
                                                                    └→ fnCallback("searchDetail")

사용자가 Master Grid 다른 행 클릭
    └→ [onrowposchanged 발생]
            └→ grdMaster_onrowposchanged()
                    └→ fnSearchDetail()  (위와 동일)
```

---

## DB 스키마 → XFDL 자동변환 룰

### 1. FK 관계 감지

```sql
-- 이런 FK 감지 시
ALTER TABLE EMP ADD CONSTRAINT FK_EMP_DEPT FOREIGN KEY (DEPT_ID) REFERENCES DEPT(DEPT_ID);
```

→ `DEPT` = Master, `EMP` = Detail

### 2. Dataset 컬럼 타입 매핑

| SQL 타입 | Dataset Column type |
|----------|---------------------|
| VARCHAR, CHAR | `STRING` |
| NUMBER, INT, BIGINT | `INT` 또는 `FLOAT` |
| DATE, DATETIME, TIMESTAMP | `STRING` size="8"~"17" |
| CLOB, TEXT | `STRING` size="4000"` |

### 3. Grid Body Cell 매핑

| 컬럼 특성 | edittype 설정 |
|-----------|---------------|
| PK 컬럼 | edittype 없음 (읽기 전용) |
| 일반 수정 가능 | `edittype="normal"` |
| FK 컬럼 (Detail) | edittype 없음 (자동 세팅) |
| 날짜 컬럼 | edittype="calendar" 또는 없음 |

### 4. URL 명명 규칙

| 동작 | URL 패턴 |
|------|----------|
| Master 조회 | `select{MasterTableCamel}List.do` |
| Detail 조회 | `select{DetailTableCamel}List.do` |
| Master 저장 | `save{MasterTableCamel}List.do` |
| Detail 저장 | `save{DetailTableCamel}List.do` |

예: `DEPT` → `selectDeptList.do`, `EMP` → `selectEmpList.do`

---

## Form 변형 (1:1 Detail)

Detail이 항상 1개 행인 경우 (1:1 관계), Grid 대신 BindItem + Edit/Combo 조합 사용.

```xml
<!-- divDetail 내부를 Grid 대신 개별 컴포넌트로 교체 -->
<Div id="divDetail" left="0" top="400" right="0" bottom="0">
  <Layouts><Layout>
    <Static id="staDetailTitle" text="■ 직원 상세" left="5" top="5" width="120" height="20"/>
    <Button id="btnDetailSave" text="저장" right="2" top="5" width="65" height="25"
            onclick="fnDetailSave" borderRadius="5px"/>
    <!-- 개별 필드 -->
    <Static text="직원명" left="10" top="40" width="80" height="25"/>
    <Edit id="edtEmpNm" left="95" top="40" width="200" height="25"/>
    <Static text="직책"  left="10" top="75" width="80" height="25"/>
    <Edit id="edtEmpPos" left="95" top="75" width="200" height="25"/>
  </Layout></Layouts>
</Div>
```

```xml
<!-- Bind 섹션에 BindItem 추가 -->
<Bind>
  <BindItem id="bi_empNm"  compid="divDetail.form.edtEmpNm"  propid="value"
            datasetid="dsDetail" columnid="empNm"/>
  <BindItem id="bi_empPos" compid="divDetail.form.edtEmpPos" propid="value"
            datasetid="dsDetail" columnid="empPos"/>
</Bind>
```

fnSearchDetail 콜백에서 `dsDetail.set_rowposition(0)` 호출하면 모든 BindItem 자동 갱신.

---

## 생성 검증 체크리스트

- [ ] `grdMaster`에 `onrowposchanged="grdMaster_onrowposchanged"` 선언 확인
- [ ] `dsSearchDetail`에 Master PK와 동일 이름/타입의 컬럼 선언 확인
- [ ] `fnCallback` switch에 `"searchMaster"`, `"searchDetail"`, `"saveMaster"`, `"saveDetail"` 4개 case 모두 포함
- [ ] `fnCallback("searchMaster")` 에서 `dsMaster.set_rowposition(0)` 호출 → Detail 자동 연쇄 조회
- [ ] `fnDetailAdd()`에서 FK 컬럼 자동 세팅 (`dsDetail.setColumn(nRow, "deptId", sMasterPk)`)
- [ ] 저장 inData에 `:A` 접미사 사용 (`"input1=dsMaster:A"`)
- [ ] Master 저장 callback에서 `fnSearchMaster()` 재호출 (화면 갱신)
- [ ] Detail 저장 callback에서 `fnSearchDetail()` 재호출 (화면 갱신)
- [ ] `<Bind>` 섹션의 `compid`가 Div 경로 포함 (`divSearch.form.edtXxx` 형식)
