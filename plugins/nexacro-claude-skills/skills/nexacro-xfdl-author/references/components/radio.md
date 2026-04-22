# Radio

**Role**: Renders a group of radio buttons from a dataset, allowing single-option selection.
**Source**: `sample_radio_01.xfdl`

## Minimum XML block

Place inside `<Layout>`:

```xml
<Radio id="radioValue" taborder="0" left="118" top="73" width="280" height="50"
       codecolumn="codecolumn" datacolumn="datacolumn" index="1"
       innerdataset="innerdataset">
  <Dataset id="innerdataset">
    <ColumnInfo>
      <Column id="codecolumn" size="256"/>
      <Column id="datacolumn" size="256"/>
    </ColumnInfo>
    <Rows>
      <Row>
        <Col id="codecolumn">1</Col>
        <Col id="datacolumn">apple</Col>
      </Row>
      <Row>
        <Col id="codecolumn">2</Col>
        <Col id="datacolumn">peach</Col>
      </Row>
    </Rows>
  </Dataset>
</Radio>
```

## Common attributes

| attr | required | description |
|---|---|---|
| id | ✓ | Unique component identifier |
| taborder | ✓ | Tab focus order |
| left / top / width / height | ✓ | Position and size in pixels |
| codecolumn | ✓ | Dataset column name used as the stored value (code) |
| datacolumn | ✓ | Dataset column name used as the display label |
| innerdataset | ✓ | ID of the inline `<Dataset>` child that supplies options |
| index | | Initially selected item index (0-based) |
| direction | | Layout direction: `horizontal` or `vertical` |
| value | | Currently selected code value |

## Common events

| event | signature | purpose |
|---|---|---|
| onitemchanged | `fn(obj:nexacro.Radio, e:nexacro.ItemChangeEventInfo)` | Fires when the selected item changes; read `obj.value` for the new code |

## Notes

- A single `<Radio>` element represents the entire option **group**, not one option.
- The inline `<Dataset>` is a child element of `<Radio>`, not placed in `<Objects>`.
- `codecolumn` is the value stored/returned; `datacolumn` is what the user sees.
- To bind to an external dataset, set `innerdataset` to the dataset id in `<Objects>` and omit the child `<Dataset>`.
