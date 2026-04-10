import asyncio
import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


async def main() -> None:
    # Create and publish a template to use in the automation
    print("--- Create and publish template ---")
    tpl: resend.Templates.CreateResponse = await resend.Templates.create_async(
        {
            "name": "welcome-email",
            "subject": "Welcome!",
            "html": "<strong>Welcome to our service!</strong>",
        }
    )
    await resend.Templates.publish_async(tpl["id"])
    print(f"Template: {tpl['id']}")

    # --- Create a simple automation (trigger → send_email) ---
    print("\n--- Create automation ---")
    simple: resend.Automations.CreateResponse = await resend.Automations.create_async(
        {
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
        }
    )
    automation_id = simple["id"]
    print(f"Created automation: {automation_id}")

    # --- Get automation ---
    print("\n--- Get automation ---")
    automation: resend.Automation = await resend.Automations.get_async(automation_id)
    print(f"Name: {automation['name']}, status: {automation['status']}")
    for step in automation["steps"]:
        print(f"  Step key={step['key']} type={step['type']}")

    # --- Update automation ---
    print("\n--- Update automation ---")
    updated: resend.Automations.UpdateResponse = await resend.Automations.update_async(
        {
            "automation_id": automation_id,
            "status": "enabled",
        }
    )
    print(f"Updated: {updated['id']}")

    # --- List automations ---
    print("\n--- List automations ---")
    list_resp: resend.Automations.ListResponse = await resend.Automations.list_async()
    print(f"Total: {len(list_resp['data'])}, has_more: {list_resp['has_more']}")

    # --- Stop automation ---
    print("\n--- Stop automation ---")
    stopped: resend.Automations.StopResponse = await resend.Automations.stop_async(
        automation_id
    )
    print(f"Stopped: {stopped['id']}, status: {stopped['status']}")

    # --- List runs ---
    print("\n--- List runs ---")
    runs: resend.Automations.Runs.ListResponse = (
        await resend.Automations.Runs.list_async(automation_id)
    )
    print(f"Total runs: {len(runs['data'])}")
    if runs["data"]:
        run_id = runs["data"][0]["id"]
        run: resend.AutomationRun = await resend.Automations.Runs.get_async(
            automation_id, run_id
        )
        print(f"Run status: {run['status']}")

    # --- Multi-step automation: delay + wait_for_event ---
    print("\n--- Create multi-step automation (delay + wait_for_event) ---")
    multi: resend.Automations.CreateResponse = await resend.Automations.create_async(
        {
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
        }
    )
    multi_id = multi["id"]
    print(f"Created: {multi_id}")

    retrieved: resend.Automation = await resend.Automations.get_async(multi_id)
    for step in retrieved["steps"]:
        print(f"  Step key={step['key']} type={step['type']} config={step['config']}")

    # --- Cleanup ---
    print("\n--- Cleanup ---")
    del1: resend.Automations.DeleteResponse = await resend.Automations.remove_async(
        automation_id
    )
    print(f"Deleted automation {del1['id']}: {del1['deleted']}")
    del2: resend.Automations.DeleteResponse = await resend.Automations.remove_async(
        multi_id
    )
    print(f"Deleted automation {del2['id']}: {del2['deleted']}")
    await resend.Templates.remove_async(tpl["id"])
    print(f"Deleted template {tpl['id']}")


asyncio.run(main())
