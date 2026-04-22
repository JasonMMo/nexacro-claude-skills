# ListBox

**역할**: Dataset에서 항목을 목록으로 표시하며 단일 또는 다중 선택을 지원하는 컴포넌트. Combo와 달리 항목이 펼쳐진 상태로 항상 표시된다.
**Source**: `sample_listbox_03.xfdl`

## 최소 구성

`<Layout>` 내부에 배치:

```xml
<ListBox id="lb_items" taborder="0" left="48" top="40" width="240" height="140"
         innerdataset="ds_items" codecolumn="CODE" datacolumn="DATA"/>
```

### 다중 선택 + 외부 Dataset

```xml
<ListBox id="lb_items" taborder="0" left="48" top="40" width="240" height="140"
         innerdataset="@ds_items" codecolumn="CODE" datacolumn="DATA" multiselect="true"/>
```

외부 Dataset은 `<Objects>` 내부에 선언한다:

```xml
<Objects>
  <Dataset id="ds_items">
    <ColumnInfo>
      <Column id="CODE" type="STRING" size="256"/>
      <Column id="DATA" type="STRING" size="256"/>
    </ColumnInfo>
    <Rows>
      <Row><Col id="CODE">01</Col><Col id="DATA">항목1</Col></Row>
      <Row><Col id="CODE">02</Col><Col id="DATA">항목2</Col></Row>
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
| innerdataset | ✓ | 항목을 공급하는 Dataset ID (`@` 접두사로 외부 Dataset 참조) |
| codecolumn | ✓ | 저장값으로 사용할 Dataset 컬럼명 |
| datacolumn | ✓ | 화면 표시 텍스트로 사용할 Dataset 컬럼명 |
| multiselect | | `"true"` 시 다중 선택 허용 |

## 이벤트

| 이벤트 | 시그니처 | 용도 |
|---|---|---|
| onitemchanged | `(obj:nexacro.ListBox, e:nexacro.ItemChangeEventInfo)` | 선택 항목이 변경될 때 발생 |

## 바인딩

ListBox는 항목 공급(`innerdataset`)과 선택값 바인딩을 분리해서 사용한다.

```javascript
// 선택된 항목 취득 (multiselect 시)
var arrSelected = this.lb_items.getSelectedItems(); // 선택된 행 인덱스 배열
var count       = this.lb_items.getSelectedCount();
// 전체 선택: for (var i=0; i<this.lb_items.getCount(); i++) this.lb_items.setSelect(i, true);
```

## 주의점 / 팁

- 외부 Dataset을 `innerdataset`에 참조할 때는 `@` 접두사를 붙여야 한다 (예: `"@ds_items"`).
- `multiselect="true"` 일 때 선택값은 `value` 속성 하나로 접근할 수 없으며 `getSelectedItems()` 를 사용해야 한다.
- Combo와 달리 항목 목록이 항상 펼쳐져 있으므로 `height` 를 충분히 확보해야 항목이 잘리지 않는다.
