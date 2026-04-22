# 데이터 바인딩 패턴 (Dataset + BindItem)

Nexacro 의 핵심 패턴: **Dataset 하나를 여러 UI 컴포넌트에 연결** 하여 자동 양방향 동기화.

## 3가지 바인딩 패턴

### 패턴 A — BindItem (1:1 단일 필드 바인딩)

Edit / CheckBox / Calendar 등 **단일 값** 컴포넌트를 Dataset 의 현재 행(currow) 특정 컬럼에 연결.

```xml
<Form id="main" width="1280" height="720">
  <Layouts>
    <Layout width="1280" height="720">
      <Edit id="edName"  left="100" top="100" width="200" height="28" taborder="0"/>
      <Edit id="edEmail" left="100" top="140" width="200" height="28" taborder="1"/>
    </Layout>
  </Layouts>

  <Objects>
    <Dataset id="dsCustomer">
      <ColumnInfo>
        <Column id="name"  size="50" type="STRING"/>
        <Column id="email" size="100" type="STRING"/>
      </ColumnInfo>
      <Rows>
        <Row><Col id="name">홍길동</Col><Col id="email">hong@example.com</Col></Row>
      </Rows>
    </Dataset>

    <!-- ↓ BindItem 선언부 -->
    <BindItem id="bi_name"  compid="edName"  propid="value" datasetid="dsCustomer" columnid="name"/>
    <BindItem id="bi_email" compid="edEmail" propid="value" datasetid="dsCustomer" columnid="email"/>
  </Objects>
</Form>
```

### `<BindItem>` 속성

| 속성 | 설명 |
|---|---|
| `id` | BindItem 식별자 |
| `compid` | 바인딩 대상 컴포넌트 id |
| `propid` | 연결할 속성 (`value`, `text`, `checked` 등) |
| `datasetid` | Dataset id |
| `columnid` | Dataset 의 컬럼 id |

### 패턴 B — innerdataset (컴포넌트 내부 임베디드)

Combo / Radio 처럼 **항목 리스트** 가 필요한 컴포넌트는 내부 `<Dataset>` 을 직접 포함.

```xml
<Combo id="cbGender" taborder="0" left="100" top="100" width="120" height="28"
       codecolumn="code" datacolumn="data" innerdataset="@ds_gender">
  <Dataset id="ds_gender">
    <ColumnInfo>
      <Column id="code" size="10" type="STRING"/>
      <Column id="data" size="20" type="STRING"/>
    </ColumnInfo>
    <Rows>
      <Row><Col id="code">M</Col><Col id="data">남</Col></Row>
      <Row><Col id="code">F</Col><Col id="data">여</Col></Row>
    </Rows>
  </Dataset>
</Combo>
```

- `codecolumn` = 실제 저장값 컬럼
- `datacolumn` = 사용자에게 표시될 라벨 컬럼
- `innerdataset="@ds_gender"` — `@` 접두사로 내부 Dataset 참조

### 패턴 C — binddataset (Grid / ListView 대량 행 바인딩)

Grid 는 **다중 행 표시** 컴포넌트라 `binddataset` 한 속성으로 전체 Dataset 을 연결.

```xml
<Layout>
  <Grid id="grdList" left="10" top="10" width="800" height="400"
        binddataset="dsCustomer" autofittype="col">
    <Formats>
      <Format id="default">
        <Columns>
          <Column size="200"/>
          <Column size="300"/>
        </Columns>
        <Rows>
          <Row band="head" size="28"/>
          <Row size="28"/>
        </Rows>
        <Band id="head">
          <Cell col="0" text="이름"/>
          <Cell col="1" text="이메일"/>
        </Band>
        <Band id="body">
          <Cell col="0" text="bind:name"/>
          <Cell col="1" text="bind:email"/>
        </Band>
      </Format>
    </Formats>
  </Grid>
</Layout>

<Objects>
  <Dataset id="dsCustomer"> ... </Dataset>
</Objects>
```

- `binddataset="dsCustomer"` — Grid 가 Dataset 전체 행을 렌더
- `<Cell text="bind:컬럼명"/>` — 해당 셀이 그 컬럼 값을 표시 + 편집 가능

## 바인딩 세 패턴 비교

| 패턴 | 용도 | 컴포넌트 예 | Dataset 위치 |
|---|---|---|---|
| BindItem | 단일 필드 ↔ 현재행 | Edit, MaskEdit, Calendar, CheckBox | `<Objects>` 아래 |
| innerdataset | 선택 항목 리스트 | Combo, Radio | 컴포넌트 **내부** (자식) |
| binddataset | 다중 행 표시 | Grid, ListView | `<Objects>` 아래 |

## 양방향 동기화 동작

- **UI → Dataset**: 사용자가 Edit 값 변경 → Dataset 컬럼 값 자동 갱신 → `_RowType_` 이 `N` 이었다면 `U` 로 전이.
- **Dataset → UI**: 스크립트에서 `dsCustomer.setColumn(0, "name", "김철수")` → Edit 이 자동 리렌더.
- **현재행(currow) 이동**: `dsCustomer.set_rowposition(1)` → 모든 BindItem 이 새 행 값으로 갱신.

## 자주 쓰는 API

```javascript
// 행 추가
var nRow = this.dsCustomer.addRow();
this.dsCustomer.setColumn(nRow, "name", "신규");

// 현재행 조회
var row = this.dsCustomer.rowposition;
var name = this.dsCustomer.getColumn(row, "name");

// 삭제 (실제로는 _RowType_ 이 D 로 마킹)
this.dsCustomer.deleteRow(row);

// 변경 사항 유무
if (this.dsCustomer.isUpdated()) { ... }
```

## 자주 틀리는 포인트

| 증상 | 원인 | 해결 |
|---|---|---|
| Edit 에 값이 안 찍힘 | BindItem `columnid` 오타 | Dataset 실제 컬럼 id 와 대소문자 정확히 일치 확인 |
| Combo 항목 빈칸 | `datacolumn` 미지정 | `codecolumn` + `datacolumn` 둘 다 필수 |
| Grid 리사이즈 안됨 | `autofittype` 누락 | `autofittype="col"` 또는 `"row"` 지정 |
| `innerdataset="@..."` 누락 오류 | `@` 접두사 빠짐 | 반드시 `@` 붙여야 참조됨 |

## 런타임 wire format 으로의 직렬화

Dataset 의 내용은 서버 통신 시 `_RowType_` 포함한 XML / SSV / JSON 중 하나로 직렬화됩니다.

→ `nexacro-data-format` skill 의 `references/{xml,ssv,json}-format.md` 참조
