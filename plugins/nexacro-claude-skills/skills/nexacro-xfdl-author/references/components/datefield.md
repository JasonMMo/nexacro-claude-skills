# DateField

**Role**: Compact input field for date or time entry, with optional dropdown picker.
**Source**: `sample_datefield_01.xfdl`

## Minimum XML block

Place inside `<Layout>`:

```xml
<DateField id="DateField00" taborder="0"
           left="50" top="50" width="150" height="60"
           inputtype="time" format="h:mm:ss aa"/>
```

## Common attributes

| attr | required | description |
|---|---|---|
| id | ✓ | Unique component identifier |
| taborder | ✓ | Tab focus order |
| left / top / width / height | ✓ | Position and size in pixels |
| inputtype | | Input mode: `"date"` (default) or `"time"` |
| format | | Display/input format string (e.g. `"h:mm:ss aa"`, `"yyyy-MM-dd"`) |
| value | | Current date/time value |

## Common events

| event | signature | purpose |
|---|---|---|
| ondropdown | `fn(obj:nexacro.DateField, e:nexacro.EventInfo)` | Fires when the dropdown arrow is clicked; call `e.preventDefault()` to suppress default picker and show a custom one |
| onchanged | `fn(obj:nexacro.DateField, e:nexacro.ChangeEventInfo)` | Fires when the value changes |

## Notes

- Use `inputtype="time"` with a time `format` (e.g. `"h:mm:ss aa"`) for time-only input.
- The sample demonstrates a custom popup pattern via `PopupDateRangePicker`: intercept `ondropdown`, call `trackPopupByComponent`, then set `value` from the picker's `ondayclick` event:

```javascript
this.DateField01_ondropdown = function(obj, e) {
    this.PopupDateRangePicker00.trackPopupByComponent("start", obj, 0, 33);
    e.preventDefault();
};
this.PopupDateRangePicker00_ondayclick = function(obj, e) {
    this.DateField01.value = e.date;
};
```

- Unlike `Calendar`, `DateField` is an inline text input — the calendar popup appears only on demand.
