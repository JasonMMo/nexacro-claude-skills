# Static

**Role**: Non-interactive text label for displaying static or dynamically evaluated text.
**Source**: `sample_static_01.xfdl`

## Minimum XML block

Place inside `<Layout>`:

```xml
<Static id="staticExpr" taborder="0" text="test"
        left="185" top="24" width="351" height="65"
        expr="comp.parent.fn_dateTostr()"/>
```

## Common attributes

| attr | required | description |
|---|---|---|
| id | ✓ | Unique component identifier |
| left / top / width / height | ✓ | Position and size in pixels |
| text | | Static label text displayed when `expr` is not set |
| expr | | XScript expression evaluated at runtime; result replaces `text` display |
| taborder | | Tab order (typically set but Static is non-interactive) |

## Notes

- `Static` has no interaction events — it is display-only.
- The `expr` attribute accepts an XScript expression string. It is re-evaluated when changed at runtime:

```javascript
this.staticExpr.expr = "comp.parent.fn_checkBrowser()";
```

- Common pattern: use `expr` to display dynamic values (today's date, browser info, OS version) without binding to a dataset.
- Use `Static` for form labels in front of `Edit`, `Combo`, or other input components.
- Unlike `Edit`, `Static` cannot receive keyboard focus for data entry.
