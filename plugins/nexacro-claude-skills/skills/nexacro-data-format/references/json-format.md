# Nexacro JSON Format

**공식 문서**: https://docs.tobesoft.com/advanced_development_guide_nexacro_n_v24_ko/e29aff991b5ddfd0

REST / JS 연동 친화적인 포맷. 사람이 읽기 가장 쉬워 디버깅·로그 분석에 유리합니다.

## 전체 샘플 (Dataset 2개)

```json
{
    "version": "1.0",
    "Parameters": [
        {"id": "ErrorCode", "value": 0},
        {"id": "ErrorMsg",  "value": ""},
        {"id": "param1",    "value": "0", "type": "string"}
    ],
    "Datasets": [
        {
            "id": "indata",
            "ColumnInfo": {
                "ConstColumn": [
                    {"id": "ConstCol1", "value": 10},
                    {"id": "ConstCol2", "type": "string", "size": "256", "value": 10}
                ],
                "Column": [
                    {"id": "Column0"},
                    {"id": "Column1", "type": "string", "size": "256"}
                ]
            },
            "Rows": [
                {"_RowType_": "U", "Column0": "",  "Column1": "zzz"},
                {"_RowType_": "O", "Column0": "",  "Column2": ""},
                {"_RowType_": "N", "Column0": "A", "Column1": "B"},
                {"_RowType_": "D", "Column0": "a", "Column1": "b"},
                {"_RowType_": "I", "Column0": "",  "Column1": ""}
            ]
        },
        {
            "id": "indata2",
            "ColumnInfo": {
                "Column": [
                    {"id": "Column0"},
                    {"id": "Column1", "type": "string", "size": "256"},
                    {"id": "Column2", "type": "string", "size": "256"}
                ]
            },
            "Rows": [
                {"Column0": "A", "Column1": "B"},
                {"Column0": "a", "Column1": "b", "Column2": "c"},
                {"Column0": "",  "Column1": "",  "Column2": ""}
            ]
        }
    ]
}
```

## 필드 레퍼런스

### 최상위

| 필드 | 타입 | 설명 |
|---|---|---|
| `version` | string | 프로토콜 버전. 현재 `"1.0"` 고정 |
| `Parameters` | array | 스칼라 파라미터 배열 |
| `Datasets` | array | Dataset 배열 |

### `Parameters[i]`

| 필드 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | 파라미터 이름 |
| `value` | ✓ | 값 (문자열 또는 숫자) |
| `type` | 선택 | `"string"` / `"int"` / `"decimal"` 등. 생략 시 JSON 원시 타입으로 해석 |

### `Datasets[i]`

| 필드 | 설명 |
|---|---|
| `id` | Dataset 식별자 |
| `ColumnInfo` | 스키마 (아래 두 서브 필드) |
| `ColumnInfo.ConstColumn` | 상수 컬럼 배열. 각 요소는 `{id, value, [type], [size]}` |
| `ColumnInfo.Column` | 일반 컬럼 배열. 각 요소는 `{id, [type], [size]}` |
| `Rows` | Row 객체 배열 |

### `Rows[i]`

- 각 Row 는 **JSON 객체**. 키는 컬럼 id, 값은 해당 셀의 값.
- `_RowType_` 키가 존재하면 상태 플래그 (`N`/`I`/`U`/`D`/`O`). 생략 시 `N` (조회 응답).
- ConstColumn 값은 Row 에 중복 기재하지 않음 (Dataset 레벨에서 이미 선언).

## 주의점 — 공식 샘플의 trailing 콤마

nexacro 공식 문서 JSON 예제 일부에서 `"value":""` 뒤 콤마가 빠진 표기가 관찰됩니다. 예:

```json
{"id":"ErrorCode", "value":0}, 
{"id":"ErrorMsg",  "value":""}    ← 이 다음에 콤마가 없음
{"id":"param1",    "value":"0", "type":"string"}
```

- **엄격 파서** (`Jackson` 기본, `JSON.parse`): 실패
- **관대 파서** (`Jackson` + `ALLOW_MISSING_VALUES`, nexacro 자체 파서): 허용

서버/클라이언트가 서로 다른 파서를 쓰면 회귀가 발생하므로, **공식 라이브러리의 직렬화기 / 파서를 쓰는 것이 안전**합니다 (`NexacroPlatformSerializer` / `PlatformData.fromJson`).

## `_RowType_` 패턴

### 단순 변경 (U/O 페어)
```json
{"_RowType_": "O", "id": "100", "name": "Alice"},
{"_RowType_": "U", "id": "100", "name": "Alicia"}
```

### 삭제
```json
{"_RowType_": "O", "id": "200", "name": "Bob"},
{"_RowType_": "D", "id": "200", "name": "Bob"}
```

### 조회 응답 (상태 없음)
```json
{"id": "100", "name": "Alice"},
{"id": "200", "name": "Bob"}
```

## 파싱 팁 (Spring WebFlux)

- `application/json` 으로 들어온 nexacro 페이로드는 Spring 의 표준 `Jackson2JsonDecoder` 로는 곧바로 `PlatformData` 로 매핑되지 않음. 커스텀 `HttpMessageReader` 혹은 nexacro 라이브러리 어댑터 필요.
- 복합 `Datasets[]` 루프 돌며 `ColumnInfo` → 스키마 생성 → `Rows[]` 를 타입 변환해 `DataSet` 에 주입하는 로직은 공식 구현과 동일한 순서로 유지할 것 (타입 힌트 없는 값의 해석 차이로 회귀 발생 가능).
- **`version` 필드 무시 금지**: 향후 프로토콜 업그레이드 시 분기 지점. 1.x 가정 하드코딩은 피해야 함.
