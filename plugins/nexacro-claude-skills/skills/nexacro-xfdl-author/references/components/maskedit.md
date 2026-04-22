# MaskEdit

**Role**: Single-line input field with a format mask that constrains and formats user input.
**Source**: `sample_maskedit_02.xfdl`

## Minimum XML block

Place inside `<Layout>`:

```xml
<!-- String mask example -->
<MaskEdit id="maskedit_string" taborder="0" left="116" top="36" width="200" height="32"
          type="string" value="abcd12345" textAlign="left" format="aaaa - #####"/>

<!-- Number mask example -->
<MaskEdit id="maskedit_number" taborder="1" left="116" top="84" width="200" height="32"
          value="1234567.890" format="#,#.###"/>
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
| format | ✓ | Mask pattern — `a` = alpha char, `#` = digit, `,` = thousands sep, `.` = decimal sep |
| type | | `"string"` for alpha-numeric masks; omit for numeric masks |
| value | | Initial value; must conform to the mask pattern |
| textAlign | | Horizontal alignment: `"left"`, `"center"`, `"right"` |

## Common events

| event | signature | purpose |
|---|---|---|
| onchange | `(obj:nexacro.MaskEdit, e:nexacro.ChangeEventInfo)` | Fires when the formatted value changes |

## Notes

- `format` mask characters: `a` = any letter, `#` = any digit, literal characters (spaces, dashes, commas, dots) are inserted automatically.
- String-type mask example: `"aaaa - #####"` — user types letters then digits; dashes and spaces are fixed.
- Number-type mask example: `"#,#.###"` — renders thousands separators and decimal places automatically.
- `type="string"` must be set when the mask contains alphabetic placeholders (`a`); omit for pure numeric masks.
- No Dataset or Bind sections are typically needed; value is managed directly via the `value` attribute.
