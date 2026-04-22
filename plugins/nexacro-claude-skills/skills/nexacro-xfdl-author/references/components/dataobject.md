# DataObject

**역할**: JSON/XML 등 불투명 바이너리 또는 구조화 데이터를 메모리에 보유하는 컴포넌트. Dataset의 `binddataobject` + `dataobjectpath`(JSONPath)를 통해 Dataset에 데이터를 공급.
**샘플**: `sample_dataobject_01.xfdl` ~ `sample_dataobject_04.xfdl`

## 최소 구성

### 외부 URL에서 JSON 로드

`<Objects>` 안에 선언:

```xml
<Objects>
  <DataObject id="DataObject00" url="../FileSample/data.json"/>
  <Dataset id="Dataset00" binddataobject="DataObject00"
           dataobjectpath="$.data[*]">
    <ColumnInfo>
      <Column id="id"   datapath="@.id"   type="STRING" size="256"/>
      <Column id="name" datapath="@.name" type="STRING" size="256"/>
    </ColumnInfo>
  </Dataset>
</Objects>
```

스크립트에서 `load()` 호출로 데이터 수신:

```javascript
this.DataObject00.load();
```

### 인라인 JSON 데이터 (CDATA)

```xml
<DataObject id="DataObject00">
  <Contents><![CDATA[{
    "items": [
      {"code": "ko", "label": "Korean"},
      {"code": "en", "label": "English"}
    ]
  }]]></Contents>
</DataObject>
```

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| `id` | ✓ | 컴포넌트 고유 식별자 |
| `url` | | 데이터를 가져올 외부 URL (JSON/XML) |
| `Contents` | | XFDL 내 인라인 데이터 (CDATA 블록) |

## Dataset 연동 속성 (Dataset 측)

| 속성 | 설명 |
|---|---|
| `binddataobject` | 바인딩할 DataObject의 id |
| `dataobjectpath` | JSONPath 표현식 (예: `$.data[*]`, `$.items[*]`) |
| `Column.datapath` | 각 컬럼의 JSONPath (예: `@.id`, `@.name`) |

## 주요 메서드

| 메서드 | 서명 | 설명 |
|---|---|---|
| `load()` | `()` | `url` 속성 기반으로 외부 데이터 요청 |
| `setData(data)` | `(string)` | 데이터를 직접 문자열로 설정 |
| `getData()` | `() → string` | 현재 보유 데이터를 문자열로 반환 |

## 이벤트

| 이벤트 | 설명 |
|---|---|
| `onload` | 외부 데이터 로드 완료 시 발생 |
| `onerror` | 로드 실패 시 발생 |

## 주의점 / 팁

- DataObject는 `<Objects>` 안에 Dataset과 함께 선언. Layout 내부에 위치하지 않음.
- `dataobjectpath`를 런타임에서 변경하면 Dataset이 자동으로 갱신됨 (다국어 전환 등에 활용).
- 인라인 `<Contents>`는 정적 참조 데이터(코드표, 번역 문자열 등)에 적합; 서버 연동은 `url` + `load()` 패턴 사용.
- 서버와의 동적 데이터 교환(CRUD)은 Dataset 직접 트랜잭션 방식(`this.transaction()`)이 더 적합. DataObject는 읽기 전용 데이터 공급에 최적.
- JSONPath 문법: 배열 전체 행 → `$.root[*]`, 단일 객체 → `$.root`.
