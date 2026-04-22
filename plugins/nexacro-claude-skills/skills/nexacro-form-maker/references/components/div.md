# Div

**Role**: Rectangular container that either holds inline child components or loads a separate `.xfdl` sub-form at runtime.
**Source**: `sample_div_01.xfdl`

## Minimum XML block

Placed inside `<Layout>` within the parent form's `<Layouts>`.

### Pattern 1 — Inline container

```xml
<Div id="divMain" left="30" top="100" width="300" height="300">
  <Layouts>
    <Layout>
      <Button id="Button00" text="Button00" left="54" top="61" width="99" height="48"/>
    </Layout>
  </Layouts>
</Div>
```

Child components are declared inside the Div's own `<Layouts><Layout>` block.
Coordinates inside the Div are relative to the Div's top-left corner (0, 0).

### Pattern 2 — Sub-form loader

```xml
<Div id="divMain" left="30" top="100" width="300" height="300" url="Sample::sample_div_01_left.xfdl"/>
```

`url` is set at design time or assigned at runtime via script. Setting `url = null` unloads the sub-form and returns the Div to an empty state.

## Structure / attributes

| attribute | type | description |
|---|---|---|
| `id` | string | Unique identifier within the form |
| `left`, `top` | int | Position relative to parent layout |
| `width`, `height` | int | Dimensions in pixels |
| `url` | string | `Alias::filename.xfdl` — loads a sub-form (Pattern 2 only) |
| `text` | string | Optional label rendered on the Div border |
| `taborder` | int | Tab-key navigation order |

## Common events

| event | signature | purpose |
|---|---|---|
| `onload` | `(obj, e)` | Fires after the sub-form URL has fully loaded |
| `onunload` | `(obj, e)` | Fires before the current sub-form is removed |

## Notes / Gotchas

- A Div using `url` must NOT have a `<Layouts>` child — the sub-form provides its own layout.
- Child component IDs inside a Div are scoped to the Div: access them as `this.divMain.Button00`.
- Setting `url` at runtime replaces the previous sub-form; the old sub-form's script context is destroyed.
- The two patterns are mutually exclusive per Div instance.
