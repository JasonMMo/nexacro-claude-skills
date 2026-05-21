# 복잡 화면 패턴: Multi-Tab

## 언제 이 패턴을 사용하는가

동일한 조회 조건 아래 **카테고리별로 다른 데이터**를 탭으로 분리할 때:
- 기본정보 / 상세이력 / 연관항목처럼 논리적으로 묶이는 여러 Grid
- 한 화면에 모두 펼치면 스크롤이 과도해지는 경우
- 탭별로 독립적인 백엔드 쿼리가 필요한 경우

---

## 레이아웃 구조 (ASCII)

```
┌─────────────────────────────────────────────────────────────┐
│ [사용자ID]: [________]  [조회]                               │  divSearch (h:40)
├─────────────────────────────────────────────────────────────┤
│ ┌──────────┬──────────┬──────────┐                          │
│ │ 기본정보 │ 권한정보 │ 변경이력 │  ← Tab 헤더              │  tabMain
│ ├──────────┴──────────┴──────────┴───────────────────────┐  │
│ │                                                          │  │
│ │  [각 탭의 Grid]                                          │  │  각 Tabpage
│ │                                                          │  │
│ └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Lazy Loading 전략**:
- 탭 0 (기본정보): `form_onload` 시 즉시 로드
- 탭 1, 2 (권한/이력): 첫 선택 시에만 로드 (`rowcount == 0` 체크)
- 조회 버튼 클릭: 모든 탭 Dataset 초기화 후 현재 탭 재로드

---

## Dataset 선언 규칙

| Dataset ID      | 역할                    |
|-----------------|-------------------------|
| `dsSearch`      | 공통 조회 조건           |
| `dsBasic`       | 탭 0 — 기본정보 결과    |
| `dsPermission`  | 탭 1 — 권한정보 결과    |
| `dsHistory`     | 탭 2 — 변경이력 결과    |

> 탭이 n개면 Dataset도 n개. 이름 규칙: `ds{TabPurpose}`.

---

## 완성 XFDL 예제

```xml
<?xml version="1.0" encoding="utf-8"?>
<FDL version="2.1">
  <Form id="UserMgmt" classname="Work" titletext="사용자 관리"
        left="0" top="0" width="1050" height="768" onload="form_onload">
    <Layouts>
      <Layout>

        <!-- ① 조회 조건 (공통) -->
        <Div id="divSearch" left="0" top="0" right="0" height="40">
          <Layouts><Layout>
            <Static id="staUserId" text="사용자ID" left="5" top="8"
                    width="70" height="25" cssclass="sta_WF_SubTitle"/>
            <Edit id="edtUserId" left="80" top="8" width="150" height="25"/>
            <Button id="btnSearch" text="조회" left="240" top="8" width="65" height="25"
                    onclick="fnSearch" borderRadius="5px"/>
          </Layout></Layouts>
        </Div>

        <!-- ② 탭 컨테이너 -->
        <Tab id="tabMain" left="0" top="40" right="0" bottom="0"
             onchanged="tabMain_onchanged">

          <!-- 탭 0: 기본정보 -->
          <Tabpage id="tpBasic" text="기본정보">
            <Grid id="grdBasic" left="0" top="0" right="0" bottom="0"
                  binddataset="dsBasic" autofittype="col">
              <Formats>
                <Format id="default">
                  <Columns>
                    <Column size="100"/>
                    <Column size="150"/>
                    <Column size="200"/>
                    <Column size="100"/>
                  </Columns>
                  <Rows>
                    <Row size="25" band="head"/>
                    <Row size="30"/>
                  </Rows>
                  <Band id="head">
                    <Cell text="사용자ID"/>
                    <Cell col="1" text="사용자명"/>
                    <Cell col="2" text="이메일"/>
                    <Cell col="3" text="등록일"/>
                  </Band>
                  <Band id="body">
                    <Cell text="bind:userId"/>
                    <Cell col="1" text="bind:userNm"  edittype="normal"/>
                    <Cell col="2" text="bind:email"   edittype="normal"/>
                    <Cell col="3" text="bind:regDt"/>
                  </Band>
                </Format>
              </Formats>
            </Grid>
          </Tabpage>

          <!-- 탭 1: 권한정보 -->
          <Tabpage id="tpPermission" text="권한정보">
            <Grid id="grdPermission" left="0" top="0" right="0" bottom="0"
                  binddataset="dsPermission" autofittype="col">
              <Formats>
                <Format id="default">
                  <Columns>
                    <Column size="100"/>
                    <Column size="200"/>
                    <Column size="100"/>
                  </Columns>
                  <Rows>
                    <Row size="25" band="head"/>
                    <Row size="30"/>
                  </Rows>
                  <Band id="head">
                    <Cell text="권한코드"/>
                    <Cell col="1" text="권한명"/>
                    <Cell col="2" text="부여일"/>
                  </Band>
                  <Band id="body">
                    <Cell text="bind:roleId"/>
                    <Cell col="1" text="bind:roleNm"/>
                    <Cell col="2" text="bind:grantDt"/>
                  </Band>
                </Format>
              </Formats>
            </Grid>
          </Tabpage>

          <!-- 탭 2: 변경이력 -->
          <Tabpage id="tpHistory" text="변경이력">
            <Grid id="grdHistory" left="0" top="0" right="0" bottom="0"
                  binddataset="dsHistory" autofittype="col">
              <Formats>
                <Format id="default">
                  <Columns>
                    <Column size="150"/>
                    <Column size="200"/>
                    <Column size="150"/>
                  </Columns>
                  <Rows>
                    <Row size="25" band="head"/>
                    <Row size="30"/>
                  </Rows>
                  <Band id="head">
                    <Cell text="변경일시"/>
                    <Cell col="1" text="변경내용"/>
                    <Cell col="2" text="처리자"/>
                  </Band>
                  <Band id="body">
                    <Cell text="bind:chgDt"/>
                    <Cell col="1" text="bind:chgDesc"/>
                    <Cell col="2" text="bind:handler"/>
                  </Band>
                </Format>
              </Formats>
            </Grid>
          </Tabpage>

        </Tab>

      </Layout>
    </Layouts>

    <Objects>
      <Dataset id="dsSearch">
        <ColumnInfo>
          <Column id="searchUserId" type="STRING" size="50"/>
        </ColumnInfo>
        <Rows><Row><Col id="searchUserId"/></Row></Rows>
      </Dataset>

      <Dataset id="dsBasic">
        <ColumnInfo>
          <Column id="userId" type="STRING" size="20"/>
          <Column id="userNm" type="STRING" size="50"/>
          <Column id="email"  type="STRING" size="100"/>
          <Column id="regDt"  type="STRING" size="8"/>
        </ColumnInfo>
      </Dataset>

      <Dataset id="dsPermission">
        <ColumnInfo>
          <Column id="roleId"  type="STRING" size="20"/>
          <Column id="roleNm"  type="STRING" size="100"/>
          <Column id="grantDt" type="STRING" size="8"/>
        </ColumnInfo>
      </Dataset>

      <Dataset id="dsHistory">
        <ColumnInfo>
          <Column id="chgDt"   type="STRING" size="17"/>
          <Column id="chgDesc" type="STRING" size="200"/>
          <Column id="handler" type="STRING" size="50"/>
        </ColumnInfo>
      </Dataset>
    </Objects>

    <Bind>
      <BindItem id="bi_searchUserId" compid="divSearch.form.edtUserId"
                propid="value" datasetid="dsSearch" columnid="searchUserId"/>
    </Bind>

    <Script type="xscript5.1"><![CDATA[

// ─── Form 초기화 ────────────────────────────────────────────────────────────
this.form_onload = function(obj:nexacro.Form, e:nexacro.LoadEventInfo) {
    this.gfnFormOnLoad(this);
    this.fnSearchBasic();            // 탭 0만 즉시 로드
};

// ─── Callback ───────────────────────────────────────────────────────────────
this.fnCallback = function(svcID, errorCode, errorMsg) {
    if (errorCode != 0) return;
    // 각 탭 조회 완료 후 특별한 후처리가 없으면 case 생략 가능
    switch(svcID) {
        case "searchBasic":      break;
        case "searchPermission": break;
        case "searchHistory":    break;
    }
};

// ─── 조회 버튼 (공통) ───────────────────────────────────────────────────────
// 모든 탭 Dataset 초기화 후 현재 탭만 재로드 (나머지는 탭 이동 시 lazy 로드)
this.fnSearch = function() {
    this.dsBasic.clearData();
    this.dsPermission.clearData();
    this.dsHistory.clearData();

    var nCurTab = this.tabMain.tabindex;
    switch(nCurTab) {
        case 0: this.fnSearchBasic();      break;
        case 1: this.fnSearchPermission(); break;
        case 2: this.fnSearchHistory();    break;
    }
};

// ─── 탭별 조회 함수 ─────────────────────────────────────────────────────────
this.fnSearchBasic = function() {
    this.gfnTransaction(
        "searchBasic",
        "selectUserBasicList.do",
        "dsSearch=dsSearch",
        "dsBasic=output1",
        "", "fnCallback", true
    );
};

this.fnSearchPermission = function() {
    this.gfnTransaction(
        "searchPermission",
        "selectUserPermissionList.do",
        "dsSearch=dsSearch",
        "dsPermission=output1",
        "", "fnCallback", true
    );
};

this.fnSearchHistory = function() {
    this.gfnTransaction(
        "searchHistory",
        "selectUserHistoryList.do",
        "dsSearch=dsSearch",
        "dsHistory=output1",
        "", "fnCallback", true
    );
};

// ─── 탭 전환 이벤트 (Lazy Loading) ─────────────────────────────────────────
this.tabMain_onchanged = function(obj:nexacro.Tab, e:nexacro.TabChangedEventInfo) {
    switch(e.postindex) {
        case 0:
            // 기본정보: 이미 로드됨, 재로드 불필요 (조회 버튼으로 명시적으로 초기화)
            break;
        case 1:
            if (this.dsPermission.rowcount == 0) {
                this.fnSearchPermission();    // 첫 진입 시에만 조회
            }
            break;
        case 2:
            if (this.dsHistory.rowcount == 0) {
                this.fnSearchHistory();       // 첫 진입 시에만 조회
            }
            break;
    }
};

    ]]></Script>
  </Form>
</FDL>
```

---

## gfnTransaction inData / outData 규칙

| 탭 | inData | outData |
|----|--------|---------|
| 공통 조건 적용 | `"dsSearch=dsSearch"` | `"ds{Tab}=output1"` |
| 탭 개별 조건 필요 시 | `"dsSearch{Tab}=dsSearch{Tab}"` | `"ds{Tab}=output1"` |

---

## 이벤트 흐름

```
form_onload → fnSearchBasic() → 탭 0 Grid 표출

사용자가 탭 1 클릭
    └→ tabMain_onchanged(e.postindex=1)
            └→ dsPermission.rowcount==0 이면 fnSearchPermission()
            └→ rowcount>0 이면 스킵 (이미 로드됨)

조회 버튼 클릭
    └→ fnSearch()
            └→ 모든 Dataset clearData()
            └→ 현재 탭 인덱스 확인 → 해당 탭만 즉시 재로드
            └→ 다른 탭은 lazy (탭 이동 시 rowcount==0 체크로 재로드)
```

---

## DB 스키마 → XFDL 변환 룰

| 조건 | 탭 구성 방식 |
|------|--------------|
| 테이블 1개, 컬럼 20개 이상 | 컬럼 그룹별로 탭 분리 |
| FK 관계 + 조회 목적만 | 탭으로 분리 (Master-Detail이 아닌 경우) |
| 동일 PK 기반 여러 연관 테이블 | 각 연관 테이블 = 각 탭 |

탭 이름 명명: 업무 의미 기반 (기본정보, 상세이력, 연관코드 등)

---

## 생성 검증 체크리스트

- [ ] 각 `<Tabpage>`의 `id`와 `text` 설정 확인
- [ ] `tabMain_onchanged`에서 `e.postindex`로 탭 분기 (0-based 인덱스)
- [ ] Lazy loading: `dsXxx.rowcount == 0` 체크 후 조회
- [ ] 조회 버튼 `fnSearch()`에서 **모든** Dataset `clearData()` 후 현재 탭만 재로드
- [ ] 탭 전환 시 조회 조건 Dataset(`dsSearch`)은 초기화하지 않음 — 공통 조건 유지
- [ ] 각 탭 Grid의 `binddataset`이 올바른 Dataset을 가리키는지 확인
- [ ] `tabMain.tabindex`로 현재 탭 인덱스 조회 (0-based)
