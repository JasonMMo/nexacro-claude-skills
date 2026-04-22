# MultiCombo

**역할**: Combo 컴포넌트의 확장형으로 여러 항목을 동시에 선택할 수 있는 다중 선택 드롭다운 컴포넌트.
**Source**: `sample_multicombo_02.xfdl`, `sample_multicombo_03.xfdl`, `sample_multicombo_04.xfdl`

## 최소 구성

`<Layout>` 내부에 배치 (`edittype="count"` — 선택 개수 표시):

```xml
<MultiCombo id="mc_items" taborder="0" left="25" top="25" width="295" height="35"
            innerdataset="dsMultiCombo" codecolumn="code" datacolumn="data"
            edittype="count"/>
```

태그 스타일 + 전체선택 체크박스 (`edittype="multitag"`):

```xml
<MultiCombo id="mc_items" taborder="0" left="25" top="25" width="365" height="270"
            edittype="multitag" innerdataset="dsMultiCombo"
            codecolumn="code" datacolumn="data"
            showselectallcheckbox="true"/>
```

`<Objects>` 에 Dataset 선언 (두 변형 공통):

```xml
<Dataset id="dsMultiCombo">
  <ColumnInfo>
    <Column id="code" type="STRING" size="256"/>
    <Column id="data" type="STRING" size="256"/>
    <Column id="readonly" type="STRING" size="256"/>
  </ColumnInfo>
  <Rows>
    <Row><Col id="code">1</Col><Col id="data">apple</Col><Col id="readonly">0</Col></Row>
    <Row><Col id="code">2</Col><Col id="data">banana</Col><Col id="readonly">0</Col></Row>
  </Rows>
</Dataset>
```

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| id | ✓ | 컴포넌트 고유 식별자 |
| taborder | ✓ | 탭 포커스 순서 |
| left / top / width / height | ✓ | 위치 및 크기(픽셀) |
| innerdataset | ✓ | 항목을 공급하는 Dataset ID |
| codecolumn | ✓ | 저장값으로 사용할 컬럼명 |
| datacolumn | ✓ | 화면 표시 텍스트로 사용할 컬럼명 |
| edittype | | `"count"` (선택 개수 표시), `"multitag"` (선택 항목을 태그로 표시) |
| type | | `"search"` 설정 시 드롭다운에 검색 필터 입력창 표시, `"dropdown"` 은 기본 |
| showselectallcheckbox | | `"true"` 시 전체 선택 체크박스 표시 |
| readonlycolumn | | 비활성화 여부 컬럼명 (값 `"1"` 이면 선택 불가) |
| readonly | | `"true"` 시 드롭다운 열기 차단 |

## 이벤트

| 이벤트 | 시그니처 | 용도 |
|---|---|---|
| onitemchanged | `(obj:nexacro.MultiCombo, e:nexacro.ItemChangeEventInfo)` | 선택 항목 변경 시 발생 |

## 바인딩

선택된 항목은 `index` 속성으로 읽거나 설정한다 (쉼표 구분 인덱스 문자열).

```javascript
var selected = this.mc_items.index; // 예: "0,2,3"
this.mc_items.index = "0,1,2";     // 스크립트로 선택 지정
```

## 주의점 / 팁

- `edittype="multitag"` 사용 시 `height` 를 충분히 크게 설정해야 태그가 잘리지 않는다(드롭다운 영역 포함).
- `type="search"` 와 `type="dropdown"` 은 런타임에서도 `this.mc_items.type = "dropdown";` 으로 전환 가능하다.
- `index` 는 Dataset의 행 번호(0-base)이며 `value` 와 다르므로 혼동하지 않도록 주의한다.
