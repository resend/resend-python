import asyncio
import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# Set up async HTTP client

# replace with some audience id
audience_id: str = "ca4e37c5-a82a-4199-a3b8-bf912a6472aa"


async def main() -> None:
    create_params: resend.Contacts.CreateParams = {
        "audience_id": audience_id,
        "email": "sw@exmple.com",
        "first_name": "Steve",
        "last_name": "Wozniak",
        "unsubscribed": False,
    }

    contact: resend.Contacts.CreateContactResponse = await resend.Contacts.create_async(
        create_params
    )
    print("Created contact !")
    print(contact)

    update_params: resend.Contacts.UpdateParams = {
        "audience_id": audience_id,
        "id": contact["id"],
        "unsubscribed": False,
        "first_name": "Steve (Async)",
    }

    updated: resend.Contacts.UpdateContactResponse = await resend.Contacts.update_async(
        update_params
    )
    print("updated contact !")
    print(updated)

    cont_by_id: resend.Contact = await resend.Contacts.get_async(
        id=contact["id"], audience_id=audience_id
    )
    print("Retrieved contact by ID")
    print(cont_by_id)

    cont_by_email: resend.Contact = await resend.Contacts.get_async(
        email="sw@exmple.com", audience_id=audience_id
    )
    print("Retrieved contact by Email")
    print(cont_by_email)

    contacts: resend.Contacts.ListResponse = await resend.Contacts.list_async(
        audience_id=audience_id
    )
    print("List of contacts")
    for c in contacts["data"]:
        print(c)

    # remove by email
    rmed = await resend.Contacts.remove_async(
        audience_id=audience_id, email=cont_by_email["email"]
    )

    # remove by id
    # rmed: resend.Contact = await resend.Contacts.remove_async(audience_id=audience_id, id=cont["id"])

    print(f"Removed contact")
    print(rmed)


if __name__ == "__main__":
    asyncio.run(main())
