import unittest
from unittest.mock import MagicMock, patch

import resend

# flake8: noqa


class TestResendContacts(unittest.TestCase):
    def test_contacts_create(self):
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json():
            return {"object": "contact", "id": "479e3145-dd38-476b-932c-529ceb705947"}

        m.json = mock_json
        mock.return_value = m

        params = {
            "audience_id": "48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
            "email": "steve.wozniak@gmail.com",
            "first_name": "Steve",
            "last_name": "Wozniak",
            "unsubscribed": True,
        }
        contact = resend.Contacts.create(params)
        assert contact["id"] == "479e3145-dd38-476b-932c-529ceb705947"
        assert contact["object"] == "contact"

        patcher.stop()

    def test_contacts_update(self):
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json():
            return {
                "object": "contact",
                "id": "479e3145-dd38-476b-932c-529ceb705947",
            }

        m.json = mock_json
        mock.return_value = m

        params = {
            "audience_id": "48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
            "id": "479e3145-dd38-476b-932c-529ceb705947",
            "first_name": "Updated",
            "unsubscribed": True,
        }
        contact = resend.Contacts.update(params)
        assert contact["id"] == "479e3145-dd38-476b-932c-529ceb705947"
        assert contact["object"] == "contact"

        patcher.stop()

    def test_contacts_get(self):
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json():
            return {
                "object": "contact",
                "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                "email": "steve.wozniak@gmail.com",
                "first_name": "Steve",
                "last_name": "Wozniak",
                "created_at": "2023-10-06T23:47:56.678Z",
                "unsubscribed": False,
            }

        m.json = mock_json
        mock.return_value = m

        contact = resend.Contacts.get(
            audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
            id="e169aa45-1ecf-4183-9955-b1499d5701d3",
        )
        assert contact["object"] == "contact"
        assert contact["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"
        assert contact["email"] == "steve.wozniak@gmail.com"
        assert contact["first_name"] == "Steve"
        assert contact["last_name"] == "Wozniak"
        assert contact["created_at"] == "2023-10-06T23:47:56.678Z"
        assert contact["unsubscribed"] is False

        patcher.stop()

    def test_contacts_remove(self):
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json():
            return {
                "object": "contact",
                "id": "520784e2-887d-4c25-b53c-4ad46ad38100",
                "deleted": True,
            }

        m.json = mock_json
        mock.return_value = m

        rmed = resend.Contacts.remove(
            audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
            id="78261eea-8f8b-4381-83c6-79fa7120f1cf",
        )
        assert rmed["object"] == "contact"
        assert rmed["id"] == "520784e2-887d-4c25-b53c-4ad46ad38100"
        assert rmed["deleted"] is True

        patcher.stop()

    def test_contacts_list(self):
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json():
            return {
                "object": "list",
                "data": [
                    {
                        "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                        "email": "steve.wozniak@gmail.com",
                        "first_name": "Steve",
                        "last_name": "Wozniak",
                        "created_at": "2023-10-06T23:47:56.678Z",
                        "unsubscribed": False,
                    }
                ],
            }

        m.json = mock_json
        mock.return_value = m

        contacts = resend.Contacts.list(
            audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8"
        )
        assert contacts["object"] == "list"
        assert contacts["data"][0]["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"
        assert contacts["data"][0]["email"] == "steve.wozniak@gmail.com"
        assert contacts["data"][0]["first_name"] == "Steve"
        assert contacts["data"][0]["last_name"] == "Wozniak"
        assert contacts["data"][0]["created_at"] == "2023-10-06T23:47:56.678Z"
        assert contacts["data"][0]["unsubscribed"] is False

        patcher.stop()
