# Graphics

**역할**: SVG 유사 벡터 그래픽 컨테이너. 스크립트로 자식 도형 객체(Line, Rect, Ellipse, Text, Image 등)를 동적 추가하여 커스텀 다이어그램·차트를 렌더링.
**샘플**: `sample_graphics_01.xfdl` ~ `sample_graphics_03.xfdl`

## 최소 구성

XFDL 선언:

```xml
<Graphics id="Graphics00" taborder="0"
          left="30" top="30" width="300" height="300"
          border="1px solid black"/>
```

스크립트로 도형 추가 후 반드시 `redraw()` 호출:

```javascript
var objGLine = new nexacro.GraphicsLine();
this.Graphics00.addChild("GraphicsLine00", objGLine);
objGLine.x = 10;  objGLine.y = 10;
objGLine.x2 = 50; objGLine.y2 = 50;
objGLine.strokepen = "1px solid red";
this.Graphics00.redraw();
```

## 주요 속성 (Graphics 컨테이너)

| 속성 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | 컴포넌트 고유 식별자 |
| `left` / `top` | ✓ | 픽셀 단위 위치 |
| `width` / `height` | ✓ | 픽셀 단위 크기 |
| `border` | | 컨테이너 테두리 (예: `"1px solid black"`) |

## 자식 도형 클래스 및 주요 속성

| 클래스 | 주요 속성 |
|---|---|
| `nexacro.GraphicsLine` | `x`, `y`, `x2`, `y2`, `strokepen` |
| `nexacro.GraphicsRect` | `x`, `y`, `width`, `height`, `strokepen`, `fillcolor` |
| `nexacro.GraphicsEllipse` | `x`, `y`, `width`, `height`, `strokepen` |
| `nexacro.GraphicsText` | `x`, `y`, `text`, `color`, `font` |
| `nexacro.GraphicsImage` | `x`, `y`, `image` (URL 형식) |
| `nexacro.GraphicsGroup` | 여러 도형을 묶어 그룹 회전·이동 지원 |

## 이벤트

| 이벤트 | 설명 |
|---|---|
| `onclick` | 컨테이너 클릭 시 발생 |
| `ondrag` / `ondragmove` | 드래그 시작/이동 시 발생 |

## 주의점 / 팁

- 도형을 추가·변경한 후 반드시 `Graphics00.redraw()` 를 호출해야 화면에 반영됨.
- `addChild(id, obj)` 시 id는 유니크해야 함. 기존 id로 재등록 시 오류 발생.
- 도형 회전은 `GraphicsRect` 또는 `GraphicsGroup` 의 `rotate` 속성으로 제어.
- Graphics는 레이아웃 기반이 아닌 좌표(x, y) 기반 배치 — 일반 Layout 컴포넌트와 혼용 불가.
- 도형 수가 많을 때 성능 저하 가능. 불필요한 자식 객체는 `removeChild()` 로 정리.
