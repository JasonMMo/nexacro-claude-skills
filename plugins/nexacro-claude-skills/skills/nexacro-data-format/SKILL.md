---
name: nexacro-data-format
description: nexacroN 클라이언트와 서버 간 통신 데이터 포맷(XML / SSV / JSON) 의 구조·샘플·RowType 의미를 참조하기 위한 스킬. "nexacro 포맷", "SSV 포맷", "Dataset XML", "nexacro JSON", "_RowType_", "ConstColumn", "nexacro 응답 파싱" 같은 요청에서 호출.
---

# Nexacro Data Format Skill

nexacroN 플랫폼에서 클라이언트 ↔ 서버 간 통신에 사용되는 세 가지 포맷의 **공식 샘플과 필드 의미**를 Claude 가 정확히 기억하고 생성/파싱 코드에 반영하기 위한 참조 스킬입니다.

## 개요

nexacro 는 동일한 Dataset 모델을 세 가지 직렬화 형식으로 주고받을 수 있습니다. 실제 선택은 서버 구현(Spring MVC `NexacroPlatformController`, WebFlux `NexacroHandlerFunction` 등) 의 `Content-Type` / `Accept` 협상과 클라이언트 `Transaction` 설정에 의해 결정됩니다.

| 포맷 | Content-Type | 주 용도 | 참조 문서 |
|---|---|---|---|
| XML | `text/xml` · `application/xml` | nexacro N 기본값, 가독성/상호운용 중심 | [references/xml-format.md](references/xml-format.md) |
| SSV | `text/ssv` (`application/ssv`) | 대용량 Dataset, 압축/전송 효율 최적화 | [references/ssv-format.md](references/ssv-format.md) |
| JSON | `application/json` | JS / REST API 연동, 수기 디버깅 친화 | [references/json-format.md](references/json-format.md) |

> 세 포맷 모두 동일한 개념 모델 (`Parameters` · `Dataset` · `ColumnInfo` · `Rows`) 을 공유합니다.

## 공통 개념

### Parameters
- 요청/응답의 스칼라 페이로드
- 서비스 ID, 메서드, 에러 코드·메시지, 단일 값 파라미터 등에 사용
- Spring/WebFlux 포팅 맥락에서는 `Map<String, String>` 형태의 request-scoped bag 으로 관리되는 것이 관례

### Dataset
- 테이블형 데이터 구조. 여러 Dataset 을 한 페이로드에 담을 수 있음
- 각 Dataset 은 `id` 로 구분

### ColumnInfo
- `ConstColumn` — 모든 Row 가 공유하는 상수 값 (예: 시장 구분, 조회 기준일)
- `Column` — 일반 컬럼 (Row 마다 값이 다름)
- `type`, `size` 속성으로 스키마 선언
- Summ/Avg 등의 집계 속성(SSV 참고)은 클라이언트 UI 컨트롤이 이용하는 메타

### Rows / `_RowType_`
클라이언트가 서버로 전송하는 Dataset 의 각 Row 는 **상태 플래그** `_RowType_` 을 가집니다. 서버는 이 플래그를 보고 INSERT/UPDATE/DELETE 를 분기합니다.

| `_RowType_` | 의미 | 서버 처리 |
|---|---|---|
| `N` | Normal — 변경 없음 | 읽기 전용, 저장 스킵 |
| `I` | Insert — 신규 Row | INSERT |
| `U` | Update — 수정된 Row | UPDATE (원본 값이 필요하면 `O` 와 짝으로 전송됨) |
| `D` | Delete — 삭제된 Row | DELETE |
| `O` | Original — 수정 전 원본 스냅샷 | UPDATE 시 WHERE 절 구성 / 낙관적 락 |

> ⚠️ `O` Row 는 `U` 또는 `D` 바로 앞(또는 뒤)에 페어로 등장합니다. 서버는 `U/O` 쌍을 묶어 원본/변경 후 값을 대조하는 것이 일반적입니다.

## 포맷 선택 가이드

- **신규 WebFlux 포팅**: 초기엔 XML 을 유지 → 회귀 테스트가 안정된 뒤 SSV 로 단계적 전환 (압축률·파싱 속도 이점)
- **브라우저 디버깅이 주된 시나리오**: JSON (Chrome DevTools Network 탭에서 바로 열람)
- **대용량 그리드 조회**: SSV (개행/컬럼 구분자를 제어문자로 사용 → 이스케이프 비용 최소화)

## 실무 팁

1. **인코딩은 UTF-8 로 고정**. SSV 첫 줄 `SSV:utf-8▼` 과 XML 선언 `encoding="utf-8"` 은 서버와 클라이언트에서 반드시 일치해야 함.
2. **SSV 구분자**: 레코드 종결 `▼` (U+25BC), 필드 구분 `•` (U+2022), 컬럼 부가 정보 구분 `:`, 컬럼 나열 `,`. 텍스트 에디터로 열 때 이 문자들이 공백/물음표로 보이면 인코딩 문제.
3. **JSON 샘플의 trailing 콤마 주의**: 공식 문서 JSON 예시 중 일부는 `"value":""` 뒤에 콤마가 빠져 있어 엄격 파서(예: `ObjectMapper` 기본 설정) 에서 실패할 수 있음. 서버 측에서 관대 파서를 쓰거나 자체 직렬화기를 쓰는 것이 안전.
4. **ConstColumn 의 `value`**: 모든 Row 에 broadcast. Row 측 `Col` 에 같은 id 가 등장하지 않아야 함 (중복 시 해석이 벤더별로 다를 수 있음).

## 출처 (공식 문서)

- XML: https://docs.tobesoft.com/advanced_development_guide_nexacro_n_v24_ko/418fa47dbe2984b1
- SSV: https://docs.tobesoft.com/advanced_development_guide_nexacro_n_v24_ko/c0e662b5844feb1b
- JSON: https://docs.tobesoft.com/advanced_development_guide_nexacro_n_v24_ko/e29aff991b5ddfd0

> 각 포맷의 **전체 샘플과 파싱 가이드**는 `references/*.md` 를 참조하세요.
