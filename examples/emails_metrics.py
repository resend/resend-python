import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

metrics: resend.Emails.MetricsResponse = resend.Emails.metrics()
print(f"Metrics for {metrics['start_date']} to {metrics['end_date']}")
for metric, value in metrics["totals"].items():
    print(f"{metric}: {value}")

print("\n--- Broken down by period and domain ---")
params: resend.Emails.MetricsParams = {
    "dimensions": ["period", "domain"],
    "metrics": ["sent", "delivered", "opened"],
    "granularity": "daily",
}
breakdown: resend.Emails.MetricsResponse = resend.Emails.metrics(params=params)
for row in breakdown.get("data", []):
    print(row)
