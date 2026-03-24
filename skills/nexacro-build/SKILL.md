---
name: nexacro-build
description: Nexacro 프로젝트의 xfdl 소스를 빌드(Generate/Deploy)하는 작업을 자동화합니다. 사용자가 "nexacro 빌드", "xfdl 빌드", "nexacrodeploy 실행", "generate 해줘", "deploy 해줘", "넥사크로 빌드" 등을 언급할 때 반드시 이 skill을 사용하세요. nexacrodeploy.exe 또는 Nexacro Deploy JAVA(start.bat/start.sh)를 사용하는 모든 빌드/배포 작업에 적용합니다.
---

# Nexacro Build Skill

넥사크로 프로젝트의 xfdl 소스 파일을 nexacrodeploy.exe로 빌드(Generate/Deploy)하는 작업을 자동화하는 skill입니다.

## 개요

- **입력**: `.xfdl` 파일 (Nexacro Studio에서 작성한 XML 형식 소스)
- **빌드 도구**: `nexacrodeploy.exe` (Windows)
- **출력**: `.xjs` 파일 (JavaScript 형식)
- **설정 파일**: `{Base Path}build-config.json` (최초 1회 자동 생성, 이후 재사용)

## 경로 규칙 (중요)

Claude Code는 skill 실행 시 이 SKILL.md 앞에 아래 형식으로 Base Path를 자동으로 제공합니다.

```
Base Path: C:\Users\username\.claude\skills\nexacro-build\
```

모든 파일 접근은 이 Base Path 기준 절대 경로를 사용합니다. 상대 경로나 `~` 는 사용하지 마세요.

| 파일 | 절대 경로 |
|------|-----------|
| `build-config-info.json` | `{Base Path}assets/build-config-info.json` |
| `build-config.json` | `{Base Path}build-config.json` |

---

## Step 1: build-config.json 로드 또는 자동 탐지

### 1-1. build-config.json 존재 여부 확인

```bash
# Base Path의 실제 절대 경로를 사용해서 확인
test -f "{Base Path}build-config.json" && echo EXISTS || echo NOT_FOUND
```

파일이 있으면 → **Step 1-2**
파일이 없으면 → **Step 1-3 자동 탐지**

---

### 1-2. 기존 설정 로드 (build-config.json 있는 경우)

`{Base Path}build-config.json`을 읽어 사용자에게 보여주고 확인합니다.

```
📋 저장된 빌드 설정을 불러왔습니다.
─────────────────────────────────────────────────────────
nexacrodeploy.exe : C:\Program Files\TOBESOFT\Nexacro N\Tools\nexacrodeploy.exe
프로젝트 (.xprj) : C:\dev\MyProject\src\main\nxui\PackageN\PackageN.xprj
출력 경로  (-O)  : C:\dev\MyProject\src\main\resources\static\PackageN\
라이브러리 (-B)  : C:\dev\MyProject\src\main\nxui\PackageN\nexacrolib
GenerateRule     : C:\Program Files\TOBESOFT\Nexacro N\SDK\24.0.0\generate
배포 경로  (-D)  : (미설정)
─────────────────────────────────────────────────────────
이 설정으로 진행할까요? 수정이 필요하면 말씀해 주세요.
```

확인 후 → **Step 2로**

---

### 1-3. 프로젝트 자동 탐지 (build-config.json 없는 경우)

항목별로 사용자에게 묻지 않습니다. 아래 순서대로 프로젝트를 직접 탐색하여 설정을 자동 구성합니다.

#### (A) nexacrodeploy.exe 탐지

고정 후보 경로를 순서대로 확인합니다.

```bash
test -f "C:\Program Files\TOBESOFT\Nexacro N\Tools\nexacrodeploy.exe" && echo FOUND
test -f "C:\Program Files (x86)\TOBESOFT\Nexacro N\Tools\nexacrodeploy.exe" && echo FOUND
where nexacrodeploy.exe 2>nul
```

#### (B) xprj 파일 탐지

현재 작업 디렉터리(Spring 프로젝트 루트)의 `src/main/` 하위에서 `*.xprj`를 검색합니다.

```bash
dir /s /b "src\main\*.xprj" 2>nul
```

결과에 따라 처리합니다.

- **1개** → 자동 확정
- **여러 개** → 목록을 보여주고 선택 요청 (이 경우만 질문 허용)

  ```
  📂 nexacro 프로젝트가 여러 개 발견됐습니다. 빌드할 프로젝트를 선택해 주세요.

  [1] src\main\nxui\PackageA\PackageA.xprj
  [2] src\main\nxui\PackageB\PackageB.xprj
  [3] 전체 순서대로 빌드
  ```

- **0개** → xprj 파일 경로 직접 입력 요청

#### (C) baselib_path 탐지

xprj 파일이 위치한 폴더 기준으로 `./nexacrolib` 존재를 확인합니다.

```bash
# xprj가 src\main\nxui\PackageN\PackageN.xprj 이면
test -d "src\main\nxui\PackageN\nexacrolib" && echo FOUND
```

#### (D) output_path 추론

xprj 파일명(확장자 제외)을 폴더명으로 사용합니다.
Spring Boot / Spring MVC를 자동 판별하여 경로를 결정합니다.

```bash
# Spring Boot: src/main/resources/static/ 존재 시
test -d "src\main\resources\static" && echo SPRING_BOOT

# Spring MVC: src/main/webapp/ 존재 시
test -d "src\main\webapp" && echo SPRING_MVC
```

| 프레임워크 | output_path |
|-----------|-------------|
| Spring Boot | `{프로젝트루트}\src\main\resources\static\{xprj명}\` |
| Spring MVC  | `{프로젝트루트}\src\main\webapp\{xprj명}\` |

#### (E) generaterule_path 탐지

SDK 설치 경로에서 `generate` 폴더를 검색합니다. 여러 버전이 있으면 가장 높은 버전을 선택합니다.

```bash
dir /s /b "C:\Program Files\TOBESOFT\Nexacro N\SDK\*\generate" 2>nul
```

---

### 1-4. 탐지 결과 제안 — 확인 1회로 완료

탐지가 완료되면 결과를 한 번에 보여주고 **확인 1회**만 받습니다.
탐지에 실패한 항목은 `❌ 미탐지`로 표시하고 해당 항목만 입력 요청합니다.

```
🔍 프로젝트를 분석했습니다. 아래 설정으로 진행할까요?
─────────────────────────────────────────────────────────
nexacrodeploy.exe : C:\Program Files\TOBESOFT\Nexacro N\Tools\nexacrodeploy.exe   ✅ 자동탐지
프로젝트 (.xprj) : C:\dev\MyProject\src\main\nxui\PackageN\PackageN.xprj         ✅ 자동탐지
출력 경로  (-O)  : C:\dev\MyProject\src\main\resources\static\PackageN\           ✅ Spring Boot
라이브러리 (-B)  : C:\dev\MyProject\src\main\nxui\PackageN\nexacrolib             ✅ 자동탐지
GenerateRule     : C:\Program Files\TOBESOFT\Nexacro N\SDK\24.0.0\generate        ✅ 자동탐지
배포 경로  (-D)  : (미설정 — 필요하면 말씀해 주세요)
─────────────────────────────────────────────────────────
진행할까요? 수정이 필요한 항목이 있으면 말씀해 주세요.
```

사용자가 확인하면 `{Base Path}build-config.json`에 저장 후 → **Step 2로**

---

### 1-5. 설정 변경 요청 처리

사용자가 "경로 바꿔줘", "output 경로 수정" 등을 요청하면 해당 항목만 재질문하고 `{Base Path}build-config.json`을 업데이트합니다.

---

## Step 2: 빌드 모드 결정

사용자 요청을 분석하여 아래 중 어떤 모드인지 판단합니다.

### 모드 A: Generate만 수행 (기본)

xfdl → xjs 변환만 수행합니다.

```
nexacrodeploy.exe -P [XPRJ] -O [OUTPUT] -B [BASELIB] -GENERATERULE [RULE]
```

### 모드 B: Generate + Deploy

Generate 후 `-D` 경로로 바로 복사합니다.

```
nexacrodeploy.exe -P [XPRJ] -O [OUTPUT] -B [BASELIB] -GENERATERULE [RULE] -D [DEPLOY_PATH]
```

> ⚠️ `-D` 경로는 `-O` 경로와 **반드시 달라야** 합니다.

### 모드 C: 특정 파일만 빌드

```
nexacrodeploy.exe -P [XPRJ] -O [OUTPUT] -B [BASELIB] -GENERATERULE [RULE] -FILE "'C:\path\a.xfdl','C:\path\b.xfdl'"
```

> ⚠️ 전체를 `"`(큰따옴표), 각 파일은 `'`(작은따옴표)로 감쌉니다. 항목 사이 **공백 없이** 콤마 구분.

### 모드 D: 여러 xprj 전체 빌드 (복수 프로젝트인 경우)

Step 1-3(B)에서 "전체 순서대로 빌드"를 선택한 경우, 탐지된 xprj 목록을 순서대로 반복 실행합니다.
각 프로젝트의 output_path는 xprj명 기준으로 각각 추론합니다.

---

## Step 3: 추가 옵션 처리

| 옵션 | 언제 추가하나 |
|------|--------------|
| `-REGENERATE` | "전체 다시 빌드", "강제 빌드" 요청 시 |
| `-COMPRESS` | 운영 배포, 압축 요청 시 |
| `-COMPRESS -SHRINK` | 난독화 포함 요청 시 |
| `-MERGE` | JS 파일 병합 요청 시 |
| `-L [LOG_PATH]` | 로그 저장 요청 시 |
| `-SERVICE [ID]` | 특정 서비스만 빌드 요청 시 |

---

## Step 4: 명령 실행

1. `{Base Path}build-config.json`의 값과 빌드 모드/추가 옵션을 조합하여 최종 명령을 구성합니다.
2. 실행 전 구성된 명령을 사용자에게 보여줍니다.
3. `bash_tool`로 명령을 실행합니다.

명령 구성 예시:
```
"C:\Program Files\TOBESOFT\Nexacro N\Tools\nexacrodeploy.exe"
  -P "C:\dev\MyProject\src\main\nxui\PackageN\PackageN.xprj"
  -O "C:\dev\MyProject\src\main\resources\static\PackageN\"
  -B "C:\dev\MyProject\src\main\nxui\PackageN\nexacrolib"
  -GENERATERULE "C:\Program Files\TOBESOFT\Nexacro N\SDK\24.0.0\generate"
```

---

## Step 5: 결과 요약 출력

```
✅ 빌드 성공  (또는 ❌ 빌드 실패)
─────────────────────────────────────────
프로젝트  : PackageN.xprj
출력 경로 : src\main\resources\static\PackageN\
배포 경로 : (Deploy 모드인 경우 표시)
─────────────────────────────────────────
[오류 발생 시]
오류 내용 : ...
원인 분석 : ...
해결 방법 : ...
```

### 자주 발생하는 오류 패턴

| 오류 메시지 패턴 | 원인 | 해결 방법 |
|-----------------|------|-----------|
| `-O`와 `-D` 경로 동일 | Deploy 경로 충돌 | `-D`를 `-O`와 다른 경로로 변경 |
| xprj 파일 없음 | `-P` 경로 오류 | xprj 파일 경로 재확인 |
| GenerateRule 없음 | `-GENERATERULE` 경로 오류 | SDK generate 폴더 경로 확인 |
| `-FILE` 파일 인식 불가 | 따옴표 형식 오류 | `"'path1','path2'"` 형식 재확인 |

---

## 참고

아규먼트 상세 레퍼런스는 `{Base Path}references/nexacrodeploy-args.md`를 참고하세요.
