# Investigation: Template HTML Transformation and Content Duplication

**Related Issues:**
- [resend-python#186](https://github.com/resend/resend-python/issues/186) - Templates.create() transforms raw HTML
- [resend-python#187](https://github.com/resend/resend-python/issues/187) - Templates.update() appends HTML instead of replacing it
- Linear: PRODUCT-1427 - Opening template rewrites HTML and duplicates content

**Investigation Date:** February 20, 2026

## Summary

The Resend dashboard template editor processes raw HTML through a React Email rendering pipeline and persists the transformed result back to storage **every time a template is opened**, even when no edits are made. This causes:

1. **HTML Transformation:** Original HTML gets bloated with React Email artifacts (data-id attributes, HTML comments, inline styles)
2. **Content Duplication:** Subsequent updates via API cause content to be duplicated in the editor
3. **Unexpected Behavior:** HTML sent via API differs from what's retrieved after dashboard viewing

## Root Cause Analysis

### The Problem Flow

1. **Create Template via API** (3,267 chars of HTML)
   ```python
   resend.Templates.create({
       "name": "test-template",
       "html": "<html>...</html>"  # Raw HTML
   })
   ```

2. **GET /templates/{id}** → Returns identical HTML (3,267 chars) ✅

3. **Open Template in Dashboard** (no edits, just view it)
   - Dashboard renders HTML through React Email pipeline
   - React Email components add artifacts:
     - `data-id="__react-email-column"` attributes
     - `<!--$-->` and `<!--/$-->` comment markers  
     - Injected inline styles
     - Transformed HTML structure
   - **Dashboard saves transformed HTML back to storage** ❌

4. **GET /templates/{id}** → HTML now ~21,000+ chars ❌

5. **Update via API with original HTML**
   ```python
   resend.Templates.update({
       "id": template_id,
       "html": "<html>...</html>"  # Same original HTML
   })
   ```

6. **Open Dashboard Again** → Content appears duplicated ❌

### Source of Artifacts

Investigation of the [react-email](https://github.com/resend/react-email) repository reveals React Email components hardcode `data-id` attributes:

**packages/column/src/column.tsx:**
```typescript
export const Column = React.forwardRef<HTMLTableCellElement, ColumnProps>(
  ({ children, style, ...props }, ref) => {
    return (
      <td {...props} data-id="__react-email-column" ref={ref} style={style}>
        {children}
      </td>
    );
  },
);
```

**packages/markdown/src/markdown.tsx:**
```typescript
<div data-id="react-email-markdown">
  {/* content */}
</div>
```

When raw HTML is rendered through React Email (even just for viewing), these components inject their attributes and transform the HTML structure.

## Evidence

### Reproduction Script

A [Node.js reproduction script](https://gist.github.com/drish/5352959c0dca9abd96141b301ea317a1) demonstrates:

- API behavior is correct (PATCH replaces HTML exactly as sent)
- Transformation only occurs after opening template in dashboard
- Issue affects both Python SDK and Node.js SDK identically
- **Conclusion: Platform/dashboard issue, not SDK-specific**

### Example Transformation

**Original HTML:**
```html
<table>
  <tr>
    <td>Cell 1</td>
    <td>Cell 2</td>
  </tr>
</table>
```

**After Dashboard View:**
```html
<!--$--><table>
  <tr>
    <td data-id="__react-email-column" style="...">Cell 1</td>
    <td data-id="__react-email-column" style="...">Cell 2</td>
  </tr>
</table><!--/$-->
```

## Impact

### User-Reported Problems

1. **HTML Bloat:** Templates grow 6-7x in size after dashboard viewing
2. **Content Duplication:** Updates cause content to appear multiple times
3. **Unexpected Behavior:** HTML sent via API ≠ HTML retrieved after dashboard interaction
4. **Loss of Control:** Users lose ability to maintain exact HTML structure

### Affected Users

- Users creating templates via API with custom HTML
- Users expecting API to preserve exact HTML formatting
- Users with CSS that relies on specific HTML structure
- Users with dark mode or complex styling (as reported in issues)

## Proposed Solutions

### Solution 1: Prevent Auto-Save on View (Recommended)

**Location:** Dashboard template editor code (private repository)

**Fix:** Only persist HTML changes when user explicitly saves, not on template view/load.

```typescript
// Current (problematic):
function onTemplateLoad(template) {
  const transformed = renderThroughReactEmail(template.html);
  saveToStorage(transformed);  // ❌ Don't do this
  displayInEditor(transformed);
}

// Proposed:
function onTemplateLoad(template) {
  const transformed = renderThroughReactEmail(template.html);
  displayInEditor(transformed);  // ✅ Only display, don't save
}

function onUserSave(editorContent) {
  saveToStorage(editorContent);  // ✅ Only save on explicit user action
}
```

**Benefits:**
- Preserves original HTML until user makes intentional changes
- Fixes both transformation and duplication issues
- No SDK changes required

### Solution 2: Add "plainText" Mode to Dashboard

**Location:** Dashboard template editor code

**Fix:** When loading templates created via API (not through React Email editor), display in plain HTML mode without React Email transformation.

```typescript
function onTemplateLoad(template) {
  if (template.createdViaAPI && !template.usesReactEmailComponents) {
    displayAsPlainHTML(template.html);  // No transformation
  } else {
    const transformed = renderThroughReactEmail(template.html);
    displayInEditor(transformed);
  }
}
```

**Benefits:**
- Preserves API-created templates
- Allows React Email templates to work as expected
- Clear distinction between template types

### Solution 3: Add Render Options to React Email

**Location:** react-email repository

**Fix:** Add option to skip adding `data-id` attributes during rendering.

```typescript
export const Column = React.forwardRef<HTMLTableCellElement, ColumnProps>(
  ({ children, style, includeDataId = true, ...props }, ref) => {
    const dataIdProp = includeDataId ? { 'data-id': '__react-email-column' } : {};
    return (
      <td {...props} {...dataIdProp} ref={ref} style={style}>
        {children}
      </td>
    );
  },
);
```

**Benefits:**
- Allows clean HTML output when needed
- Maintains editor functionality when attributes are included
- Flexible for different use cases

**Drawbacks:**
- Requires changes across multiple React Email components
- May affect editor features that rely on these attributes

### Solution 4: Template Versioning

**Location:** Dashboard backend

**Fix:** Store both original and transformed versions, serve appropriate version based on request source.

```typescript
interface Template {
  id: string;
  name: string;
  originalHtml: string;      // Preserved as submitted via API
  transformedHtml?: string;   // For dashboard editor use
  // ...
}
```

**Benefits:**
- Preserves original HTML for API consumers
- Allows dashboard to work with transformed version
- Non-breaking change

**Drawbacks:**
- Increased storage requirements
- More complex synchronization logic

## Recommended Action Plan

1. **Immediate Fix (Critical):** Implement Solution 1 - Stop auto-saving transformed HTML on template view
2. **Short-term:** Implement Solution 2 - Add plain HTML mode for API-created templates
3. **Long-term:** Consider Solution 4 - Template versioning for robust handling of both API and UI workflows

## SDK Considerations

The Python SDK (and all other SDKs) are working correctly. No SDK changes are required. The issue is entirely in the dashboard/backend platform code.

### Workaround for Users (Until Fix)

Currently, users should:
1. Create/update templates via API
2. **Avoid opening templates in dashboard** if HTML preservation is critical
3. Use the Resend API directly for all template operations

## Testing Recommendations

After implementing fixes, verify:

1. ✅ Template created via API → HTML unchanged after dashboard view
2. ✅ Template updated via API → No content duplication
3. ✅ Template created in dashboard → React Email features work correctly
4. ✅ Template edited in dashboard → Changes saved correctly
5. ✅ API GET returns exact HTML that was PUT/PATCH

## Related Code Repositories

- **resend-python:** SDK confirmed working correctly
- **resend-node:** SDK confirmed working correctly  
- **react-email:** Contains components that add data-id attributes
- **resend-openapi:** API specification (does not indicate transformation behavior)
- **Dashboard (private):** Contains problematic auto-save logic

## Verification

To verify the fix works:

```bash
# Run the reproduction script from the gist
node reproduction-script.js

# Expected results after fix:
# - Original HTML length: 3267 chars
# - After dashboard view: 3267 chars (unchanged)
# - After update: 3267 chars (unchanged)
# - HTML identical to original: true (always)
```

## Contributors

- **Investigation:** João (drish) - identified root cause
- **Reproduction:** Node.js script demonstrating issue
- **Analysis:** Cursor AI Agent - traced issue to React Email component attributes and dashboard auto-save behavior
