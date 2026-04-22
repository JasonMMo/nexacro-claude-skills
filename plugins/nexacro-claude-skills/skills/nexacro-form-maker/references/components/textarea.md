# TextArea

**Role**: Multi-line text input field supporting word-wrap and scrollable long-form text.
**Source**: `sample_textarea_01.xfdl`

## Minimum XML block

Place inside `<Layout>`:

```xml
<TextArea id="textareaWordwarp" taborder="1" left="44" top="50" width="278" height="99"
          value="Lorem ipsum dolor sit amet..."/>
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
| value | | Initial multi-line text content |
| wordWrap | | Word-wrap mode: `"none"`, `"char"`, `"english"` — settable at runtime |

## Common events

| event | signature | purpose |
|---|---|---|
| onchange | `(obj:nexacro.TextArea, e:nexacro.ChangeEventInfo)` | Fires when text content changes |

## Notes

- `wordWrap` is set at runtime in the sample: `this.textareaWordwarp.wordWrap = value;`
- Valid `wordWrap` values from the sample: `"none"` (no wrapping), `"char"` (wrap at any character), `"english"` (wrap at word boundaries).
- Unlike `Edit`, TextArea supports multi-line content natively — no special configuration needed.
- `value` holds the full text string including embedded newlines.
- No Dataset or Bind sections are required for standalone usage.
