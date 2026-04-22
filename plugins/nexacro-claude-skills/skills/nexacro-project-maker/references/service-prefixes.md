# 서비스 Prefix 매핑 (`typedefinition.xml` / `<Services>`)

Nexacro 는 `formurl="Base::main.xfdl"` 처럼 **prefix** 를 사용해 리소스를 참조합니다. 이 prefix 가 실제 URL 로 어떻게 풀리는지 결정하는 곳이 `<Services>` 섹션입니다.

## 기본 샘플

```xml
<Services>
  <Service prefixid="theme"    type="resource" url="./_resource_/_theme_/"    include_subdir="true"/>
  <Service prefixid="imagerc"  type="resource" url="./_resource_/_images_/"   include_subdir="true"/>
  <Service prefixid="xcssrc"   type="resource" url="./_resource_/_xcss_/"     include_subdir="false"/>
  <Service prefixid="font"     type="resource" url="./_resource_/_font_/"     include_subdir="false"/>
  <Service prefixid="Base"     type="form"     url="./Base/"                  cachelevel="session" include_subdir="false"/>
  <Service prefixid="Sample"   type="form"     url="./Sample/"                cachelevel="session" include_subdir="false"/>
  <Service prefixid="SvcGet"   type="file"     url="./Service/"               cachelevel="session" include_subdir="true"/>
</Services>
```

## `type` 값 세 가지

| type | 의미 | 사용 예 |
|---|---|---|
| `resource` | 정적 자산 (테마/이미지/CSS/폰트) | `imagerc::logo.png`, `theme::default.zip` |
| `form` | xfdl 폼 파일 | `Base::main.xfdl`, `Sample::customer_list.xfdl` |
| `file` | 기타 파일 (서버 API 경로 포함 가능) | `SvcGet::data.json` |

## 핵심 속성

| 속성 | 설명 |
|---|---|
| `prefixid` | xfdl/script 안에서 참조할 prefix. `prefixid::subpath/file.ext` 형식으로 사용 |
| `url` | 실제 URL. 상대 경로는 애플리케이션 배포 루트 기준 |
| `include_subdir` | `true` 면 하위 디렉터리 탐색 허용. Studio 의 폼 탐색 트리에도 영향 |
| `cachelevel` | `none` / `session` / `permanent`. 폼/파일 캐싱 전략 |
| `version` / `communicationversion` | 캐시 무효화 플래그 (숫자 올리면 강제 재다운로드) |

## 자주 쓰는 prefix 관례

| prefix | 통상 매핑 | 설명 |
|---|---|---|
| `theme::` | `./_resource_/_theme_/` | 테마 자산 |
| `imagerc::` | `./_resource_/_images_/` | 이미지 |
| `xcssrc::` | `./_resource_/_xcss_/` | xcss 스타일시트 |
| `font::` | `./_resource_/_font_/` | xfont 파일 |
| `Base::` | `./Base/` | 기동/공통 폼 위치 관례 |
| `frame::` | `./frame/` | packageN 스타일 xadl 의 MainFrame / leftFrame 구성요소 위치 (→ `xadl-frame-patterns.md`) |
| `<업무ID>::` | `./<업무ID>/` | 업무 모듈별 폼 디렉터리 (예: `Sample::`, `Order::`, `HR::`) |

## 주의점

- **prefix 없이 쓰면 로딩 실패**. 순수 상대 경로 `./main.xfdl` 은 안 됨. 반드시 `Base::main.xfdl`.
- **prefix 와 디렉터리명을 일치시키는 것이 관례** 이지만 필수는 아님. `prefixid="Customer"` + `url="./Cust/"` 가능 — 다만 팀 컨벤션 깨므로 비권장.
- **대소문자 구분**. `base::` 와 `Base::` 는 다름.
- **업무 모듈 추가 순서**:
  1. `typedefinition.xml` 의 `<Services>` 에 `<Service prefixid="NewModule" type="form" url="./NewModule/" .../>` 추가
  2. 동일 이름 디렉터리 `./NewModule/` 생성
  3. 안에 xfdl 파일 배치 → `NewModule::foo.xfdl` 로 참조 가능

## 디버깅 팁

- 런타임 "form not found" 에러 → prefix 오타 / 서비스 미등록 / 디렉터리 누락 3가지 중 하나.
- Studio 가 로드 실패하면 `typedefinition.xml` 을 Studio 에서 저장 (재빌드 트리거) 후 프로젝트 재오픈.
- 캐싱 문제 의심 시 `version` / `communicationversion` 숫자를 +1 하거나 브라우저 캐시 초기화.
