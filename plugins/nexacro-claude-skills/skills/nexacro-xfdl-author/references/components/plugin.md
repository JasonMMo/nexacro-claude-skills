# Plugin

**역할**: 외부 플러그인(ActiveX 또는 네이티브 모듈)을 폼에 삽입하는 레거시 컨테이너 컴포넌트.
**샘플**: 샘플 없음 — 공식 매뉴얼 참조 (https://docs.tobesoft.com/nexacro_n_v24_ko)

## 최소 구성

```xml
<Plugin id="Plugin00" taborder="0"
        left="32" top="40" width="400" height="300"
        classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"
        src="movie.swf"/>
```

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | 컴포넌트 고유 식별자 |
| `classid` | ✓ | ActiveX 또는 플러그인 클래스 ID (CLSID 형식) |
| `src` | | 플러그인에 전달할 소스 파일 경로 |
| `left` / `top` | ✓ | 픽셀 단위 위치 |
| `width` / `height` | ✓ | 픽셀 단위 크기 |

## 이벤트

| 이벤트 | 설명 |
|---|---|
| `onload` | 플러그인 로드 완료 시 발생 |

## 주의점 / 팁

- Plugin 컴포넌트는 ActiveX 기반 레거시 기술을 위한 것으로, 웹 환경에서는 동작하지 않음.
- 브라우저 보안 정책으로 인해 현대 브라우저에서 ActiveX 플러그인은 대부분 차단됨.
- 신규 개발에는 사용하지 말 것. WebBrowser 또는 네이티브 Nexacro N 컴포넌트 사용 권장.
- Nexacro N v24 데스크톱 앱(XClient) 환경에서만 동작 가능.
