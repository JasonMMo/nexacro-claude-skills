# Combo

**Role**: Drop-down selection component driven by an inline or external Dataset.
**Source**: `sample_combo_02.xfdl`

## Minimum XML block

Place inside `<Layout>`:

```xml
<Combo id="Combo00" taborder="0" left="32" top="40" width="200" height="32"
       codecolumn="codecolumn" datacolumn="datacolumn"
       innerdataset="innerdataset" index="0" value="00" text="apple" readonly="false">
  <Dataset id="innerdataset">
    <ColumnInfo>
      <Column id="codecolumn" size="256"/>
      <Column id="datacolumn" size="256"/>
    </ColumnInfo>
    <Rows>
      <Row>
        <Col id="codecolumn">00</Col>
        <Col id="datacolumn">apple</Col>
      </Row>
      <Row>
        <Col id="codecolumn">01</Col>
        <Col id="datacolumn">banana</Col>
      </Row>
    </Rows>
  </Dataset>
</Combo>
```

### Companion `<Dataset>` (alternative — place inside `<Objects>` for shared use)

```xml
<Dataset id="ds_combo">
  <ColumnInfo>
    <Column id="codecolumn" size="256"/>
    <Column id="datacolumn" size="256"/>
  </ColumnInfo>
  <Rows>
    <Row>
      <Col id="codecolumn">00</Col>
      <Col id="datacolumn">apple</Col>
    </Row>
  </Rows>
</Dataset>
```

## Common attributes

| attr | required | description |
|---|---|---|
| id | ✓ | Unique component identifier |
| taborder | ✓ | Tab key focus order |
| left | ✓ | X position in pixels |
| top | ✓ | Y position in pixels |
| width | ✓ | Width in pixels |
| height | ✓ | Height in pixels |
| innerdataset | ✓ | ID of the Dataset supplying list items |
| codecolumn | ✓ | Dataset column used as the stored value (`value`) |
| datacolumn | ✓ | Dataset column used as the display label (`text`) |
| index | | Initially selected row index (0-based) |
| value | | Initially selected code value |
| text | | Display text matching the initial selection |
| readonly | | `"false"` allows typing to filter; `"true"` forces list-only selection |

## Common events

| event | signature | purpose |
|---|---|---|
| onitemchanged | `(obj:nexacro.Combo, e:nexacro.ItemChangeEventInfo)` | Fires when selected item changes |

## Notes

- The inline `<Dataset id="innerdataset">` is nested directly inside `<Combo>` — this is the simplest pattern.
- For a Dataset shared across multiple components, place it in `<Objects>` and reference it by ID in `innerdataset`.
- `value` returns the `codecolumn` value; `text` returns the `datacolumn` display string.
- Always specify both `codecolumn` and `datacolumn` — the Combo will not render items without them.
