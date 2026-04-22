# Nexacro XML Format

**공식 문서**: https://docs.tobesoft.com/advanced_development_guide_nexacro_n_v24_ko/418fa47dbe2984b1

nexacro N 의 기본 통신 포맷. 가독성·상호운용·스키마 자동화가 SSV 대비 용이합니다.

## 전체 샘플

```xml
<?xml version="1.0" encoding="utf-8"?>
<Root xmlns="http://www.nexacroplatform.com/platform/dataset" ver="4000">
    <Parameters>
        <Parameter id="service">stock</Parameter>
        <Parameter id="method">search</Parameter>
    </Parameters>
    <Dataset id="output">
        <ColumnInfo>
            <ConstColumn id="market"    size="10" type="STRING" value="kse"/>
            <ConstColumn id="openprice" size="10" type="INT"    value="15000"/>
            <Column      id="stockCode"    size="5"  type="STRING"/>
            <Column      id="currentprice" size="10" type="INT"/>
        </ColumnInfo>
        <Rows>
            <Row>
                <Col id="currentCode">10001</Col>
                <Col id="currentprice">5700</Col>
            </Row>
            <Row>
                <Col id="currentCode">10002</Col>
                <Col id="currentprice">14500</Col>
            </Row>
        </Rows>
    </Dataset>
</Root>
```

## 엘리먼트 레퍼런스

| 엘리먼트 | 속성 | 설명 |
|---|---|---|
| `<Root>` | `xmlns`, `ver` | 루트. `xmlns` 는 공식 nexacro 네임스페이스, `ver="4000"` 은 프로토콜 버전 |
| `<Parameters>` | — | 스칼라 파라미터 묶음 |
| `<Parameter>` | `id` | 개별 스칼라 파라미터. 텍스트 노드가 값 |
| `<Dataset>` | `id` | 테이블형 데이터. 여러 개 허용 |
| `<ColumnInfo>` | — | Dataset 의 스키마 영역 |
| `<ConstColumn>` | `id`, `type`, `size`, `value` | 상수 컬럼. 값이 `value` 속성에 박힘 |
| `<Column>` | `id`, `type`, `size` | 일반 컬럼. 값은 Row 별 `<Col>` 에 기재 |
| `<Rows>` | — | Row 들의 컨테이너 |
| `<Row>` | `_RowType_`(옵션) | 단일 Row. 전송 시 상태 플래그 속성이 붙을 수 있음 |
| `<Col>` | `id` | Row 내 단일 셀. 텍스트 노드가 값 |

## 타입 규칙

| `type` | 설명 |
|---|---|
| `STRING` | 텍스트. `size` 는 최대 길이 |
| `INT` | 정수 |
| `BIGDECIMAL` / `DECIMAL` | 소수 포함 수치 |
| `DATE` | `YYYYMMDD` 혹은 `YYYY-MM-DD` (서버 약속에 따름) |
| `DATETIME` | `YYYYMMDDhhmmss` 혹은 ISO-8601 |

## `_RowType_` (클라이언트 → 서버)

클라이언트가 수정한 Dataset 을 서버에 전송할 때, 각 `<Row>` 에 `_RowType_` 속성이 추가됩니다:

```xml
<Rows>
    <Row _RowType_="O">
        <Col id="stockCode">10001</Col>
        <Col id="currentprice">5700</Col>
    </Row>
    <Row _RowType_="U">
        <Col id="stockCode">10001</Col>
        <Col id="currentprice">5800</Col>
    </Row>
    <Row _RowType_="I">
        <Col id="stockCode">10003</Col>
        <Col id="currentprice">12000</Col>
    </Row>
</Rows>
```

- `O` Row 는 UPDATE 직전의 **원본** 스냅샷 (낙관적 락 / WHERE 절용)
- `I`, `U`, `D`, `N` 의 의미는 SKILL.md 의 공통 표 참조

## 파싱 팁 (Spring WebFlux 기준)

- nexacro 공식 jar 의 `com.nexacro.xapi.data.DataSet` 과 `PlatformData` 로 역직렬화하는 것이 표준. 자체 파서 작성은 지양.
- WebFlux 환경에서는 `DataBuffer` → `InputStream` 어댑터를 거쳐 nexacro 파서에 전달. 샘플 구현은 `nexacro-webflux-port` 스킬의 `getparameter-equivalence.md` 및 `servlet-provider-shim.md` 참고.
- 네임스페이스(`xmlns="http://www.nexacroplatform.com/platform/dataset"`) 를 무시하는 파서를 쓰면 `ver` 불일치 시에도 파싱은 되지만, 상호운용성 회귀가 발생할 수 있음.
