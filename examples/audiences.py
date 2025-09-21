import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


create_params: resend.Audiences.CreateParams = {
    "name": "New Audience from Python SDK",
}
audience: resend.Audiences.CreateAudienceResponse = resend.Audiences.create(
    create_params
)
print(f"Created audience: {audience['id']}")
print(audience)

aud: resend.Audience = resend.Audiences.get(audience["id"])
print("Retrieved audience: ", aud)

audiences: resend.Audiences.ListResponse = resend.Audiences.list()
print("List of audiences:", [a["id"] for a in audiences["data"]])
print(f"Has more audiences: {audiences['has_more']}")

print("\n--- Using pagination parameters ---")
if audiences["data"]:
    paginated_params: resend.Audiences.ListParams = {
        "limit": 5,
        "after": audiences["data"][0]["id"],
    }
    paginated_audiences: resend.Audiences.ListResponse = resend.Audiences.list(
        params=paginated_params
    )
    print(f"Retrieved {len(paginated_audiences['data'])} audiences with pagination")
    print(f"Has more audiences: {paginated_audiences['has_more']}")
else:
    print("No audiences available for pagination example")

rmed: resend.Audiences.RemoveAudienceResponse = resend.Audiences.remove(
    id=audience["id"]
)
print(f"Deleted audience with ID: {audience['id']}")
print(rmed)
