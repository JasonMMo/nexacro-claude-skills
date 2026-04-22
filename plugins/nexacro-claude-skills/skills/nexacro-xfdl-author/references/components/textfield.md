# TextField

**역할**: Material 스타일 단일행 텍스트 입력 컴포넌트. 라벨, 헬퍼 텍스트, 유효성 메시지를 내장하며 Edit의 현대적 대체재로 사용된다.
**Source**: `sample_textfield_02.xfdl`

## 최소 구성

`<Layout>` 내부에 배치:

```xml
<TextField id="tf_name" taborder="0" left="100" top="50" width="200" height="80"
           labeltext="이름" labelposition="inside" helpertext="성명을 입력하세요"
           usehelpertext="true" onchanged="tf_name_onchanged"/>
```

### Dataset 바인딩 형태

```xml
<TextField id="tf_name" taborder="0" left="100" top="50" width="200" height="80"
           labeltext="이름" labelposition="inside"/>
```

### `<Bind>` 블록 (sibling of `<Layouts>`)

```xml
<Bind>
  <BindItem id="bind0" compid="tf_name" propid="value" datasetid="ds_main" columnid="col_name"/>
</Bind>
```

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| id | ✓ | 컴포넌트 고유 식별자 |
| taborder | ✓ | 탭 포커스 순서 |
| left / top / width / height | ✓ | 위치 및 크기(픽셀) |
| labeltext | | 입력 필드 위/내부에 표시할 라벨 텍스트 |
| labelposition | | 라벨 위치: `"inside"` (기본), `"outside"` |
| labelfloatingfixed | | `"true"` 로 설정 시 라벨이 항상 상단에 고정 |
| helpertext | | 하단에 표시할 안내 문구 |
| usehelpertext | | `"true"` 로 설정해야 helpertext 가 렌더링됨 |
| usecharcount | | `"true"` 시 현재/최대 글자 수 표시 |
| inputtype | | `"email"`, `"number"` 등 입력 유형 제한 |
| invalidtext | | inputtype 유효성 실패 시 표시할 메시지 |
| usetrailingbutton | | `"true"` 시 오른쪽 끝에 버튼 표시 |
| cssclass | | 적용할 CSS 클래스명 |

## 이벤트

| 이벤트 | 시그니처 | 용도 |
|---|---|---|
| onchanged | `(obj:nexacro.TextField, e:nexacro.ChangeEventInfo)` | 값이 변경되고 포커스를 잃을 때 발생 |
| oninput | `(obj:nexacro.TextField, e:nexacro.InputEventInfo)` | 입력 중 실시간으로 발생 |

## 바인딩

Dataset 컬럼과 1:1 바인딩할 때 `<Bind>` 블록의 `propid`에 `"value"` 를 지정한다.

```javascript
// 런타임에서 값 읽기/쓰기
var name = this.tf_name.value;
this.tf_name.value = "홍길동";
```

## 주의점 / 팁

- `height`는 라벨+입력영역+헬퍼텍스트 합산이므로 Edit보다 넉넉히(70~90px) 설정해야 한다.
- `labelposition="inside"` 사용 시 `labelfloatingfixed="true"` 를 추가하면 라벨이 항상 위로 올라가 입력과 겹치지 않는다.
- `cssclass` 를 지정하지 않으면 기본 스타일만 적용되며, Material 하단 밑줄 스타일은 프로젝트 CSS 클래스에 의존한다.
