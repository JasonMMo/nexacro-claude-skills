# DateRangePicker

**역할**: 시작일과 종료일을 한 번에 선택하는 달력 형태의 날짜 범위 선택 컴포넌트.
**출처**: `sample_daterangepicker_01.xfdl`

## 최소 구성

`<Layout>` 안에 배치:

```xml
<DateRangePicker id="DateRangePicker00" taborder="0"
                 left="50" top="50" width="420" height="285"
                 startdate="20230101"/>
```

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | 고유 컴포넌트 식별자 |
| `taborder` | ✓ | 탭 포커스 순서 |
| `left` / `top` / `width` / `height` | ✓ | 위치 및 크기 (픽셀) |
| `startdate` | | 시작일 초기값 (형식: `yyyyMMdd`) |
| `enddate` | | 종료일 초기값 (형식: `yyyyMMdd`) |
| `mindate` | | 선택 가능한 최소 날짜 |
| `maxdate` | | 선택 가능한 최대 날짜 |
| `useheadline` | | `true` 시 상단 헤드라인 영역 표시 |

## 이벤트

| 이벤트 | 서명 | 설명 |
|---|---|---|
| `onchange` | `fn(obj:nexacro.DateRangePicker, e:nexacro.ChangeEventInfo)` | 시작일 또는 종료일이 변경될 때 발생 |
| `ondayclick` | `fn(obj:nexacro.DateRangePicker, e:nexacro.EventInfo)` | 날짜 셀을 클릭할 때 발생 |

## 주의점 / 팁

- `startdate`, `enddate` 는 `yyyyMMdd` 형식의 문자열 또는 Date 값으로 설정한다.
- `mindate` / `maxdate` 는 런타임에 스크립트로 동적 변경 가능:
  ```javascript
  this.DateRangePicker00.mindate = this.Dataset00.getColumn(row, "mindate");
  this.DateRangePicker00.maxdate = this.Dataset00.getColumn(row, "maxdate");
  ```
- 인라인 달력 형태로 항상 화면에 노출되며, 팝업으로 사용하려면 `PopupDateRangePicker`를 사용한다.
- `width`는 두 달(Month) 패널을 나란히 표시할 만큼 충분히 확보해야 한다 (최소 약 400px).
