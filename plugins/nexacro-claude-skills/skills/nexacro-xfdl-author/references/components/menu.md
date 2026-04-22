# Menu

**역할**: Dataset에 바인딩되는 수평 메뉴 바. `<Menuitem>` 트리 없이 Dataset 컬럼으로 계층 구조를 정의한다.
**출처**: `sample_menu_01.xfdl`

## 최소 구성

`<Layout>` 안에 배치. 반드시 `<Dataset>` 과 함께 사용:

```xml
<Menu id="menuMain" taborder="0"
      left="0" top="0" width="600" height="39"
      captioncolumn="captioncolumn"
      idcolumn="idcolumn"
      levelcolumn="levelcolumn"
      enablecolumn="enablecolumn"
      checkboxcolumn="checkboxcolumn"
      userdatacolumn="userdatacolumn"
      onmenuclick="menuMain_onmenuclick"/>
```

### 동반 Dataset (필수)

```xml
<Dataset id="datasetMenu">
  <ColumnInfo>
    <Column id="captioncolumn"  type="STRING" size="256"/>
    <Column id="idcolumn"       type="STRING" size="256"/>
    <Column id="levelcolumn"    type="INT"    size="4"/>
    <Column id="enablecolumn"   type="STRING" size="256"/>
    <Column id="checkboxcolumn" type="STRING" size="256"/>
    <Column id="userdatacolumn" type="STRING" size="256"/>
  </ColumnInfo>
  <Rows>
    <!-- level=0: 최상위 메뉴 항목 -->
    <Row><Col id="captioncolumn">파일</Col><Col id="idcolumn">A</Col><Col id="levelcolumn">0</Col></Row>
    <!-- level=1: 서브 메뉴 항목 -->
    <Row><Col id="captioncolumn">열기</Col><Col id="idcolumn">A-1</Col><Col id="levelcolumn">1</Col></Row>
    <Row><Col id="captioncolumn">저장</Col><Col id="idcolumn">A-2</Col><Col id="levelcolumn">1</Col></Row>
    <Row><Col id="captioncolumn">편집</Col><Col id="idcolumn">B</Col><Col id="levelcolumn">0</Col></Row>
    <Row><Col id="captioncolumn">복사</Col><Col id="idcolumn">B-1</Col><Col id="levelcolumn">1</Col></Row>
  </Rows>
</Dataset>
```

## 계층 구조 규칙

```
level=0  → 수평 메뉴 바 항목 (루트)
level=1  → 드롭다운 서브 메뉴
level=2  → 2단계 서브 메뉴 (플라이아웃)
```

Dataset 행 순서가 메뉴 표시 순서이며, `levelcolumn` 값으로 계층 깊이를 결정한다.

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | 고유 컴포넌트 식별자 |
| `left` / `top` / `width` / `height` | ✓ | 위치 및 크기 |
| `captioncolumn` | ✓ | 메뉴 표시 텍스트 컬럼명 |
| `idcolumn` | ✓ | 메뉴 항목 고유 ID 컬럼명 |
| `levelcolumn` | ✓ | 계층 깊이 컬럼명 (0-based 정수) |
| `enablecolumn` | | 활성화 여부 컬럼명 |
| `checkboxcolumn` | | 체크박스 표시 컬럼명 |
| `iconcolumn` | | 아이콘 이미지 컬럼명 |
| `userdatacolumn` | | 사용자 데이터 컬럼명 |

## 이벤트

| 이벤트 | 서명 | 설명 |
|---|---|---|
| `onmenuclick` | `fn(obj:nexacro.Menu, e:nexacro.MenuClickEventInfo)` | 메뉴 항목 클릭 시 발생; `e.id`로 항목 ID 획득 |

## 주의점 / 팁

- `onmenuclick` 에서 `e.id` 값으로 클릭된 메뉴를 구분하여 처리한다.
- `checkboxcolumn` 값을 Dataset에서 동적으로 변경하면 체크 상태가 실시간 반영된다:
  ```javascript
  this.menuMain_onmenuclick = function(obj, e) {
      if (e.id == "A-1") {
          var row = this.datasetMenu.findRow("idcolumn", "A-1");
          this.datasetMenu.setColumn(row, "checkboxcolumn", true);
      }
  };
  ```
- Menu 컴포넌트는 별도의 `<Menuitem>` XML 태그를 사용하지 않고 Dataset 바인딩으로 구성된다.
