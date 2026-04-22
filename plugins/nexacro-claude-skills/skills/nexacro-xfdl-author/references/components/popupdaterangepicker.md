# PopupDateRangePicker

**역할**: 드롭다운 팝업 형태의 날짜 범위 선택 컴포넌트. `DateField` 등과 연동하여 입력 필드 아래에 펼쳐진다.
**출처**: `sample_datefield_01.xfdl` (DateField Notes 참조)

## 최소 구성

`<Layout>` 안에 배치 (초기 `visible`을 `false`로 두거나 팝업 API로 제어):

```xml
<PopupDateRangePicker id="PopupDateRangePicker00"
                      left="0" top="0" width="420" height="285"
                      visible="false"/>
```

### DateField와 연동 패턴

```xml
<DateField id="DateField00" taborder="0"
           left="50" top="50" width="150" height="32"
           ondropdown="DateField00_ondropdown"/>
<PopupDateRangePicker id="PopupDateRangePicker00"
                      left="0" top="0" width="420" height="285"
                      visible="false"
                      ondayclick="PopupDateRangePicker00_ondayclick"/>
```

```javascript
this.DateField00_ondropdown = function(obj, e) {
    this.PopupDateRangePicker00.trackPopupByComponent("start", obj, 0, 33);
    e.preventDefault();
};
this.PopupDateRangePicker00_ondayclick = function(obj, e) {
    this.DateField00.value = e.date;
};
```

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | 고유 컴포넌트 식별자 |
| `left` / `top` / `width` / `height` | ✓ | 기준 위치 및 크기 |
| `startdate` | | 시작일 초기값 (`yyyyMMdd`) |
| `enddate` | | 종료일 초기값 (`yyyyMMdd`) |
| `mindate` | | 선택 가능한 최소 날짜 |
| `maxdate` | | 선택 가능한 최대 날짜 |
| `visible` | | 초기 표시 여부 (보통 `false`) |

## 이벤트

| 이벤트 | 서명 | 설명 |
|---|---|---|
| `ondayclick` | `fn(obj:nexacro.PopupDateRangePicker, e:nexacro.EventInfo)` | 날짜 클릭 시 발생; `e.date`로 선택된 날짜 획득 |
| `onchange` | `fn(obj:nexacro.PopupDateRangePicker, e:nexacro.ChangeEventInfo)` | 날짜 범위 변경 시 발생 |

## 주의점 / 팁

- `trackPopupByComponent(mode, component, offsetX, offsetY)` 로 팝업을 열며, `mode`는 `"start"` 또는 `"end"`.
- `DateField.ondropdown` 에서 반드시 `e.preventDefault()`를 호출해야 기본 달력 팝업이 중복 표시되지 않는다.
- 팝업이 화면 밖으로 나가지 않도록 `offsetX`, `offsetY` 를 적절히 조정한다.
- 인라인 항상 표시 버전은 `DateRangePicker`를 사용한다.
