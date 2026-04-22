# Nexacro SSV Format

**공식 문서**: https://docs.tobesoft.com/advanced_development_guide_nexacro_n_v24_ko/c0e662b5844feb1b

SSV (Separated Values) 는 nexacro 의 **대용량 / 고속** 통신 포맷입니다. 구분자로 제어 문자 대용의 특수 문자를 사용해 이스케이프 비용을 최소화합니다.

## 구분자 (매우 중요)

| 기호 | 유니코드 | 역할 |
|---|---|---|
| `▼` | U+25BC (BLACK DOWN-POINTING TRIANGLE) | 레코드(행) 종결 |
| `•` | U+2022 (BULLET) | 필드(셀) 구분 |
| `:` | U+003A | 컬럼명-타입-옵션 구분 (메타 영역에서만) |
| `,` | U+002C | 컬럼 정의 나열 (메타 영역에서만) |
| `=` | U+003D | `ConstColumn` 의 값 할당 |

> ⚠️ 이 문자들이 데이터에 포함되어야 할 경우 nexacro 공식 라이브러리가 자동 이스케이프. 자체 직렬화기를 작성할 때 누락되기 쉬운 지점.

## 전체 샘플 (Dataset 2개)

```
SSV:utf-8▼
Dataset:dataset0▼
_Const_•ConstCol1:STRING(20)=Name•ConstCol2:INT=1•ConstCol3:DECIMAL=0.8▼
_RowType_•Col1:STRING(20)•Col2:INT:SUM•Col3:DECIMAL:AVG▼
N•Test•0•1•1▼
I•Abc•1•2•2▼
U•Def•2•3•3▼
O•Chk•2•3•3▼
D•Ghi•3•4•4▼
▼
Dataset:dataset1▼
_RowType_•Col1:INT(4):Summ,Col2:STRING(30):Text▼
N•0•test▼
I•1•test1▼
U•2•test3▼
O•2•test3-1▼
D•3•test4▼
▼
```

## 레코드 구조

### 1. 헤더
```
SSV:utf-8▼
```
- 고정 시그니처. 인코딩 선언.

### 2. Dataset 시작
```
Dataset:<id>▼
```

### 3. `_Const_` 행 (선택)
ConstColumn 의 정의 + 값. 한 줄에 컬럼 정의가 `•` 로 나열됨.

```
_Const_•<id>:<TYPE>(<size>)=<value>•<id>:<TYPE>(<size>)=<value>▼
```

### 4. `_RowType_` 행
일반 Column 의 정의. 첫 필드는 항상 리터럴 `_RowType_`.

```
_RowType_•<id>:<TYPE>(<size>)[:<agg>]•<id>:<TYPE>(<size>)[:<agg>]▼
```

- `<agg>` 는 `SUM`, `AVG`, `COUNT` 등의 집계 플래그 (UI 메타. 서버 저장 로직엔 영향 없음)

### 5. 데이터 Row
```
<RowType>•<col1>•<col2>•<col3>…▼
```
- 첫 필드가 `_RowType_` 값 (`N` / `I` / `U` / `D` / `O`)
- 나머지는 컬럼 순서대로 값

### 6. Dataset 종결
```
▼
```
- 빈 레코드 = Dataset 경계. 다음 `Dataset:<id>▼` 가 바로 이어지거나 페이로드 종료.

## `_RowType_` 페어 (UPDATE 의 경우)

```
O•key1•oldValue1•oldValue2▼
U•key1•newValue1•newValue2▼
```
- `O` (Original) + `U` (Update) 쌍. 서버는 `O` 로 WHERE 절을 만들고 `U` 로 SET 을 채움.
- `D` 삭제에도 `O` 가 동반될 수 있음 (WHERE 기준 제공).

## 파싱 팁

- **라인 단위 split 금지.** `\n` 이 아니라 `▼` 로 분리해야 함. 데이터에 줄바꿈이 포함된 경우 라인 split 은 즉시 깨짐.
- **바이트 단위 처리 주의**: `▼` / `•` 는 UTF-8 에서 3바이트. 인덱스 기반 자르기를 쓰면 멀티바이트 경계를 넘을 수 있음. 문자열 토큰화 API 사용.
- **공식 라이브러리 의존 권장**: `com.nexacro.xapi.data.datatype.PlatformDataType` 등 내부 타입 체계가 XML/JSON 과 공유됨. 자체 파서 작성 시 `INT`, `DECIMAL`, `DATE` 포맷 규칙을 모두 맞춰야 하므로 유지보수 비용이 큼.
- **압축 효과**: 컬럼 이름이 헤더에 단 한 번만 나와 Dataset 당 오버헤드가 상수. JSON 대비 40~60% 수준 전송 용량 (그리드 수십만 행 시 체감 큼).
