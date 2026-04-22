# CheckBox

**Role**: Boolean toggle control that stores one of two configurable values.
**Source**: `sample_checkbox_02.xfdl`

## Minimum XML block

Place inside `<Layout>`:

```xml
<CheckBox id="CheckBox00" taborder="0" text="CheckBox00"
          left="32" top="40" width="120" height="20"
          truevalue="Yes" falsevalue="No" value="No"/>
```

## Dataset companion

Place inside `<Objects>`:

```xml
<Dataset id="Dataset00">
  <ColumnInfo>
    <Column id="Status" type="STRING" size="256"/>
  </ColumnInfo>
  <Rows>
    <Row>
      <Col id="Status">Yes</Col>
    </Row>
  </Rows>
</Dataset>
```

## Bind companion

Place inside `<Bind>`:

```xml
<BindItem id="item0" compid="CheckBox00" propid="value"
          datasetid="Dataset00" columnid="Status"/>
```

## Common attributes

| attr | required | description |
|---|---|---|
| id | ✓ | Unique component identifier |
| taborder | ✓ | Tab focus order |
| left / top / width / height | ✓ | Position and size in pixels |
| text | | Label displayed next to the checkbox |
| truevalue | | Value stored when checkbox is checked (e.g. `"Yes"`, `"1"`) |
| falsevalue | | Value stored when checkbox is unchecked (e.g. `"No"`, `"0"`) |
| value | | Current value; compared against `truevalue`/`falsevalue` |

## Common events

| event | signature | purpose |
|---|---|---|
| onchanged | `fn(obj:nexacro.CheckBox, e:nexacro.ChangeEventInfo)` | Fires when the checked state changes |

## Notes

- `value` is compared to `truevalue` to determine checked state; defaults differ from `true`/`false` — always set both explicitly.
- Binding via `<BindItem propid="value">` keeps the checkbox in sync with a dataset column bidirectionally.
- The sample also binds the same column to an `<Edit>` to show the live stored value.
