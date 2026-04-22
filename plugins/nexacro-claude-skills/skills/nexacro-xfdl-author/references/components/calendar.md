# Calendar

**Role**: Full month-view calendar widget for date display and selection.
**Source**: `sample_calendar_01.xfdl`

## Minimum XML block

Place inside `<Layout>`:

```xml
<Calendar id="calDisplay" taborder="5"
          left="120" top="128" width="269" height="32"
          value="20160601"/>
```

## Common attributes

| attr | required | description |
|---|---|---|
| id | ✓ | Unique component identifier |
| taborder | ✓ | Tab focus order |
| left / top / width / height | ✓ | Position and size in pixels |
| value | | Initially selected date in `YYYYMMDD` format |
| dateformat | | Display format string (e.g. `"yyyy/MM/dd"`); set via script or attribute |
| locale | | Locale string that controls day/month names (e.g. `"ko-KR"`); set via script or attribute |

## Common events

| event | signature | purpose |
|---|---|---|
| onchanged | `fn(obj:nexacro.Calendar, e:nexacro.ChangeEventInfo)` | Fires when the selected date changes |

## Notes

- `value` is stored and returned in `YYYYMMDD` (8-digit) format.
- `dateformat` and `locale` can be changed at runtime via script (see sample's `btnChange_onclick`).
- The sample shows a pattern where `<Edit>` fields drive `locale` and `dateformat` updates:

```javascript
this.calDisplay.locale = this.editLocale.value;
this.calDisplay.dateformat = this.editDateformat.value;
```

- Calendar renders as a visible expanded month grid; for a compact picker use `DateField` instead.
