# ListView

**역할**: 모바일·카드형 목록 표시 컴포넌트. Dataset에 바인딩하고 `<Format>` 내부에 `<Band>`/`<Cell>`로 아이템 템플릿을 정의한다. Grid와 달리 자유로운 레이아웃의 아이템 행을 구성할 수 있다.
**출처**: `sample_listview_01.xfdl`, `sample_listview_02.xfdl`, `sample_listview_03.xfdl`

## 최소 구성

`<Layout>` 안에 배치하고, Dataset과 함께 사용:

```xml
<ListView id="ListView00" taborder="0"
          left="20" top="20" width="500" height="500"
          binddataset="Dataset00"
          oncellclick="ListView00_oncellclick">
  <Formats>
    <Format id="default">
      <Band id="body" width="100%" height="80">
        <Cell id="cellTitle" left="10" top="10" width="200" height="30"
              text="bind:title" font="normal bold 16px/normal &quot;Gulim&quot;"
              border="0px none"/>
        <Cell id="cellSub"   left="10" top="45" width="300" height="25"
              text="bind:subtitle" border="0px none"/>
      </Band>
    </Format>
  </Formats>
</ListView>
```

### 함께 사용하는 Dataset

```xml
<Dataset id="Dataset00">
  <ColumnInfo>
    <Column id="title"    type="STRING" size="256"/>
    <Column id="subtitle" type="STRING" size="256"/>
  </ColumnInfo>
</Dataset>
```

## 주요 속성

| 속성 | 설명 |
|---|---|
| `binddataset` | 바인딩할 Dataset의 `id` |
| `formatid` | 런타임에 전환할 Format의 `id` (기본값: `"default"`) |
| `bandinitstatus` | `"collapse"` — 상세 Band(`detail`) 초기 상태를 접힘으로 설정 |
| `bandexpandtype` | 아이템 펼침 방식: `"expand"` / `"toggle"` / `"none"` |
| `bandindentsize` | 중첩 Band 들여쓰기 크기(px) |

### Format 내부 Band 속성

| Band `id` | 용도 |
|---|---|
| `body` | 각 Dataset 행마다 반복 렌더링되는 기본 아이템 영역 |
| `detail` | `body` 아래 펼쳐지는 확장 영역 (`bandinitstatus="collapse"` 와 함께 사용) |

## 이벤트

| 이벤트 | 시그니처 | 설명 |
|---|---|---|
| `oncellclick` | `(obj:nexacro.ListView, e:nexacro.ListViewClickEventInfo)` | 아이템 셀 클릭 시 발생. `e.row`로 행 인덱스 확인 |

## 사용 API (스크립트)

```javascript
// 런타임 Format 전환
this.ListView00.formatid = "format00";
this.ListView00.formatid = "default";

// 펼침 방식 변경
this.ListView00.bandexpandtype = "toggle";

// 클릭 이벤트 처리
this.ListView00_oncellclick = function(obj, e) {
    var row = e.row;
    var title = this.Dataset00.getColumn(row, "title");
    this.alert(title);
};
```

## 주의점 / 팁

- `<Band id="body">` 내부의 Cell `text`는 반드시 `"bind:컬럼명"` 형식으로 Dataset 컬럼에 바인딩한다.
- `displaytype="imagecontrol"`을 Cell에 지정하면 이미지 URL을 Dataset 값으로 직접 표시할 수 있다.
- 여러 `<Format>`을 정의하고 `formatid`를 런타임에 교체하면 동일 데이터를 다른 레이아웃으로 전환할 수 있다.
- `detail` Band와 `bandinitstatus="collapse"` 조합으로 아코디언형 목록을 구현한다.
