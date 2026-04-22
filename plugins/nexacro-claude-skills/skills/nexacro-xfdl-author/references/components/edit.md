# Edit

**Role**: Single-line text input field for user data entry or display.
**Source**: `sample_edit_02.xfdl`

## Minimum XML block

Place inside `<Layout>`:

```xml
<Edit id="edit_input" taborder="1" left="100" top="28" width="360" height="32"
      onkeyup="edit_input_onkeyup" value=""/>
```

### Dataset-bound form (when binding to a Dataset column)

```xml
<Edit id="edit_input" taborder="1" left="100" top="28" width="360" height="32"/>
```

### `<Bind>` (sibling of `<Layouts>`)

```xml
<Bind>
  <BindItem id="bind0" compid="edit_input" propid="value" datasetid="ds_main" columnid="col_name"/>
</Bind>
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
| value | | Initial text value; read/set at runtime via `this.<id>.value` |
| onkeyup | | Name of the key-up event handler |

## Common events

| event | signature | purpose |
|---|---|---|
| onkeyup | `(obj:nexacro.Edit, e:nexacro.KeyEventInfo)` | Fires on each key release; use to react to input changes in real time |
| onchange | `(obj:nexacro.Edit, e:nexacro.ChangeEventInfo)` | Fires when value changes and focus leaves the field |

## Notes

- `value` is the primary property for reading/writing content: `this.edit_input.value`.
- For Dataset-bound usage, omit `value` attribute and use a `<Bind>` block instead.
- Pair with a `<Static>` label component for accessible form layouts.
