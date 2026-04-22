# CheckBoxSet

**역할**: Dataset의 각 행을 체크박스 항목으로 렌더링하는 컴포넌트. Radio와 유사하나 다중 선택을 허용한다.
**Source**: `sample_checkboxset_01.xfdl`

## 최소 구성

`<Layout>` 내부에 배치:

```xml
<CheckBoxSet id="cbs_fruit" taborder="0" left="25" top="25" width="200" height="100"
             innerdataset="dsCheckBoxSet" codecolumn="code" datacolumn="data" columncount="2"/>
```

`<Objects>` 에 Dataset 선언:

```xml
<Objects>
  <Dataset id="dsCheckBoxSet">
    <ColumnInfo>
      <Column id="code" type="STRING" size="256"/>
      <Column id="data" type="STRING" size="256"/>
      <Column id="readonly" type="STRING" size="256"/>
    </ColumnInfo>
    <Rows>
      <Row><Col id="code">1</Col><Col id="data">apple</Col><Col id="readonly">0</Col></Row>
      <Row><Col id="code">2</Col><Col id="data">banana</Col><Col id="readonly">0</Col></Row>
      <Row><Col id="code">3</Col><Col id="data">orange</Col><Col id="readonly">0</Col></Row>
    </Rows>
  </Dataset>
</Objects>
```

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| id | ✓ | 컴포넌트 고유 식별자 |
| taborder | ✓ | 탭 포커스 순서 |
| left / top / width / height | ✓ | 위치 및 크기(픽셀) |
| innerdataset | ✓ | 항목을 공급하는 Dataset ID |
| codecolumn | ✓ | 체크 시 저장값으로 사용할 컬럼명 |
| datacolumn | ✓ | 화면 표시 텍스트로 사용할 컬럼명 |
| readonlycolumn | | 비활성화 여부를 결정하는 컬럼명 (값 `"1"` 이면 비활성) |
| columncount | | 가로 배치할 체크박스 열 수 (기본 `1`) |

## 이벤트

| 이벤트 | 시그니처 | 용도 |
|---|---|---|
| onitemchanged | `(obj:nexacro.CheckBoxSet, e:nexacro.ItemChangeEventInfo)` | 체크 상태 변경 시 발생 |

## 바인딩

CheckBoxSet은 항목 공급에 Dataset을 사용한다. 체크된 항목 코드는 스크립트로 취득한다.

```javascript
// 체크된 항목 코드 취득 (쉼표 구분 문자열)
var checkedValue = this.cbs_fruit.value;

// 개별 항목 체크 상태 확인
var item = this.cbs_fruit.getItem(0); // 0번째 항목 정보
```

## 주의점 / 팁

- `readonlycolumn` 컬럼 값이 `"1"` 인 항목은 사용자가 체크/해제할 수 없으나 스크립트로는 변경 가능하다.
- `columncount` 로 열 수를 지정하면 항목이 좌→우 순서로 배치된다. 세로 배치가 필요하면 `direction="vertical"` 을 사용한다.
- `value` 속성은 체크된 항목의 `codecolumn` 값을 쉼표로 연결한 문자열을 반환한다.
