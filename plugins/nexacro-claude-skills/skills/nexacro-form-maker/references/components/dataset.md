# Dataset

**Role**: In-memory tabular data store declared inside an XFDL form. Binds to Grid, ComboBox, and other data-aware components, and is the primary vehicle for client-server data exchange.
**Source**: `sample_dataset_01.xfdl` (also visible in `sample_grid_02.xfdl`)

## Minimum XML block

Placed inside `<Objects>` at the form level (sibling of `<Layouts>`).

```xml
<Objects>
  <Dataset id="Dataset00">
    <ColumnInfo>
      <Column id="Name"    type="STRING"  size="256"/>
      <Column id="Address" type="STRING"  size="256"/>
      <Column id="Salary"  type="INT"     size="256"/>
    </ColumnInfo>
    <Rows>
      <Row>
        <Col id="Name">John</Col>
        <Col id="Address">Seoul, KOREA</Col>
        <Col id="Salary">15000</Col>
      </Row>
    </Rows>
  </Dataset>
</Objects>
```

### Empty dataset (populated at runtime via transaction)

```xml
<Dataset id="dsEmployee">
  <ColumnInfo>
    <Column id="empId"   type="STRING" size="10"/>
    <Column id="empName" type="STRING" size="50"/>
    <Column id="salary"  type="INT"    size="10"/>
  </ColumnInfo>
  <Rows/>
</Dataset>
```

### With ConstColumn (shared constant value for all rows)

```xml
<Dataset id="dsStock">
  <ColumnInfo>
    <ConstColumn id="market" type="STRING" size="10" value="kse"/>
    <Column id="stockCode"   type="STRING" size="5"/>
    <Column id="price"       type="INT"    size="10"/>
  </ColumnInfo>
  <Rows/>
</Dataset>
```

## Structure / attributes

### ColumnInfo

| element | attribute | description |
|---|---|---|
| `<Column>` | `id` | Column name — used as the bind key (`bind:ColumnId`) |
| | `type` | `STRING`, `INT`, `DECIMAL`, `DATE` |
| | `size` | Storage size hint (characters for STRING, digits for numeric) |
| `<ConstColumn>` | `value` | Fixed value shared by all rows; not editable at runtime |

### Column types

| type | notes |
|---|---|
| `STRING` | Default; handles all text |
| `INT` | Integer; used for IDs, counts, currency integers |
| `DECIMAL` | Floating point; specify precision via `size` |
| `DATE` | Stored as `YYYYMMDD` string internally |

### Rows / Row / Col

- `<Rows>` may be empty (`<Rows/>`) when data will arrive from a server transaction.
- Each `<Row>` contains `<Col id="columnId">value</Col>` entries.
- Columns not listed in a `<Row>` default to empty/null.

## Common script methods

| method | signature | purpose |
|---|---|---|
| `getCount()` | `() → int` | Total row count |
| `getColumn(row, col)` | `(int, string) → value` | Read a cell value |
| `setColumn(row, col, val)` | `(int, string, any)` | Write a cell value |
| `addRow()` | `() → int` | Append a new empty row, returns new row index |
| `deleteRow(row)` | `(int)` | Mark row as deleted (`_RowType_ = "D"`) |
| `getCaseSum(expr, col)` | `(string, string) → number` | Conditional sum |
| `getCaseAvg(expr, col)` | `(string, string) → number` | Conditional average |
| `getCaseCount(expr, col)` | `(string, string) → number` | Conditional count |

## Notes / Gotchas

- Dataset `id` must match the `binddataset` attribute on any bound Grid or ComboBox.
- Datasets live in `<Objects>`, never inside `<Layouts>`.
- Pre-seeded `<Rows>` are useful for lookup/reference data that never changes; leave `<Rows/>` empty for anything fetched from the server.
- `ConstColumn` values appear in every row but are not transmitted in the modified-rows payload when sending data back to the server.
- Row state (`_RowType_`) tracks `N` (normal), `I` (inserted), `U` (updated), `D` (deleted) for delta transmission.

> This document covers the XFDL declaration. For the runtime wire format used in client-server communication (XML / SSV / JSON), see the `nexacro-data-format` skill.
