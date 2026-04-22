# Sketch

**역할**: 사용자가 마우스(또는 터치)로 자유롭게 그림을 그릴 수 있는 캔버스형 드로잉 컴포넌트.
**샘플**: `sample_sketch_01.xfdl`

## 최소 구성

```xml
<Sketch id="sketchMain" taborder="0"
        left="16" top="25" width="289" height="127"/>
```

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | 컴포넌트 고유 식별자 |
| `left` / `top` | ✓ | 픽셀 단위 위치 |
| `width` / `height` | ✓ | 픽셀 단위 크기 |
| `pencolor` | | 펜 색상 (예: `"Black"`, `"Red"`) |
| `pensize` | | 펜 굵기 (픽셀 단위 정수) |

## 주요 메서드

| 메서드 | 서명 | 설명 |
|---|---|---|
| `clear()` | `()` | 드로잉 영역 전체 초기화 |
| `getImageData()` | `() → string` | 현재 그림을 Base64 인코딩 이미지로 반환 |
| `setImageData(data)` | `(string)` | Base64 이미지 데이터를 Sketch에 로드 |

## 이벤트

| 이벤트 | 설명 |
|---|---|
| `ondrawend` | 한 획(stroke) 그리기 완료 시 발생 |

## 주의점 / 팁

- 색상(`pencolor`)과 굵기(`pensize`)는 Combo/Radio 컴포넌트와 연동해 런타임에서 동적으로 변경 가능.
- 샘플(`sample_sketch_01.xfdl`)에서 Color Combo와 Size Radio를 통해 펜 속성을 제어하는 패턴 참조.
- `getImageData()` / `setImageData()` 를 이용해 서버에 서명 이미지 등을 저장/복원할 수 있음.
- 펜 모드 외에 지우개 모드(`none`) 지원 — 샘플의 Radio 컴포넌트에서 `stroke` / `none` 값으로 전환.
- 터치 디바이스에서 손가락 드로잉이 지원되나 정밀도는 기기에 따라 다름.
