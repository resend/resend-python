import asyncio
import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# Set up async HTTP client
resend.default_http_client = resend.HTTPXClient()


async def main() -> None:
    create_params: resend.Segments.CreateParams = {
        "name": "New Segment from Python SDK (Async)",
    }
    segment: resend.Segments.CreateSegmentResponse = await resend.Segments.create_async(
        create_params
    )
    print(f"Created segment: {segment['id']}")
    print(segment)

    seg: resend.Segment = await resend.Segments.get_async(segment["id"])
    print("Retrieved segment: ", seg)

    segments: resend.Segments.ListResponse = await resend.Segments.list_async()
    print("List of segments:", [s["id"] for s in segments["data"]])

    rmed: resend.Segments.RemoveSegmentResponse = await resend.Segments.remove_async(
        id=segment["id"]
    )
    print("Deleted segment")
    print(rmed)


if __name__ == "__main__":
    asyncio.run(main())
