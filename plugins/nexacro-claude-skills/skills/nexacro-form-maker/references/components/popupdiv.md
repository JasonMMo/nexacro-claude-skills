# PopupDiv

**역할**: `trackPopupByComponent` API로 표시/숨김을 제어하는 플로팅 Div 컨테이너. 커스텀 팝업 UI에 사용한다.
**출처**: `sample_popupdiv_02.xfdl`

## 최소 구성

`<Layout>` 안에 배치. 초기 `visible="false"` 권장:

```xml
<PopupDiv id="PopupDiv00"
          left="218" top="46" width="200" height="200"
          visible="false"
          background="white">
  <Layouts>
    <Layout>
      <!-- 팝업 내부 컴포넌트 -->
      <Button id="btnClose" text="닫기" left="10" top="10" width="80" height="30"
              onclick="btnClose_onclick"/>
    </Layout>
  </Layouts>
</PopupDiv>
```

### trackPopupByComponent 호출 패턴

```javascript
// 버튼 클릭 시 버튼 아래에 팝업 표시
this.Button00_onclick = function(obj, e) {
    this.PopupDiv00.trackPopupByComponent(obj,
        obj.getOffsetWidth(),      // x 오프셋: 버튼 오른쪽
        obj.getOffsetHeight(),     // y 오프셋: 버튼 아래
        160, 240);                 // 팝업 width, height
};

// 팝업 닫기
this.btnClose_onclick = function(obj, e) {
    this.parent.PopupDiv00.closePopup();
};
```

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | 고유 컴포넌트 식별자 |
| `left` / `top` / `width` / `height` | ✓ | 기본 크기 (실제 위치는 trackPopup API가 결정) |
| `visible` | | 초기 표시 여부 (보통 `false`) |
| `background` | | 팝업 배경색 |
| `text` | | 팝업 테두리에 표시할 선택적 레이블 |

## 이벤트

| 이벤트 | 서명 | 설명 |
|---|---|---|
| `onload` | `fn(obj:nexacro.PopupDiv, e:nexacro.EventInfo)` | PopupDiv가 로드될 때 발생 |
| `onpopupclose` | `fn(obj:nexacro.PopupDiv, e:nexacro.EventInfo)` | 팝업이 닫힐 때 발생 |

## 주의점 / 팁

- `trackPopupByComponent(anchorComp, offsetX, offsetY, popupWidth, popupHeight)` — anchorComp 기준으로 팝업 위치를 자동 계산한다.
- 자식 컴포넌트에서 팝업을 닫으려면 `this.parent.closePopup()` 또는 `this.popupdiv.closePopup()` 을 호출한다.
- Div와 달리 PopupDiv는 다른 컴포넌트 위에 플로팅되므로 z-order 처리가 자동으로 된다.
- `url` 속성으로 외부 xfdl을 서브폼으로 로드할 수도 있다 (Div와 동일한 패턴).
- 팝업 외부 클릭 시 자동으로 `closePopup` 이 호출된다.
