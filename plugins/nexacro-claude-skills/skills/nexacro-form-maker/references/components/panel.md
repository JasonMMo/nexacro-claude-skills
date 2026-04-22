# Panel

**역할**: `<PanelItem>` 으로 자식 컴포넌트의 레이아웃 순서를 선언하는 경량 컨테이너. Div의 `horizontal` 레이아웃 안에서 특히 유용하다.
**출처**: `sample_panel_01.xfdl`

## 최소 구성

`<Layout>` 안에 배치. `<Contents>` 의 `<PanelItem>` 이 자식 컴포넌트 참조를 정의:

```xml
<Div id="Div00" left="50" top="50" width="442" height="42" border="1px solid black">
  <Layouts>
    <Layout type="horizontal" flexwrap="wrap" verticalgap="5">

      <Panel id="Panel00" left="1" top="1" width="220" height="40">
        <Contents>
          <PanelItem id="PanelItem00" componentid="Static00"/>
          <PanelItem id="PanelItem01" componentid="Edit00"/>
        </Contents>
      </Panel>
      <Static id="Static00" text="First Name"
              left="0" top="0" width="100" height="40" textAlign="center"/>
      <Edit id="Edit00"
            left="0" top="0" width="120" height="40"/>

    </Layout>
  </Layouts>
</Div>
```

## 자식 구조 — PanelItem 참조

```
Panel
└── Contents
    ├── PanelItem (componentid="Static00")   ← 실제 컴포넌트는 Panel 외부에 선언
    └── PanelItem (componentid="Edit00")
```

`<PanelItem componentid>` 는 동일 `<Layout>` 안의 컴포넌트 `id`를 참조한다.
Panel 자체는 크기와 순서만 정의하고 컴포넌트를 직접 소유하지 않는다.

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | 고유 컴포넌트 식별자 |
| `taborder` | ✓ | 탭 포커스 순서 |
| `left` / `top` / `width` / `height` | ✓ | 위치 및 크기 (픽셀) |

### PanelItem 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | PanelItem 식별자 |
| `componentid` | ✓ | 참조할 컴포넌트의 `id` |

## 이벤트

Panel 컴포넌트 자체에 별도 이벤트는 없다. 이벤트는 `<PanelItem>` 이 참조하는 각 자식 컴포넌트에서 처리한다.

## 주의점 / 팁

- Panel은 주로 부모 `<Layout type="horizontal">` 안에서 여러 컴포넌트를 하나의 묶음으로 취급할 때 사용한다.
- `PanelItem` 의 `componentid` 는 동일 `<Layout>` 에 있는 컴포넌트여야 한다.
- Panel 내부에 `<Layouts>` 블록이 없다는 점이 Div와 다르다 — 자식 컴포넌트는 여전히 외부 Layout에 선언된다.
- 부모 Div가 `fittocontents="height"` 로 설정되면 Panel 묶음 기준으로 높이가 자동 조정된다.
- 단순 시각적 컨테이너만 필요하다면 `Div`, 레이아웃 그룹핑이 목적이면 `Panel`을 선택한다.
