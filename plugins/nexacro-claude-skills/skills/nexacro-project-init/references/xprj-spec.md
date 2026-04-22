# `.xprj` 엘리먼트 레퍼런스

Nexacro Studio 프로젝트의 **엔트리 파일**. Studio 는 이 파일을 열어 전체 워크스페이스를 구성합니다.

## 전체 샘플

```xml
<?xml version="1.0" encoding="utf-8"?>
<Project version="2.1" nexacrosdk="Latest Version" sdkversion="24.0.0">
  <EnvironmentDefinition url="environment.xml"/>
  <TypeDefinition url="typedefinition.xml"/>
  <AppVariables url="appvariables.xml"/>
  <AppInfos>
    <AppInfo url="MyApp.xadl"/>
  </AppInfos>
  <BootstrapCustomize url="bootstrap.xml"/>
</Project>
```

## 엘리먼트

| 엘리먼트 | 필수 | 설명 |
|---|---|---|
| `<Project>` | ✓ | 루트. `version` / `sdkversion` / `nexacrosdk` 속성 |
| `<EnvironmentDefinition>` | ✓ | `environment.xml` 경로. 테마 / 스크린 / 쿠키 정의 |
| `<TypeDefinition>` | ✓ | `typedefinition.xml` 경로. 컴포넌트 모듈 / 서비스 prefix |
| `<AppVariables>` | ✓ | `appvariables.xml` 경로. 전역 변수 / Dataset |
| `<AppInfos>` | ✓ | `<AppInfo>` 목록. 다중 Application 지원 |
| `<AppInfo>` | ✓ | 개별 `.xadl` 파일 참조. 단일 .xprj 가 여러 xadl 을 가질 수 있음 |
| `<BootstrapCustomize>` | 선택 | `bootstrap.xml` 경로. HTML 로더 템플릿 커스터마이즈 |

## 속성

| 속성 | 값 | 의미 |
|---|---|---|
| `version` | `2.1` | Studio 프로젝트 포맷 버전 (고정) |
| `nexacrosdk` | `Latest Version` / 고정 버전 | Studio 내 SDK 선택 |
| `sdkversion` | `24.0.0` | 실제 SDK 버전 (빌드 타임 참조) |

## 주의점

- **경로는 `.xprj` 파일 기준 상대경로**. 절대경로 / `..` 는 Studio 가 경고.
- `sdkversion` 이 설치본과 불일치하면 Studio 가 호환 프롬프트를 띄움.
- `<AppInfos>` 는 배열이지만 일반적으로 xadl 은 1개. 복수 xadl 구성은 다중 애플리케이션 진입점이 필요한 경우 (예: 관리자/사용자 분리 앱).
