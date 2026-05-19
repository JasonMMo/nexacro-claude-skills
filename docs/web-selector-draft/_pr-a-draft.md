# PR-A 초안 — runner-matrix.yml release publish step

> **거주 repo**: `JasonMMo/nexacroN-fullstack` (이 repo 아님 — 별도 클론에서 적용)
> **목적**: nightly 매트릭스 그린 후 7 자산을 `nightly` 태그에 정확한 이름으로 publish
> **계약**: 자산 파일명 = `{runnerKey}.{packaging}` (셀렉터 `buildUrl()` 와 1:1)
> **생성**: 2026-05-19, M2 준비 작업

---

## 적용 절차 (다음 세션 — 별도 워크트리 / 클론)

```powershell
# 시블링 클론 생성 (1회)
cd D:\AI\workspace
git clone https://github.com/JasonMMo/nexacroN-fullstack.git
cd nexacroN-fullstack
git checkout -b feat/release-publish-nightly

# 아래 patch 적용 후 push + PR open
```

---

## upstream `.github/workflows/runner-matrix.yml` 현재 상태 (2026-05-19 확인)

요점:
- 7-job matrix: `runner` × `jdk` × `smoke(jar|war)`
- 각 job: `checkout → setup-java → mvn package → upload-artifact → smoke(continue-on-error)`
- `permissions:` 미설정 (기본 read-only) — release 게시 위해 `contents: write` 필요
- 트리거: `pull_request` + `schedule (0 18 * * * = nightly 03:00 KST)` + `workflow_dispatch`

---

## Patch (unified diff 형식)

```diff
 name: runner-matrix
 on:
   pull_request:
     paths:
       - 'samples/runners/**'
       - 'scripts/**'
       - '.github/workflows/runner-matrix.yml'
   schedule:
     - cron: '0 18 * * *'   # nightly 03:00 KST
   workflow_dispatch:

+permissions:
+  contents: write
+
 jobs:
   build:
     strategy:
       fail-fast: false
       matrix:
         include:
           - { runner: boot-jdk17-jakarta,       jdk: 17, smoke: jar }
           - { runner: boot-jdk8-javax,          jdk: 8,  smoke: jar }
           - { runner: mvc-jdk17-jakarta,        jdk: 17, smoke: war }
           - { runner: mvc-jdk8-javax,           jdk: 8,  smoke: war }
           - { runner: egov5-boot-jdk17-jakarta, jdk: 17, smoke: jar }
           - { runner: egov4-boot-jdk8-javax,    jdk: 8,  smoke: jar }
           - { runner: egov4-mvc-jdk8-javax,     jdk: 8,  smoke: war }
     runs-on: ubuntu-latest
     steps:
       - uses: actions/checkout@v4
       - uses: actions/setup-java@v4
         with:
           distribution: temurin
           java-version: ${{ matrix.jdk }}
           cache: maven
       - name: build
         run: mvn -B -ntp clean package
         working-directory: samples/runners/${{ matrix.runner }}
       - uses: actions/upload-artifact@v4
         with:
           name: ${{ matrix.runner }}-target
           path: samples/runners/${{ matrix.runner }}/target/*.${{ matrix.smoke }}
           retention-days: 7
       - name: smoke - /select_datalist.do
         if: matrix.smoke == 'jar'
         run: |
           jar=$(ls target/*.jar | head -1)
           nohup java -jar "$jar" > app.log 2>&1 &
           for i in $(seq 1 30); do sleep 2; curl -sf http://localhost:8080/uiadapter/ && break; done
           curl -sfX POST http://localhost:8080/uiadapter/select_datalist.do \
             -H 'Content-Type: text/xml' \
             --data '<Root><Parameters/><Dataset id="input1"><ColumnInfo/><Rows/></Dataset></Root>' \
             | grep -q 'ErrorCode' && echo OK
         working-directory: samples/runners/${{ matrix.runner }}
         continue-on-error: true
+      - name: rename artifact for release
+        if: github.event_name == 'schedule' && github.ref == 'refs/heads/main'
+        run: |
+          src=$(find target -maxdepth 1 -name "*.${{ matrix.smoke }}" -not -name "original-*" | head -1)
+          if [ -z "$src" ]; then echo "no artifact found"; exit 1; fi
+          cp "$src" "target/${{ matrix.runner }}.${{ matrix.smoke }}"
+          ls -la "target/${{ matrix.runner }}.${{ matrix.smoke }}"
+        working-directory: samples/runners/${{ matrix.runner }}
+      - name: publish to nightly release
+        if: github.event_name == 'schedule' && github.ref == 'refs/heads/main'
+        uses: softprops/action-gh-release@v2
+        with:
+          tag_name: nightly
+          name: nightly
+          prerelease: true
+          files: samples/runners/${{ matrix.runner }}/target/${{ matrix.runner }}.${{ matrix.smoke }}
```

---

## 설계 결정 노트

### 왜 매트릭스 job 안에 step 으로? (aggregator job 아닌 이유)
- 핸드오프 §검증 플랜 2: "워크플로에 release publish step 추가" — 단수 step 으로 명시.
- 7 jobs 가 동일 `nightly` 태그에 병렬로 attach → `softprops/action-gh-release@v2` 가 race 안전하게 처리 (먼저 도착한 job 이 release 생성, 나머지는 첨부).
- 실패 격리: 1개 runner 빌드 실패 시 나머지 6개는 publish 계속.

### 왜 rename step 분리?
- `softprops/action-gh-release@v2` 의 `files:` 는 정확한 경로 필요. Maven 생성 파일명 (`app-1.0.0.jar` 등) 은 셀렉터 URL 계약과 불일치.
- `original-*` 제외: Spring Boot `repackage` 가 생성하는 thin-jar 회피 (fat-jar 만 publish).

### 왜 `if` 가드 2중 (event + ref)?
- `pull_request` 트리거에서 실수로 release publish 방지.
- `workflow_dispatch` 에서도 publish 안 함 (수동 promote 는 v1.1, 핸드오프 §범위 밖).
- 오직 `schedule` 발화 + `main` 브랜치 만 publish.

### 왜 `permissions: contents: write` 워크플로 레벨?
- GitHub Actions 기본 토큰은 2023 부터 read-only.
- release 생성·자산 첨부 위해 `contents: write` 필수.
- job 레벨 대신 워크플로 레벨 — 추후 다른 job 추가 시 일관성.

### `stable` 채널은?
- 본 PR 미포함. 핸드오프 §범위 밖: "수동으로 시작, v1.1에서 자동화 검토".
- M6 (수동 promote) 에서 별도 `workflow_dispatch` 워크플로로 추가 예정.

---

## PR 본문 초안 (영문 — guide docs 정책 예외, PR 본문은 영문)

```
## Summary

- Publish 7 matrix runner artifacts to a rolling `nightly` release after each scheduled build
- Asset filename contract: `{runner}.{packaging}` (e.g. `boot-jdk17-jakarta.jar`, `mvc-jdk8-javax.war`)
  — pinned to web selector `buildUrl()` (downstream `nexacro-claude-skills/docs/web-selector-draft/selection.js`)
- Gated to `schedule` events on `main` only; PR builds remain release-free

## Why now

Downstream web selector (Track B) needs deterministic asset URLs to wire static
download links without a backend. Once this PR merges and the first nightly runs,
7 artifacts become available at:

  https://github.com/JasonMMo/nexacroN-fullstack/releases/download/nightly/{runner}.{packaging}

## Test plan

- [ ] After merge, verify nightly run produces 7 assets via `gh release view nightly`
- [ ] Each asset filename matches `{runner}.{packaging}` exactly
- [ ] `gh release download nightly --pattern '*.jar' --dir /tmp/r` succeeds
- [ ] `java -jar /tmp/r/boot-jdk17-jakarta.jar` boots and serves `/uiadapter/` on :8080
- [ ] PR-triggered runs do NOT publish (verify by re-running this PR's CI)

## Rollback

- Revert this PR — release step disappears next nightly
- Delete `nightly` tag if cleanup desired: `gh release delete nightly --yes && git push --delete origin nightly`
```

---

## 정합성 체크 (4-필터)

| 필터 | 결과 | 근거 |
|---|---|---|
| F1 북극성 진척 | ✅ | M3 (첫 nightly 자동 7-자산 publish) 의 직접 입력. |
| F2 D1–D5 위반 없음 | ✅ | 백엔드 0 / PAT 0 (`GITHUB_TOKEN` 만 사용) / 라이선스 미포함 / 재빌드 없음 (rename = cp 1회) / raw `*.jar`·`*.war`. |
| F3 M3 입력 | ✅ | 머지 + 1 nightly cycle 후 7개 URL 활성화. selection.js `buildUrl()` 결과와 byte-level 일치. |
| F4 롤백 ≤ 1커밋 | ✅ | PR 1개 revert → step 3개 (permissions, rename, publish) 제거. `nightly` 태그 1줄 명령 삭제 가능. |

---

## M2 종료 정의 (Definition of Done)

다음 모두 충족 시 M2 통과 → M3 자동 진입:

1. PR-A 가 upstream `master` 에 머지됨
2. 첫 스케줄 발화 (또는 `workflow_dispatch` 1회) 에서 7개 자산이 `nightly` 태그에 게시됨
3. `gh release view nightly --json assets --jq '.assets[].name'` 출력이 정확히:
   ```
   boot-jdk17-jakarta.jar
   boot-jdk8-javax.jar
   mvc-jdk17-jakarta.war
   mvc-jdk8-javax.war
   egov5-boot-jdk17-jakarta.jar
   egov4-boot-jdk8-javax.jar
   egov4-mvc-jdk8-javax.war
   ```
   (순서 무관, 7개 정확)
4. selection.js 의 `buildUrl('boot-jdk17-jakarta', 'jar', 'nightly')` 결과 URL 에 `curl -I` 했을 때 `HTTP 302` (redirect to CDN) 응답

---

## 위험과 대응

| 위험 | 가능성 | 영향 | 대응 |
|---|---|---|---|
| Race condition: 7 jobs 동시 release 생성 | 낮음 | 낮음 | `softprops/action-gh-release@v2` 가 내부적으로 처리 (검증된 패턴). 1차 nightly에서 7 assets 확인. |
| `find ... -not -name "original-*"` 가 다른 valid 파일 누락 | 매우 낮음 | 높음 (publish 실패) | rename step 의 `if [ -z "$src" ]; then exit 1` 가드로 즉시 실패. CI 로그에서 발견. |
| `permissions: contents: write` 이 너무 광범위 | 낮음 | 낮음 | job 레벨로 좁힐 수도 있으나, 워크플로 레벨 유지 (M6 stable promote workflow 추가 시 재사용). |
| `pull_request` 가드 실패로 PR 빌드에서 release 발생 | 매우 낮음 | 중간 (실수 publish) | `if: github.event_name == 'schedule' && github.ref == 'refs/heads/main'` 이중 가드. PR 빌드는 `pull_request` 이벤트. |
| Maven 빌드는 통과하지만 fat-jar 가 비정상 (run 불가) | 중간 | 중간 (사용자 경험) | smoke step (`continue-on-error: true`) 가 신호. M3 종료 정의 #4 의 `curl -I` 로 발견. M5 (end-to-end smoke) 가 최종 안전망. |

---

## M2 다음 세션 시작 메시지 (복붙용)

```
@RESUME.md 트랙 B 재개. M2 PR-A 작성 단계.
참조: docs/web-selector-draft/_pr-a-draft.md (이 repo)
별도 클론에서 작업: D:\AI\workspace\nexacroN-fullstack\
```
