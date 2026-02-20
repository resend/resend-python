"""
Investigation Script: Template HTML Transformation Issue

This script demonstrates the issue where opening a template in the Resend dashboard
causes the HTML to be transformed through React Email pipeline and saved back to storage.

Related Issues:
- https://github.com/resend/resend-python/issues/186
- https://github.com/resend/resend-python/issues/187
- Linear: PRODUCT-1427

Usage:
    export RESEND_API_KEY="re_..."
    python examples/investigation_template_transformation.py
"""

import os
import time
from typing import Optional

import resend

# Same HTML used in the Node.js investigation
COMPLEX_HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="color-scheme" content="light dark" />
    <meta name="supported-color-schemes" content="light dark" />
    <style>
      :root {
        color-scheme: light dark;
      }

      /* ── Light mode (default) ── */

      body {
        margin: 0;
        padding: 0;
        background-color: #f5f5f5;
        font-family:
          -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      }

      .wrapper {
        padding: 40px 24px;
      }

      .heading {
        font-size: 24px;
        margin: 0 0 8px 0;
        color: #171717;
      }

      .subtitle {
        font-size: 16px;
        line-height: 1.6;
        margin: 0 0 24px 0;
        color: #525252;
      }

      .data td {
        padding: 12px 16px;
        font-size: 14px;
        color: #171717;
        background-color: #ffffff;
        border: 2px solid #2563eb;
      }

      .data .thead td {
        font-weight: 600;
        color: #ffffff;
        background-color: #2563eb;
        border-color: #2563eb;
      }

      /* ── Dark mode overrides ── */

      @media (prefers-color-scheme: dark) {
        body {
          background-color: #171717;
        }

        .heading {
          color: #f5f5f5;
        }

        .subtitle {
          color: #a3a3a3;
        }

        .data td {
          background-color: #262626;
          border-color: #b91c1c;
          color: #e5e5e5;
        }

        .data .thead td {
          background-color: #b91c1c;
          border-color: #b91c1c;
          color: #ffffff;
        }
      }
    </style>
  </head>

  <body>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td align="center" class="wrapper">
          <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0">
            <tr>
              <td>
                <h1 class="heading">Monthly Report</h1>
                <p class="subtitle">Borders are blue in light mode and red in dark mode.</p>
              </td>
            </tr>
            <tr>
              <td>
                <table class="data" width="100%" cellpadding="0" cellspacing="0" border="0">
                  <tr class="thead">
                    <td>Metric</td>
                    <td>Value</td>
                    <td>Change</td>
                  </tr>
                  <tr>
                    <td>Emails Sent</td>
                    <td>12,450</td>
                    <td>+18%</td>
                  </tr>
                  <tr>
                    <td>Open Rate</td>
                    <td>42.3%</td>
                    <td>+2.1%</td>
                  </tr>
                  <tr>
                    <td>Click Rate</td>
                    <td>8.7%</td>
                    <td>-0.4%</td>
                  </tr>
                  <tr>
                    <td>Bounces</td>
                    <td>23</td>
                    <td>-12</td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>"""


def find_first_diff(a: str, b: str) -> Optional[int]:
    """Find the first character position where two strings differ."""
    min_len = min(len(a), len(b))
    for i in range(min_len):
        if a[i] != b[i]:
            return i
    return min_len if len(a) != len(b) else None


def pause(message: str) -> None:
    """Pause execution and wait for user input."""
    print("\n" + "=" * 60)
    print(f"PAUSE: {message}")
    print("=" * 60)
    input("Press Enter to continue...\n")


def main():
    """Run the investigation."""
    # Ensure API key is set
    resend.api_key = os.environ.get("RESEND_API_KEY")
    if not resend.api_key:
        print("ERROR: RESEND_API_KEY environment variable not set")
        return

    html_length = len(COMPLEX_HTML)
    print(f"Original HTML length: {html_length} chars\n")

    # Step 1: Create template
    print("--- Step 1: Creating template ---")
    timestamp = int(time.time())
    create_params: resend.Templates.CreateParams = {
        "name": f"Investigation Test {timestamp}",
        "subject": "Welcome",
        "html": COMPLEX_HTML,
    }

    created = resend.Templates.create(create_params)
    template_id = created["id"]
    print(f"Created template ID: {template_id}")

    # Step 2: Retrieve via API and compare
    print("\n--- Step 2: Retrieving via API ---")
    fetched = resend.Templates.get(template_id)

    fetched_length = len(fetched["html"])
    html_match = fetched["html"] == COMPLEX_HTML
    print(f"Retrieved HTML length: {fetched_length} chars")
    print(f"HTML identical to original: {html_match}")

    if not html_match:
        print("\nDIFFERENCES FOUND:")
        diff_pos = find_first_diff(COMPLEX_HTML, fetched["html"])
        print(f"First divergence at char: {diff_pos}")

    # Step 3: Pause to check dashboard
    pause(
        "Open the template in the Resend dashboard editor, then press Enter. "
        "The dashboard should show TRANSFORMED HTML (React Email artifacts)."
    )

    # Step 3b: Retrieve AFTER dashboard view to capture the damage
    print("--- Step 3b: Retrieving via API AFTER dashboard view ---")
    after_dashboard = resend.Templates.get(template_id)
    after_dashboard_length = len(after_dashboard["html"])
    after_dashboard_match = after_dashboard["html"] == COMPLEX_HTML
    print(f"After-dashboard HTML length: {after_dashboard_length} chars")
    print(f"HTML identical to original: {after_dashboard_match}")

    if not after_dashboard_match:
        increase = after_dashboard_length / html_length
        print(
            f"Dashboard MUTATED stored HTML: {html_length} -> {after_dashboard_length} chars "
            f"({increase:.1f}x increase)"
        )

        # Check for React Email artifacts
        if "data-id" in after_dashboard["html"]:
            print("  → Detected 'data-id' attributes (React Email artifact)")
        if "<!--$-->" in after_dashboard["html"]:
            print("  → Detected '<!--$-->' comments (React Email artifact)")
        if "__react-email-column" in after_dashboard["html"]:
            print("  → Detected '__react-email-column' (React Email artifact)")

    # Step 4: Update with the same HTML
    print("\n--- Step 4: Updating template with same HTML ---")
    update_params: resend.Templates.UpdateParams = {
        "id": template_id,
        "html": COMPLEX_HTML,
    }
    resend.Templates.update(update_params)
    print("Update response completed")

    # Retrieve again to verify
    after_update = resend.Templates.get(template_id)
    after_update_length = len(after_update["html"])
    after_update_match = after_update["html"] == COMPLEX_HTML
    print(f"After-update HTML length: {after_update_length} chars")
    print(f"HTML identical to original: {after_update_match}")

    if not after_update_match:
        print("\nDIFFERENCES FOUND:")
        diff_pos = find_first_diff(COMPLEX_HTML, after_update["html"])
        print(f"First divergence at char: {diff_pos}")

    # Step 5: Pause to check dashboard for duplication
    pause(
        "Check the Resend dashboard again. The template should now show DUPLICATED content "
        "(full body repeated, separated by <p><br /></p>)."
    )

    # Step 6: Second update to check compounding
    print("--- Step 6: Second update (checking compounding) ---")
    resend.Templates.update(update_params)

    after_update2 = resend.Templates.get(template_id)
    after_update2_length = len(after_update2["html"])
    after_update2_match = after_update2["html"] == COMPLEX_HTML
    print(f"After 2nd update HTML length: {after_update2_length} chars")
    print(f"HTML identical to original: {after_update2_match}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Original HTML:            {html_length} chars")
    print(f"After create (API):       {fetched_length} chars - Match: {html_match}")
    print(
        f"After dashboard view:     {after_dashboard_length} chars - Match: {after_dashboard_match}"
    )
    print(
        f"After update (API):       {after_update_length} chars - Match: {after_update_match}"
    )
    print(
        f"After 2nd update:         {after_update2_length} chars - Match: {after_update2_match}"
    )

    if not after_dashboard_match:
        increase = after_dashboard_length / html_length
        print(f"\nKEY FINDING: Opening the dashboard editor mutated stored HTML")
        print(
            f"from {html_length} to {after_dashboard_length} chars ({increase:.1f}x increase)."
        )
        print("The API never transforms HTML — the dashboard's React Email")
        print("rendering layer rewrites stored data on every view.")

    if html_match and after_update_match and after_update2_match:
        print("\nAPI behavior is correct — PATCH replaces HTML exactly as sent.")
        print(
            "Both #186 and #187 are caused by the dashboard editor, not the API or SDK."
        )

    # Step 7: Cleanup
    print("\n--- Cleanup: Removing template ---")
    try:
        resend.Templates.remove(template_id)
        print("Template removed successfully.")
    except Exception as e:
        print(f"Remove failed: {e}")


if __name__ == "__main__":
    main()
