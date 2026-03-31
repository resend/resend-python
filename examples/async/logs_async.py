import asyncio
import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


async def main() -> None:
    logs: resend.Logs.ListResponse = await resend.Logs.list_async()
    for log in logs["data"]:
        print(log["id"])
        print(log["endpoint"])
        print(log["method"])
        print(log["response_status"])
        print(log["created_at"])

    print("\n--- Using pagination parameters ---")
    if logs["data"]:
        paginated_params: resend.Logs.ListParams = {
            "limit": 10,
            "after": logs["data"][0]["id"],
        }
        paginated_logs: resend.Logs.ListResponse = await resend.Logs.list_async(
            params=paginated_params
        )
        print(f"Retrieved {len(paginated_logs['data'])} logs with pagination")
        print(f"Has more logs: {paginated_logs['has_more']}")
    else:
        print("No logs available for pagination example")

    print("\n--- Retrieve a single log ---")
    if logs["data"]:
        log_id = logs["data"][0]["id"]
        single_log: resend.Logs.GetResponse = await resend.Logs.get_async(log_id)
        print(f"Log ID: {single_log['id']}")
        print(f"Endpoint: {single_log['endpoint']}")
        print(f"Method: {single_log['method']}")
        print(f"Status: {single_log['response_status']}")
        print(f"Request body: {single_log['request_body']}")
        print(f"Response body: {single_log['response_body']}")


asyncio.run(main())
