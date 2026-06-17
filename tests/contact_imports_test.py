import resend
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestContactImports(ResendBaseTest):
    def test_create_contact_import(self) -> None:
        self.set_mock_json(
            {"object": "contact_import", "id": "479e3145-dd38-476b-932c-529ceb705947"}
        )

        params: resend.Contacts.Imports.CreateParams = {
            "file": b"email,first_name\nsteve@example.com,Steve",
        }
        resp: resend.Contacts.Imports.CreateContactImportResponse = resend.Contacts.Imports.create(params)
        assert resp["id"] == "479e3145-dd38-476b-932c-529ceb705947"
        assert resp["object"] == "contact_import"

    def test_create_contact_import_with_options(self) -> None:
        self.set_mock_json(
            {"object": "contact_import", "id": "479e3145-dd38-476b-932c-529ceb705947"}
        )

        params: resend.Contacts.Imports.CreateParams = {
            "file": b"email,first_name\nsteve@example.com,Steve",
            "filename": "contacts.csv",
            "on_conflict": "upsert",
            "column_map": {"email": "email", "first_name": "first_name"},
            "segments": ["seg-123"],
        }
        resp = resend.Contacts.Imports.create(params)
        assert resp["id"] == "479e3145-dd38-476b-932c-529ceb705947"

    def test_create_contact_import_missing_file(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            resend.Contacts.Imports.create({"file": b""})
        assert str(ctx.exception) == "file is required"

    def test_get_contact_import(self) -> None:
        self.set_mock_json(
            {
                "object": "contact_import",
                "id": "479e3145-dd38-476b-932c-529ceb705947",
                "status": "completed",
                "created_at": "2023-10-06T23:47:56.678Z",
                "counts": {
                    "total": 100,
                    "created": 80,
                    "updated": 10,
                    "skipped": 5,
                    "failed": 5,
                },
            }
        )

        result: resend.ContactImport = resend.Contacts.Imports.get(
            "479e3145-dd38-476b-932c-529ceb705947"
        )
        assert result["id"] == "479e3145-dd38-476b-932c-529ceb705947"
        assert result["status"] == "completed"
        counts = result["counts"]
        assert counts is not None
        assert counts["total"] == 100

    def test_get_contact_import_missing_id(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            resend.Contacts.Imports.get("")
        assert str(ctx.exception) == "id is required"

    def test_list_contact_imports(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "object": "contact_import",
                        "id": "479e3145-dd38-476b-932c-529ceb705947",
                        "status": "completed",
                        "created_at": "2023-10-06T23:47:56.678Z",
                    }
                ],
            }
        )

        result: resend.Contacts.Imports.ListContactImportsResponse = resend.Contacts.Imports.list()
        assert result["object"] == "list"
        assert result["has_more"] is False
        assert len(result["data"]) == 1
        assert result["data"][0]["id"] == "479e3145-dd38-476b-932c-529ceb705947"

    def test_list_contact_imports_with_filters(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [],
            }
        )

        result = resend.Contacts.Imports.list(
            {"status": "completed", "limit": 10}
        )
        assert result["object"] == "list"
