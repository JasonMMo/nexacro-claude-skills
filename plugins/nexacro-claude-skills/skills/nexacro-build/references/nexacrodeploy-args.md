# nexacrodeploy.exe 아규먼트 레퍼런스

> 출처: 넥사크로 N V24 개발도구 가이드 24.0.0.1000

## 기본 실행 형식

```
nexacrodeploy.exe -P [ARG] -O [ARG] -B [ARG] -GENERATERULE [ARG] [추가옵션...]
```

---

## 필수 옵션 (4개 모두 필수)

| 옵션 | 설명 |
|------|------|
| `-P [경로]` | 프로젝트 `.xprj` 파일 경로 |
| `-O [경로]` | Generate 결과물 저장 경로 (없으면 자동 생성) |
| `-B [경로]` | nexacrolib 라이브러리 경로 |
| `-GENERATERULE [경로]` | Generate Rule 파일 경로 (SDK > {버전} > generate 폴더) |

---

## 작업 대상 선택 옵션 (미지정 시 전체 대상)

| 옵션 | 설명 |
|------|------|
| `-FILE "[경로목록]"` | 특정 xfdl 파일만 빌드. 형식: `"'a.xfdl','b.xfdl'"` (공백 없이) |
| `-SERVICE [ID목록]` | 특정 서비스 prefix ID만 빌드. 복수 시 콤마 구분 |
| `-BOOTSTRAP [OS]` | Bootstrap 파일만 생성. Android, iOS 등 |
| `-MODULE` | Module 파일만 Generate |

---

## Generate 옵션

| 옵션 | 설명 |
|------|------|
| `-REGENERATE` | 수정 여부 무관하게 모든 파일 강제 재Generate |
| `-BROWSER [목록]` | 특정 브라우저용 파일만 생성. ex: `"NRE,Chrome"` (공백 없이) |
| `-JSVERSION` | 스크립트 검증 규칙. 기본값: ECMAScript 2015 |
| `-DEFER` | Bootstrap의 Script 태그에 defer 속성 추가 |
| `-SPLASH` | Bootstrap에 Splash Loader 스크립트 포함 |
| `-RTL` | RTL 적용 결과 파일 포함 |
| `-UNARCHIVE [OS]` | Run.zip 대신 Run.html 생성. Android, iOS |

### -BROWSER 지정 가능 값
`NRE`, `Chrome`, `Firefox`, `Opera`, `Safari`
(IE 10/11은 24.0.0.100 이후 라이브러리에서 미지원)

---

## Deploy 옵션

| 옵션 | 설명 |
|------|------|
| `-D [경로]` | Deploy 결과물 경로. `-O` 경로와 **달라야 함** |
| `-MERGE` | JSON Module의 여러 JS 파일을 하나로 병합 |
| `-MERGEXCSS` | 여러 xcss 파일을 하나로 병합 |
| `-COMPRESS` | JS 파일 압축 (주석·공백 제거, 1줄 코드) |
| `-SHRINK` | 변수명 난독화 (`-COMPRESS`와 함께 사용) |
| `-IGNORECOMPRESS [경로]` | 압축 제외 파일 목록 (`.ignorecompress`). `-COMPRESS` 필요 |
| `-IGNOREEVAL` | eval 함수 무관하게 난독화 (`-SHRINK` 필요, 비권장) |
| `-COMPILE` | NRE 전용 암호화 파일로 변환 (NRE에서만 실행 가능) |
| `-PRJURL [URL]` | App Load URL 지정 (iOS/iPad 전용) |

---

## 기타 옵션

| 옵션 | 설명 |
|------|------|
| `-L [경로]` | 로그 파일 저장 경로 (없으면 자동 생성) |
| `-H` / `-?` / `-HELP` | 도움말 출력 |

---

## 주요 사용 예제

### 전체 Generate
```
nexacrodeploy.exe -P "C:\proj\proj.xprj" -O "E:\output" -B "C:\proj\nexacrolib" -GENERATERULE "C:\proj\generate"
```

### 특정 파일만 Generate
```
nexacrodeploy.exe -P "C:\proj\proj.xprj" -O "E:\output" -B "C:\proj\nexacrolib" -GENERATERULE "C:\proj\generate" -FILE "'C:\proj\aa.xfdl','C:\proj\bb.xfdl'"
```

### Generate + Spring 서버로 Deploy
```
nexacrodeploy.exe -P "C:\proj\proj.xprj" -O "E:\output" -B "C:\proj\nexacrolib" -GENERATERULE "C:\proj\generate" -D "C:\spring-app\src\main\webapp\resource"
```

### Generate + Deploy + 압축 + 난독화
```
nexacrodeploy.exe -P "C:\proj\proj.xprj" -O "E:\output" -B "C:\proj\nexacrolib" -GENERATERULE "C:\proj\generate" -D "C:\spring-app\src\main\webapp\resource" -COMPRESS -SHRINK
```

### 로그 저장 포함
```
nexacrodeploy.exe -P "C:\proj\proj.xprj" -O "E:\output" -B "C:\proj\nexacrolib" -GENERATERULE "C:\proj\generate" -L "C:\logs\build.txt"
```
