# Tab

**역할**: 여러 `<Tabpage>` 자식을 탭 버튼으로 전환하는 탭 컨테이너 컴포넌트.
**출처**: `sample_tab_02.xfdl`

## 최소 구성

`<Layout>` 안에 배치. `<Tabpages>` 자식이 필수:

```xml
<Tab id="Tab00" taborder="0"
     left="20" top="60" width="540" height="300"
     tabindex="0">
  <Tabpages>
    <Tabpage id="Tabpage1" text="첫 번째 탭">
      <Layouts>
        <Layout>
          <Button id="btnTab1" text="버튼" left="10" top="10" width="80" height="30"/>
        </Layout>
      </Layouts>
    </Tabpage>
    <Tabpage id="Tabpage2" text="두 번째 탭">
      <Layouts>
        <Layout/>
      </Layouts>
    </Tabpage>
  </Tabpages>
</Tab>
```

## 자식 구조 — Tabpage 중첩

```
Tab
└── Tabpages
    ├── Tabpage (id, text)
    │   └── Layouts > Layout
    │       └── [자식 컴포넌트들]
    └── Tabpage (id, text)
        └── Layouts > Layout
            └── [자식 컴포넌트들]
```

각 `<Tabpage>` 는 독립적인 `<Layouts><Layout>` 을 가지며, 내부 컴포넌트 좌표는 Tab 왼쪽 상단 기준이다.

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | 고유 컴포넌트 식별자 |
| `taborder` | ✓ | 탭 포커스 순서 |
| `left` / `top` / `width` / `height` | ✓ | 위치 및 크기 (픽셀) |
| `tabindex` | | 현재 활성화된 탭 인덱스 (0-based) |
| `multiline` | | `true` 시 탭 버튼이 여러 줄로 표시 |
| `showextrabutton` | | `true` 시 탭 목록 화살표 버튼 표시 |

## 이벤트

| 이벤트 | 서명 | 설명 |
|---|---|---|
| `onchanged` | `fn(obj:nexacro.Tab, e:nexacro.TabEventInfo)` | 활성 탭이 변경된 후 발생; `e.tabpage`로 새 탭 접근 |
| `onchanging` | `fn(obj:nexacro.Tab, e:nexacro.TabEventInfo)` | 탭 전환 직전 발생; `e.preventDefault()`로 전환 취소 가능 |

## 주의점 / 팁

- 런타임에 탭 추가: `Tab00.insertTabpage("newId", -1)` (-1 = 마지막에 추가).
- 탭 수 조회: `Tab00.getTabpageCount()`.
- 자식 컴포넌트 접근: `this.Tab00.Tabpage1.Button00`.
- `tabindex` 를 스크립트에서 변경하면 탭이 전환되며 `onchanged` 이벤트가 발생한다.
- `multiline="true"` 이면 탭이 많을 때 줄바꿈되어 표시되므로 높이를 충분히 확보한다.
