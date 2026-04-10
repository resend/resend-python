import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# Create and publish a template to use in the automation
print("--- Create and publish template ---")
tpl: resend.Templates.CreateResponse = resend.Templates.create({
    "name": "welcome-email",
    "subject": "Welcome!",
    "html": "<strong>Welcome to our service!</strong>",
})
resend.Templates.publish(tpl["id"])
print(f"Template: {tpl['id']}")

# --- Create a simple automation (trigger → send_email) ---
print("\n--- Create automation ---")
simple: resend.Automations.CreateResponse = resend.Automations.create({
    "name": "Welcome Flow",
    "status": "disabled",
    "steps": [
        {
            "key": "trigger_1",
            "type": "trigger",
            "config": {"event_name": "user.created"},
        },
        {
            "key": "send_1",
            "type": "send_email",
            "config": {"template": {"id": tpl["id"]}},
        },
    ],
    "connections": [
        {"from": "trigger_1", "to": "send_1"},
    ],
})
automation_id = simple["id"]
print(f"Created automation: {automation_id}")

# --- Get automation ---
print("\n--- Get automation ---")
automation: resend.Automation = resend.Automations.get(automation_id)
print(f"Name: {automation['name']}, status: {automation['status']}")
for step in automation["steps"]:
    print(f"  Step key={step['key']} type={step['type']}")
for conn in automation["connections"]:
    print(f"  Connection: {conn['from']} -> {conn['to']}")

# --- Update automation ---
print("\n--- Update automation ---")
updated: resend.Automations.UpdateResponse = resend.Automations.update({
    "automation_id": automation_id,
    "status": "enabled",
})
print(f"Updated: {updated['id']}")

# --- List automations ---
print("\n--- List automations ---")
list_resp: resend.Automations.ListResponse = resend.Automations.list()
print(f"Total: {len(list_resp['data'])}, has_more: {list_resp['has_more']}")

list_enabled: resend.Automations.ListResponse = resend.Automations.list(
    params={"status": "enabled", "limit": 10}
)
print(f"Enabled: {len(list_enabled['data'])}")

# --- Stop automation ---
print("\n--- Stop automation ---")
stopped: resend.Automations.StopResponse = resend.Automations.stop(automation_id)
print(f"Stopped: {stopped['id']}, status: {stopped['status']}")

# --- List runs ---
print("\n--- List runs ---")
runs: resend.Automations.ListRunsResponse = resend.Automations.list_runs(automation_id)
print(f"Total runs: {len(runs['data'])}")
if runs["data"]:
    run_id = runs["data"][0]["id"]
    run: resend.AutomationRun = resend.Automations.get_run(automation_id, run_id)
    print(f"Run status: {run['status']}, steps: {len(run['steps'])}")
    for step in run["steps"]:
        print(f"  Step key={step['key']} type={step['type']} status={step['status']}")

# --- Multi-step automation: delay + wait_for_event ---
print("\n--- Create multi-step automation (delay + wait_for_event) ---")
multi: resend.Automations.CreateResponse = resend.Automations.create({
    "name": "Onboarding Flow",
    "status": "disabled",
    "steps": [
        {
            "key": "trigger_1",
            "type": "trigger",
            "config": {"event_name": "user.created"},
        },
        {
            "key": "delay_1",
            "type": "delay",
            # duration is a human-readable string; "seconds" (int) is also accepted
            "config": {"duration": "30 minutes"},
        },
        {
            "key": "wait_1",
            "type": "wait_for_event",
            # timeout is a human-readable string; timeout_seconds is NOT supported
            "config": {"event_name": "user.verified", "timeout": "1 hour"},
        },
        {
            "key": "send_1",
            "type": "send_email",
            "config": {"template": {"id": tpl["id"]}},
        },
    ],
    "connections": [
        {"from": "trigger_1", "to": "delay_1"},
        {"from": "delay_1", "to": "wait_1"},
        {"from": "wait_1", "to": "send_1", "type": "event_received"},
        {"from": "wait_1", "to": "send_1", "type": "timeout"},
    ],
})
multi_id = multi["id"]
print(f"Created: {multi_id}")

retrieved: resend.Automation = resend.Automations.get(multi_id)
for step in retrieved["steps"]:
    print(f"  Step key={step['key']} type={step['type']} config={step['config']}")

# --- Delete automations and template ---
print("\n--- Cleanup ---")
del1: resend.Automations.DeleteResponse = resend.Automations.remove(automation_id)
print(f"Deleted automation {del1['id']}: {del1['deleted']}")
del2: resend.Automations.DeleteResponse = resend.Automations.remove(multi_id)
print(f"Deleted automation {del2['id']}: {del2['deleted']}")
resend.Templates.remove(tpl["id"])
print(f"Deleted template {tpl['id']}")
