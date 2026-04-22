# Grid

**Role**: Tabular data display and editing component bound to a Dataset. The most structurally complex component in Nexacro.
**Source**: `sample_grid_02.xfdl`

## Minimum XML block

Placed inside `<Layout>` within `<Layouts>`. Always pair with a `<Dataset>` in `<Objects>`.

```xml
<Grid id="Grid00" left="32" top="40" width="560" height="211"
      binddataset="Dataset00"
      autofittype="col"
      selecttype="row">
  <Formats>
    <Format id="default">

      <!-- Column width definitions — one <Column> per data column -->
      <Columns>
        <Column size="80"/>
        <Column size="160"/>
        <Column size="80"/>
      </Columns>

      <!-- Row height templates -->
      <!-- band="head" → header row; no band attr → body (data) row -->
      <Rows>
        <Row size="24" band="head"/>
        <Row size="24"/>
      </Rows>

      <!-- Header band: static label text -->
      <Band id="head">
        <Cell text="Name"/>
        <Cell col="1" text="Address"/>
        <Cell col="2" text="Company"/>
      </Band>

      <!-- Body band: bound to Dataset columns -->
      <Band id="body">
        <Cell text="bind:Name" textAlign="left"/>
        <Cell col="1" text="bind:Address" textAlign="left" wordWrap="char"/>
        <Cell col="2" text="bind:Company" textAlign="left"/>
      </Band>

    </Format>
  </Formats>
</Grid>
```

### Companion Dataset (required)

```xml
<Objects>
  <Dataset id="Dataset00">
    <ColumnInfo>
      <Column id="Name"    type="STRING" size="256"/>
      <Column id="Address" type="STRING" size="256"/>
      <Column id="Company" type="STRING" size="256"/>
    </ColumnInfo>
    <Rows>
      <Row>
        <Col id="Name">John</Col>
        <Col id="Address">Seoul, KOREA</Col>
        <Col id="Company">Acme</Col>
      </Row>
    </Rows>
  </Dataset>
</Objects>
```

## Structure / attributes

### Grid tag

| attribute | type | description |
|---|---|---|
| `binddataset` | string | Dataset `id` that supplies row data |
| `autofittype` | `col` / `none` | Stretch columns to fill grid width |
| `autosizingtype` | `row` / `none` | Auto-expand row height to fit content |
| `selecttype` | `row` / `cell` / `multirow` | Selection granularity |
| `extendsizetype` | `none` / `last` | Which column absorbs extra width |
| `autoenter` | string | `edit` to auto-enter edit mode on click |
| `fillareatype` | string | Fill empty rows below data |

### Formats > Format

One `<Format id="default">` is always required. Multiple formats can be defined and switched at runtime via `Grid.formatid`.

### Columns

One `<Column size="N"/>` per visible column. Order matches `col` index used in `<Cell col="N">`.

### Rows

| attribute | effect |
|---|---|
| `band="head"` | This row template renders in the header band |
| `band="summary"` | This row template renders in the summary (footer) band |
| _(no band attr)_ | Body row template, repeated for each Dataset row |
| `size` | Height in pixels |

### Band / Cell

| attribute | description |
|---|---|
| `id` | `head`, `body`, or `summary` |
| `col` | Zero-based column index of the cell (omit for col 0) |
| `row` | Zero-based row index within the band (omit for row 0) |
| `text` | Static text, or `bind:ColumnId` to bind to Dataset column |
| `displaytype` | `currency`, `date`, `checkbox`, `image`, etc. |
| `edittype` | `normal`, `dropdownlist`, `calendar`, etc. — enables editing |
| `textAlign` | `left` / `center` / `right` |
| `wordWrap` | `char` / `english` / `none` |
| `suppress` | `1` = hide duplicate consecutive values in the column |

### currency displaytype example

```xml
<Cell col="4" text="bind:Salary" displaytype="currency" textAlign="right"/>
```

## Common events

| event | signature | purpose |
|---|---|---|
| `oncellclick` | `(obj, e)` | User clicks a cell; `e.col`, `e.row` give position |
| `oncelldblclick` | `(obj, e)` | Double-click on a cell |
| `oncellchanged` | `(obj, e)` | Cell value committed after edit |
| `onheadclick` | `(obj, e)` | Click on a header cell |
| `onselectchanged` | `(obj, e)` | Selected row/cell changed |

## Notes / Gotchas

- `binddataset` references the Dataset by `id`, not by path. The Dataset must be in the same form's `<Objects>` or accessible via the transaction namespace.
- Column index in `<Cell col="N">` is zero-based and must match the physical order of `<Column>` entries in `<Columns>`.
- A Grid without a `band="head"` `<Row>` will render no header. Always declare it explicitly.
- `displaytype="currency"` formats the number with locale-aware separators; the underlying Dataset value stays numeric.
- `suppress="1"` on a body cell hides repeated identical values visually but does not change data.
- Multiple `<Format>` blocks allow switching between layouts (e.g., compact vs. detailed) at runtime: `Grid00.formatid = "detail";`
- Summary band (`band="summary"`) needs its own `<Row band="summary" size="24"/>` entry in `<Rows>`.
