# 로컬 자료 검색 가이드

ripgrep이 설치되어 있어 로컬 자료를 더 효율적으로 검색할 수 있습니다.

## 🔍 ripgrep 사용법

### 기본 검색
```bash
# 현재 디렉토리에서 검색
rg "검색어"

# 특정 확장자로만 검색
rg "검색어" --type md
rg "검색어" --type js

# 대소문자 무시
rg "검색어" -i

# 라인 번호 표시
rg "검색어" -n

# 컬러 출력 강제
rg "검색어" --color always
```

### 고급 검색

#### 여러 패턴 동시 검색
```bash
# 여러 단어 중 하나라도 포함되는 파일 찾기
rg "build|deploy|generate" -n

# 특정 디렉토리만 검색
rg "nexacro" docs/
rg "skill" skills/
```

#### 패턴 검색
```bash
# 숫자가 포함된 라인 검색
rg "\d+" -n

# 이메일 주소 검색
rg "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

# 파일 경로 검색
rg "\.md" -l
```

#### 결과 필터링
```bash
# 파일명만 출력
rg "검색어" -l

# 라인 수 제한
rg "검색어" -n -A 3 -B 3  # 각 매치 앞뒤 3줄 표시

# 정규식을 사용한 파일 제외
rg "검색어" --glob "!*.test.js"
```

## 📁 검색 최적화 설정

### 특정 폴더 검색
```bash
# skills 폴더만 검색
rg "build" skills/

# docs 폴더에서 한글 검색
rg "빌드" docs/ --type md

# examples 폴더에서 예제 찾기
rg "예제" examples/
```

### 프로젝트별 검색 패턴

#### 넥사크로 관련 검색
```bash
# 모든 넥사크로 관련 용어 검색
rg "넥사크로|nexacro" --type md --type js

# 빌드 관련 용어
rg "빌드|build|배포|deploy|generate" -n

# 스킬 관련 용어
rg "스킬|skill|트리거|trigger" -n
```

#### 오류 메시지 검색
```bash
# 에러 로그 검색
rg "Error|error|오류|실패" -A 2 -B 2
```

## 🛠️ 검색 스크립트 예시

### 상위 디렉토리까지 검색
```bash
# 상위 디렉토리로 올라가면서 검색
cd .. && rg "검색어" --type md
```

### 특정 형식의 파일만 검색
```bash
# 모든 Markdown 파일에서 검색
rg "검색어" -t md

# JavaScript 파일만 검색
rg "검색어" -t js
```

### Git 제외 파일 무시
```bash
# .gitignore 파일 기반으로 무시
rg "검색어" --ignore-file .gitignore
```

## 📋 실용적인 검색 예제

### 1. 스킬 관련 문서 검색
```bash
# 스킬 이름으로 검색
rg "nexacro-build" -n

# 설명에서 특정 기능 검색
rg "자동화" docs/
```

### 2. 코드 예제 검색
```bash
# 예제 코드 찾기
rg "예제|example" examples/ -A 5 -B 5

# 사용법 검색
rg "사용법|how to" -n
```

### 3. 오류 해결 검색
```bash
# 에러 메시지 검색
rg "timeout|시간초과" -A 3 -B 3

# 해결책 검색
rg "해결|solution|fix" -n
```

## 🔧 추천 단축키 (사용 시)

별도 설정을 통해 단축키를 지정할 수 있습니다. 주로 사용하는 패턴을 저장해두고 필요할 때마다 활용하세요.

```bash
# 검색 결과를 파일로 저장
rg "검색어" > results.txt

# 검색 결과와 함께 파일명만 출력
rg "검색어" -l
```

ripgrep은 일반 grep보다 훨씬 빠르고 정확하며, 자동으로 이진 파일과 Git 저장소를 건너뛰는 등 실용적인 기능을 제공합니다.