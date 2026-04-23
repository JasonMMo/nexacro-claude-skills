# Troubleshooting

자주 발생하는 이슈와 해결법.

## 설치/호출 단계

### `gh` 미인증

증상: `git clone` 단계에서 `remote: Repository not found` 또는 HTTPS 자격 증명 실패.

해결:
```bash
gh auth login
# or for public clone only
git config --global credential.helper manager-core
```

### Windows 에서 `sed -i` 실패

증상: 토큰 치환 단계에서 `sed: -i may not be used with stdin`.

해결: `sed -i` 대신 Python 사용.
```bash
python -c "
import pathlib, sys
for p in pathlib.Path('.').rglob('*'):
    if not p.is_file() or p.suffix in {'.jar','.class','.zip','.png','.jpg'}: continue
    try: t = p.read_text(encoding='utf-8')
    except: continue
    if '{{PROJECT_NAME}}' in t:
        p.write_text(t.replace('{{PROJECT_NAME}}', '${PROJECT_NAME}'), encoding='utf-8')
"
```

### `.gitignore` 누락으로 `target/` 커밋됨

증상: 초기 커밋에 수만 파일.

해결: 템플릿의 `.gitignore` 가 복사되었는지 확인. 없으면 수동 추가 후:
```bash
git rm -rf --cached target/
git add .gitignore
git commit -m "chore: apply gitignore"
```

## 빌드 단계

### Maven `compile` — `package javax.servlet does not exist`

증상: jdk17 환경에서 javax 기반 runner 실행.

원인: 잘못된 runner 선택 (예: jdk17 환경에서 `boot-jdk8-javax`).

해결: 올바른 runner 재스캐폴드 또는 `JAVA_HOME` 을 jdk8 로 설정.

### Maven `test-compile` — `package jakarta.servlet does not exist`

증상: jdk8 환경에서 jakarta 기반 runner 실행.

원인: 반대 케이스. jdk17 설치 필요.

해결: `JAVA_HOME` jdk17 로 설정 또는 `boot-jdk8-javax` 재스캐폴드.

### `mvn spring-boot:run` — port 8080 already in use

증상: `Web server failed to start. Port 8080 was already in use.`

해결 1: 기존 프로세스 종료
```bash
# Windows
netstat -ano | findstr :8080
taskkill /F /PID <pid>
# macOS/Linux
lsof -ti :8080 | xargs kill -9
```

해결 2: 다른 포트 사용 (`application.yml` 의 `server.port` 수정) — 단, nxui `svcurl` 도 맞춰 수정 필요.

## 실행 단계

### nexacro IDE 에서 `packageN.xprj` 열기 실패

증상: "프로젝트 파일이 손상되었습니다".

원인: `{{PROJECT_NAME}}` 토큰 치환 누락.

해결: 타겟 디렉터리에서 `grep -r "{{" nxui/` 로 남은 토큰 확인 후 수동 치환.

### 브라우저 `http://localhost:8080/uiadapter/` 에서 404

증상: nxui 가 로드되지 않음.

원인 1: 서버가 실행 중이 아님. `mvn spring-boot:run` 출력 확인.

원인 2: `contextPath` 불일치. `application.yml` 의 `server.servlet.context-path` 가 `/uiadapter` 인지 확인.

원인 3: nexacro 빌드 산출물이 `static/uiadapter/` 에 배포 안 됨. 별도 플러그인 `nexacro-build` 로 생성 후 복사.

### `login.do` 가 항상 "LOGIN_SUCCESS" 반환

정상 동작입니다. Plan 1 은 Spring Security 미적용, 로그인은 스텁 구현 (§1.3 of design spec). Phase 2 이후 실제 인증 추가 예정.

### WebFlux runner — Mono chain 에서 `Cannot invoke "..." because "..." is null`

증상: 업로드/다운로드 endpoint 에서 NPE.

원인: multipart 부분 읽기가 blocking 코드와 혼재.

참고: `plugins/nexacro-webflux-port/skills/nexacro-webflux-port/references/multipart-import-by-type.md`
