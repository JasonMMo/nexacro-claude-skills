# PopupMenu

**역할**: 우클릭 또는 버튼 클릭 시 `trackPopup` API로 표시하는 컨텍스트 메뉴. Dataset 바인딩으로 항목을 구성한다.
**출처**: `sample_popupmenu_01.xfdl`

## 최소 구성

`<Layout>` 안에 배치 (초기 위치는 화면 밖으로 설정):

```xml
<PopupMenu id="popupmenuCtx"
           left="-104" top="-64" width="93" height="113"
           captioncolumn="captioncolumn"
           idcolumn="idcolumn"
           levelcolumn="levelcolumn"
           enablecolumn="enablecolumn"
           checkboxcolumn="checkboxcolumn"
           hotkeycolumn="hotkeycolumn"
           iconcolumn="iconcolumn"
           userdatacolumn="userdatacolumn"
           onmenuclick="popupmenuCtx_onmenuclick"/>
```

### 동반 Dataset (필수)

```xml
<Dataset id="datasetPopup">
  <ColumnInfo>
    <Column id="captioncolumn"  type="STRING" size="256"/>
    <Column id="idcolumn"       type="STRING" size="256"/>
    <Column id="levelcolumn"    type="INT"    size="4"/>
    <Column id="enablecolumn"   type="STRING" size="256"/>
    <Column id="checkboxcolumn" type="STRING" size="256"/>
    <Column id="hotkeycolumn"   type="STRING" size="256"/>
    <Column id="iconcolumn"     type="STRING" size="256"/>
    <Column id="userdatacolumn" type="STRING" size="256"/>
  </ColumnInfo>
  <Rows>
    <Row><Col id="captioncolumn">항목 A</Col><Col id="idcolumn">A</Col><Col id="levelcolumn">0</Col></Row>
    <Row><Col id="captioncolumn">항목 B</Col><Col id="idcolumn">B</Col><Col id="levelcolumn">0</Col></Row>
    <Row><Col id="captioncolumn">항목 C</Col><Col id="idcolumn">C</Col><Col id="levelcolumn">0</Col></Row>
  </Rows>
</Dataset>
```

### trackPopup 호출 패턴

```javascript
// 우클릭 이벤트에서 팝업 표시
this.Form_onrclick = function(obj, e) {
    this.popupmenuCtx.trackPopup(e.clientX, e.clientY);
};

// 버튼 클릭에서 팝업 표시
this.Button00_onclick = function(obj, e) {
    this.popupmenuCtx.trackPopup(obj.getOffsetLeft(), obj.getOffsetTop() + obj.getOffsetHeight());
};
```

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | 고유 컴포넌트 식별자 |
| `left` / `top` / `width` / `height` | ✓ | 기본 크기 (팝업 시 위치는 trackPopup이 결정) |
| `captioncolumn` | ✓ | 메뉴 표시 텍스트 컬럼명 |
| `idcolumn` | ✓ | 항목 고유 ID 컬럼명 |
| `levelcolumn` | ✓ | 계층 깊이 컬럼명 (0-based) |
| `enablecolumn` | | 활성화 여부 컬럼명 |
| `checkboxcolumn` | | 체크박스 표시 컬럼명 |
| `hotkeycolumn` | | 단축키 표시 텍스트 컬럼명 |
| `iconcolumn` | | 아이콘 컬럼명 |

## 이벤트

| 이벤트 | 서명 | 설명 |
|---|---|---|
| `onmenuclick` | `fn(obj:nexacro.PopupMenu, e:nexacro.MenuClickEventInfo)` | 항목 클릭 시 발생; `e.id`로 항목 식별 |

## 주의점 / 팁

- `trackPopup(x, y)` 의 x, y는 폼 기준 절대 좌표이다.
- 초기 `left`, `top` 을 화면 밖 음수 값으로 설정하여 폼 로드 시 보이지 않게 한다.
- `level=1` 행을 추가하면 플라이아웃 서브 메뉴가 자동 구성된다.
- Menu와 달리 PopupMenu는 수평 바 없이 수직 목록만 표시된다.
