# Button

**Role**: Clickable button that triggers an action via `onclick` event handler.
**Source**: `sample_button_02.xfdl`

## Minimum XML block

Place inside `<Layout>`:

```xml
<Button id="btn_ok" taborder="4" text="OK" left="32" top="40" width="120" height="32"
        onclick="btn_ok_onclick" icon="URL(&quot;imagerc::img_sta_des.png&quot;)"/>
```

## Common attributes

| attr | required | description |
|---|---|---|
| id | ✓ | Unique component identifier |
| taborder | ✓ | Tab key focus order |
| text | | Button label text |
| left | ✓ | X position in pixels |
| top | ✓ | Y position in pixels |
| width | ✓ | Width in pixels |
| height | ✓ | Height in pixels |
| onclick | | Name of the click handler function |
| icon | | Image URL using `URL("imagerc::filename")` syntax |

## Common events

| event | signature | purpose |
|---|---|---|
| onclick | `(obj:nexacro.Button, e:nexacro.ClickEventInfo)` | Fires when button is clicked; `e.eventid` contains the event name |

## Notes

- Button is rarely data-bound; no Dataset or Bind sections needed.
- Use `URL("imagerc::filename")` to reference image resources for the `icon` attribute.
- Access the button label at runtime via `obj.text` or `this.<id>.text`.
