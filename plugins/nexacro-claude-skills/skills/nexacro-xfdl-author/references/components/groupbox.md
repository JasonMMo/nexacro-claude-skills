# GroupBox

**역할**: 제목이 있는 테두리 선으로 관련 컴포넌트를 시각적으로 묶어주는 그룹 컨테이너.
**출처**: `sample_groupbox_02.xfdl`

## 최소 구성

`<Layout>` 안에 배치. GroupBox 자체는 배경/테두리 역할이며, 자식 컴포넌트는 GroupBox와 **같은 레벨** `<Layout>` 에 배치하고 좌표를 GroupBox 범위 안으로 맞춘다:

```xml
<GroupBox id="GroupBox00" taborder="0"
          left="32" top="40" width="480" height="280"
          text="그룹 이름"/>
<!-- 자식 컴포넌트는 GroupBox와 동일 Layout에 위치 -->
<Static id="Static00" taborder="1" text="이름"
        left="48" top="96" width="120" height="32"/>
<Edit id="Edit00" taborder="2"
      left="120" top="96" width="240" height="32" value=""/>
```

### Div 방식 대안 (자식을 내부에 포함하려면)

자식을 내부에서 관리하려면 `GroupBox` 대신 `text` 속성이 있는 `Div`를 사용하거나, GroupBox 범위 내 좌표로 별도 컴포넌트를 배치하는 방식을 사용한다.

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | 고유 컴포넌트 식별자 |
| `taborder` | ✓ | 탭 포커스 순서 |
| `left` / `top` / `width` / `height` | ✓ | 위치 및 크기 (픽셀) |
| `text` | | 그룹 상단에 표시되는 제목 문자열 |
| `background` | | 배경색 |
| `border` | | 테두리 스타일 |

## 이벤트

| 이벤트 | 서명 | 설명 |
|---|---|---|
| `onclick` | `fn(obj:nexacro.GroupBox, e:nexacro.ClickEventInfo)` | GroupBox 클릭 시 발생 |

## 주의점 / 팁

- GroupBox는 자식 컴포넌트를 `<Layouts>` 로 포함하지 않는다. 자식은 **같은 `<Layout>`** 안에서 좌표로 GroupBox 영역 내에 배치한다.
- 자식 컴포넌트를 GroupBox와 함께 이동하려면 선택 후 그룹 이동 또는 `Div` 패턴을 사용한다.
- 디자인 툴에서 GroupBox → 자식 컴포넌트 순서로 `taborder`를 지정하면 탭 이동이 자연스럽다.
- 단순 시각적 구분 용도이므로 로직 컨테이너로는 `Div`를 권장한다.
