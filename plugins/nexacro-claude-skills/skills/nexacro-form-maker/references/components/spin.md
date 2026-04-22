# Spin

**역할**: 위/아래 버튼으로 숫자 값을 증감하는 스피너 컴포넌트. 최솟값, 최댓값, 증감 단위를 지정할 수 있다.
**Source**: `sample_spin_02.xfdl`

## 최소 구성

`<Layout>` 내부에 배치:

```xml
<Spin id="spin_qty" taborder="0" left="100" top="40" width="120" height="32"
      min="0" max="100" increment="1" value="0"/>
```

### 편집 불가(표시 전용) + 콤마 형식

```xml
<Spin id="spin_amount" taborder="0" left="100" top="40" width="200" height="32"
      min="-100000000" max="100000000" increment="1000"
      type="noneditable" displaycomma="true" value="0"/>
```

### Dataset 바인딩 형태

```xml
<Spin id="spin_qty" taborder="0" left="100" top="40" width="120" height="32"
      min="0" max="100" increment="1"/>
```

### `<Bind>` 블록 (sibling of `<Layouts>`)

```xml
<Bind>
  <BindItem id="bind0" compid="spin_qty" propid="value" datasetid="ds_main" columnid="col_qty"/>
</Bind>
```

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| id | ✓ | 컴포넌트 고유 식별자 |
| taborder | ✓ | 탭 포커스 순서 |
| left / top / width / height | ✓ | 위치 및 크기(픽셀) |
| min | | 최솟값 (기본값 없음) |
| max | | 최댓값 (기본값 없음) |
| increment | | 버튼 클릭 시 증감 단위 (기본 `1`) |
| value | | 초기값 |
| type | | `"noneditable"` 로 설정 시 키보드 직접 입력 차단 |
| displaycomma | | `"true"` 시 천 단위 콤마 표시 |

## 이벤트

| 이벤트 | 시그니처 | 용도 |
|---|---|---|
| onchanged | `(obj:nexacro.Spin, e:nexacro.ChangeEventInfo)` | 값이 변경될 때 발생; `obj.value` 로 현재 값 확인 |

## 바인딩

```javascript
// 런타임에서 값 읽기/쓰기
var qty = this.spin_qty.value;
this.spin_qty.value = 10;
```

## 주의점 / 팁

- `min` / `max` 를 지정하지 않으면 범위 제한 없이 음수 방향으로도 값이 내려간다.
- `type="noneditable"` 은 버튼으로만 값을 변경할 수 있도록 제한하며, 금액 입력 등에 적합하다.
