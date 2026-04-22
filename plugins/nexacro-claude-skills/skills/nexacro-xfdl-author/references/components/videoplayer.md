# VideoPlayer

**역할**: 폼 내에서 MP4 등 동영상을 재생하는 미디어 플레이어 컴포넌트. 재생/일시정지/정지 등 제어 메서드를 제공.
**샘플**: `sample_videoplayer_01.xfdl`, `sample_videoplayer_02.xfdl`

## 최소 구성

```xml
<VideoPlayer id="VideoPlayer00" taborder="0"
             left="32" top="40" width="540" height="320"
             showcontrolbar="true"
             url="https://example.com/movie.mp4"/>
```

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | 컴포넌트 고유 식별자 |
| `url` | | 재생할 동영상 URL (런타임에서도 변경 가능) |
| `showcontrolbar` | | 기본 컨트롤바 표시 여부 (`true` / `false`) |
| `mute` | | 음소거 여부 (`true` / `false`) |
| `currenttime` | | 현재 재생 위치 (밀리초 단위) |
| `duration` | | 동영상 전체 길이 (밀리초 단위, 읽기 전용) |

## 주요 메서드

| 메서드 | 서명 | 설명 |
|---|---|---|
| `play()` | `()` | 재생 시작 |
| `pause()` | `()` | 일시정지 |
| `stop()` | `()` | 정지 (위치 초기화) |

## 이벤트

| 이벤트 | 서명 | 설명 |
|---|---|---|
| `oncurrenttimechanged` | `(obj, e:nexacro.VideoCurrentTimeChangedEventInfo)` | 재생 위치 변경 시 발생 |
| `onplaystatuschanged` | `(obj, e)` | 재생 상태 변경 시 발생 |

## 주의점 / 팁

- `showcontrolbar="true"` 이면 컴포넌트 내장 컨트롤바가 표시됨. 커스텀 UI 구현 시 `false`로 설정하고 `play()` / `pause()` / `stop()` 직접 호출.
- `currenttime` 속성에 값을 직접 할당해 빠르기/되감기 구현 가능 (밀리초 단위).
- `mute` 속성을 런타임에서 토글하면 음소거/해제 전환.
- 재생 진행 시간 표시: `nexacro.round(currenttime / 1000)` 으로 초 단위로 변환.
- 지원 포맷은 실행 환경(브라우저/XClient)에 따라 다를 수 있음. MP4(H.264)가 가장 호환성이 높음.
- CORS 정책에 따라 외부 URL 동영상 재생이 제한될 수 있음.
