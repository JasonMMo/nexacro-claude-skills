# GoogleMap

**역할**: Google Maps API를 이용해 지도를 폼에 임베드하고, 마커 추가·삭제·이벤트 처리를 지원하는 컴포넌트.
**샘플**: `sample_googlemap_01.xfdl` ~ `sample_googlemap_04.xfdl`

## 최소 구성

```xml
<GoogleMap id="GoogleMap00" taborder="0"
           left="170" top="40" width="480" height="320"
           onload="GoogleMap00_onload"
           onerror="GoogleMap00_onerror"/>
```

런타임에서 `load()` 호출로 지도를 표시:

```javascript
this.GoogleMap00.apikey = nexacro.getApplication().googleMapAPIKey;
this.GoogleMap00.showzoom = true;
// load(hybrid, latitude, longitude, maptype, zoom)
this.GoogleMap00.load(false, 37.5665, 126.9780, 0, 13);
```

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | 컴포넌트 고유 식별자 |
| `apikey` | ✓ | Google Maps API 키 (보통 `appvariables.xml`의 `googleMapAPIKey` 참조) |
| `showzoom` | | 줌 컨트롤 표시 여부 (`true` / `false`) |
| `left` / `top` | ✓ | 픽셀 단위 위치 |
| `width` / `height` | ✓ | 픽셀 단위 크기 |

## 주요 메서드

| 메서드 | 서명 | 설명 |
|---|---|---|
| `load(hybrid, lat, lng, maptype, zoom)` | `(bool, number, number, int, int)` | 지도 로드 및 초기 위치 설정 |
| `addItem(id, marker)` | `(string, GoogleMapMarker)` | 마커 추가 |
| `removeItem(id)` | `(string)` | 마커 제거 |

## 이벤트

| 이벤트 | 서명 | 설명 |
|---|---|---|
| `onload` | `(obj, e:nexacro.GoogleMapEventInfo)` | 지도 로드 완료 시 발생 |
| `onerror` | `(obj, e:nexacro.GoogleMapErrorEventInfo)` | 로드 오류 시 발생; `e.errormsg` 확인 |
| `onrecvsuccess` | `(obj, e)` | 지오코딩 등 요청 성공 시 발생 |

## 주의점 / 팁

- API 키는 XFDL에 직접 하드코딩하지 말 것. `appvariables.xml`에 `googleMapAPIKey` 변수로 선언하고 `nexacro.getApplication().googleMapAPIKey`로 참조.
- `load()` 는 `apikey` 속성 설정 후 호출해야 함. `onload` 이벤트 전에는 마커 조작 불가.
- `nexacro.GoogleMapMarker()` 객체 생성 후 `latitude`, `longitude`, `text`, `draggable` 속성 설정, `addItem()`으로 추가.
- 인터넷 연결이 필수. 오프라인 환경에서는 `onerror` 이벤트로 실패 처리 필요.
- Google Maps API 이용 약관 및 사용량 제한(쿼터) 주의.
