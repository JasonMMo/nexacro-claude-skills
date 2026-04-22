# ImageViewer

**역할**: 이미지를 화면에 표시하는 컴포넌트. `imagerc::` 리소스 또는 외부 URL 이미지를 렌더링하며, 비율 유지·맞춤·원본 크기 등 다양한 표시 모드를 지원한다.
**출처**: `sample_imageviewer_01.xfdl`, `sample_imageviewer_02.xfdl`, `sample_imageviewer_03.xfdl`

## 최소 구성

`<Layout>` 안에 배치:

```xml
<ImageViewer id="imgMain" taborder="0"
             left="30" top="30" width="320" height="480"
             image="URL(&quot;imagerc::sample_photo.jpg&quot;)"/>
```

## 주요 속성

| 속성 | 설명 |
|---|---|
| `image` | 표시할 이미지 경로. `URL("imagerc::파일명")` 또는 외부 URL 문자열 |
| `stretch` | 이미지 표시 방식: `fit`(전체 채움), `fixaspectratio`(비율 유지), `none`(원본 크기) |
| `fittocontents` | `both` / `width` / `height` — 이미지 크기에 맞게 컴포넌트 크기 자동 조정 |
| `imagewidth` | (읽기 전용) 로드된 이미지의 실제 너비(px) |
| `imageheight` | (읽기 전용) 로드된 이미지의 실제 높이(px) |

## 이벤트

| 이벤트 | 시그니처 | 설명 |
|---|---|---|
| `onload` | `(obj:nexacro.ImageViewer, e:nexacro.LoadEventInfo)` | 이미지 로드 완료 후 발생. `imagewidth`/`imageheight` 참조 가능 |

## 사용 API (스크립트)

```javascript
// imagerc 리소스 교체
this.imgMain.image = "imagerc::new_photo.png";

// 외부 URL 이미지
this.imgMain.image = "https://example.com/photo.jpg";

// 표시 모드 변경
this.imgMain.stretch = "fixaspectratio"; // 비율 유지
this.imgMain.stretch = "fit";            // 컴포넌트에 맞게 채움
this.imgMain.stretch = "none";           // 원본 크기 그대로

// 로드 후 실제 이미지 크기 확인
this.imgMain_onload = function(obj, e) {
    var info = obj.imagewidth + " x " + obj.imageheight;
    this.staticInfo.text = info;
};
```

## 주의점 / 팁

- `image` 속성에 `URL(...)` 래퍼는 XFDL XML 선언 시 필요하고, 스크립트에서 동적으로 변경할 때는 `"imagerc::파일명"` 문자열만 사용한다.
- `fittocontents="both"` 설정 시 이미지 로드 후 컴포넌트 크기가 자동으로 조정되므로, 레이아웃 기반 배치와 혼용 시 주의한다.
- 외부 URL 이미지는 네트워크 환경·보안 정책에 따라 로드 실패가 발생할 수 있으므로 `onload`에서 `imagewidth == 0` 조건으로 실패를 감지한다.
- `imagerc`는 프로젝트 리소스(이미지 리소스 파일)에 등록된 이미지를 참조하는 접두사다.
