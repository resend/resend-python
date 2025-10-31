import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# Create a new segment
create_params: resend.Segments.CreateParams = {
    "name": "VIP Newsletter Subscribers",
}
segment: resend.Segments.CreateSegmentResponse = resend.Segments.create(create_params)
print(f"\n✓ Created segment: {segment['id']}")
print(f"  Name: {segment['name']}")

# Get segment details
seg: resend.Segment = resend.Segments.get(segment["id"])
print(f"\n✓ Retrieved segment: {seg['name']}")
print(f"  Created at: {seg['created_at']}")

# List all segments
segments: resend.Segments.ListResponse = resend.Segments.list()
print(f"\n✓ List of segments: {[s['name'] for s in segments['data']]}")
print(f"  Has more: {segments['has_more']}")

# List with pagination
if segments["data"]:
    paginated_params: resend.Segments.ListParams = {
        "limit": 5,
        "after": segments["data"][0]["id"],
    }
    paginated_segments: resend.Segments.ListResponse = resend.Segments.list(
        params=paginated_params
    )
    print(f"\n✓ Paginated results: {len(paginated_segments['data'])} segments")

# First, create a contact (using the legacy audience_id approach)
# Note: Contacts API still uses audience_id, not segment_id
contact_params: resend.Contacts.CreateParams = {
    "audience_id": segment["id"],  # Segments and audiences are now the same
    "email": "vip@example.com",
    "first_name": "VIP",
    "last_name": "User",
}
contact = resend.Contacts.create(contact_params)
print(f"\n✓ Created contact: {contact['id']}")

# Add contact to segment (using the new Contacts.segments sub-API)
add_params: resend.ContactSegments.AddParams = {
    "segment_id": segment["id"],
    "contact_id": contact["id"],
}
add_response = resend.Contacts.Segments.add(add_params)
print(f"\n✓ Added contact to segment: {add_response['id']}")

# Alternative: Add by email instead of contact_id
add_by_email_params: resend.ContactSegments.AddParams = {
    "segment_id": segment["id"],
    "email": "another-vip@example.com",
}
# add_response2 = resend.Contacts.Segments.add(add_by_email_params)
# print(f"✓ Added contact (by email) to segment: {add_response2['id']}")

# List all segments for a contact
list_params: resend.ContactSegments.ListParams = {
    "contact_id": contact["id"],
}
contact_segments = resend.Contacts.Segments.list(list_params)
print(f"\n✓ Contact is in {len(contact_segments['data'])} segment(s):")
for cs in contact_segments["data"]:
    print(f"  - {cs['name']} (ID: {cs['id']})")

# Alternative: List by email
list_by_email_params: resend.ContactSegments.ListParams = {
    "email": "vip@example.com",
}
# contact_segments2 = resend.Contacts.Segments.list(list_by_email_params)

# Remove contact from segment
remove_params: resend.ContactSegments.RemoveParams = {
    "segment_id": segment["id"],
    "contact_id": contact["id"],
}
remove_response = resend.Contacts.Segments.remove(remove_params)
print(f"\n✓ Removed contact from segment")
print(f"  Deleted: {remove_response['deleted']}")

# Clean up: Remove the contact
resend.Contacts.remove(audience_id=segment["id"], id=contact["id"])
print(f"\n✓ Deleted contact: {contact['id']}")

# Clean up: Remove the segment
rmed: resend.Segments.RemoveSegmentResponse = resend.Segments.remove(id=segment["id"])
print(f"\n✓ Deleted segment: {segment['id']}")
print(f"  Deleted: {rmed['deleted']}")
