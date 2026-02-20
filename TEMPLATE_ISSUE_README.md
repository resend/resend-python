# Template HTML Transformation Issue

## Quick Links

- **Full Investigation Report:** [INVESTIGATION_TEMPLATE_HTML_TRANSFORMATION.md](./INVESTIGATION_TEMPLATE_HTML_TRANSFORMATION.md)
- **Python Reproduction Script:** [examples/investigation_template_transformation.py](./examples/investigation_template_transformation.py)
- **Related Issues:** [#186](https://github.com/resend/resend-python/issues/186), [#187](https://github.com/resend/resend-python/issues/187)

## TL;DR

**Problem:** Opening a template in the Resend dashboard causes the HTML to be transformed through React Email and saved back to storage, even when no edits are made. This results in:
- HTML bloat (6-7x size increase)
- Content duplication on subsequent updates
- Loss of exact HTML formatting

**Root Cause:** Dashboard auto-saves React Email-transformed HTML (with `data-id` attributes and comments) instead of preserving the original HTML.

**Status:** Confirmed platform issue, not an SDK bug. The Python SDK is working correctly.

**Workaround:** Avoid opening templates in the dashboard if HTML preservation is critical. Use API-only operations.

## Running the Investigation

To reproduce the issue yourself:

```bash
export RESEND_API_KEY="re_your_api_key"
python examples/investigation_template_transformation.py
```

The script will:
1. Create a template with complex HTML (3,267 chars)
2. Verify HTML is preserved after creation
3. Prompt you to open the template in dashboard
4. Show HTML has been transformed (~21,000+ chars)
5. Demonstrate content duplication on updates

## Proposed Solutions

See the [full investigation report](./INVESTIGATION_TEMPLATE_HTML_TRANSFORMATION.md#proposed-solutions) for detailed solutions, including:

1. **Stop auto-saving transformed HTML** (recommended immediate fix)
2. **Add plain HTML mode** for API-created templates
3. **Make React Email data-id attributes optional**
4. **Template versioning** to store both original and transformed HTML

## For Resend Team

The fix needs to be implemented in the dashboard/platform code (likely a private repository). The specific area to investigate:

```typescript
// Dashboard template editor (pseudo-code)
function onTemplateLoad(template) {
  const transformed = renderThroughReactEmail(template.html);
  saveToStorage(transformed);  // ❌ This line is the problem
  displayInEditor(transformed);
}
```

Should be:

```typescript
function onTemplateLoad(template) {
  const transformed = renderThroughReactEmail(template.html);
  displayInEditor(transformed);  // ✅ Display only, don't auto-save
}
```

## SDK Impact

**No SDK changes are required.** All SDKs (Python, Node.js, etc.) are functioning correctly. The issue is entirely in the platform/dashboard layer.
