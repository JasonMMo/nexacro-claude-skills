# WebBrowser

**역할**: 폼 내에 HTML 페이지를 인라인으로 표시하는 임베디드 브라우저 컴포넌트 (iframe 유사).
**샘플**: `sample_webbrowser_01.xfdl` ~ `sample_webbrowser_09.xfdl`

## 최소 구성

```xml
<WebBrowser id="WebBrowser00" taborder="0"
            left="32" top="40" width="540" height="320"
            url="http://example.com"
            onusernotify="WebBrowser00_onusernotify"/>
```

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | 컴포넌트 고유 식별자 |
| `url` | | 초기 로드할 URL (런타임에서도 변경 가능) |
| `left` / `top` | ✓ | 픽셀 단위 위치 |
| `width` / `height` | ✓ | 픽셀 단위 크기 |
| `onusernotify` | | HTML 페이지에서 nexacro로 메시지 전달 시 발생 |

## 주요 메서드

| 메서드 | 서명 | 설명 |
|---|---|---|
| `navigate(url)` | `(string)` | 지정 URL로 이동 |
| `getProperty(name)` | `(string) → object` | 내부 DOM 객체 속성 취득 |
| `postData(url, data)` | `(string, string)` | POST 방식으로 데이터 전송 후 이동 |

## 이벤트

| 이벤트 | 서명 | 설명 |
|---|---|---|
| `onusernotify` | `(obj, e:nexacro.UserNotifyEventInfo)` | HTML에서 `nexacro.userNotify()` 호출 시 수신 |
| `onload` | `(obj, e:nexacro.LoadEventInfo)` | URL 로드 완료 시 발생 |

## 주의점 / 팁

- `url` 속성은 선언 시 또는 `onload` 스크립트에서 동적으로 지정 가능.
- HTML 내부 DOM 접근은 `getProperty("document")` → `callMethod("getElementById", ...)` 체이닝으로 처리.
- 사용 후 DOM 객체는 반드시 `destroy()` 호출로 해제할 것 (메모리 누수 방지).
- 크로스 도메인 HTML 접근은 브라우저 보안 정책에 따라 제한될 수 있음.
- 모바일 환경에서 렌더링 결과가 데스크톱과 다를 수 있음.
