import unittest

import pytest

from resend.exceptions import (MissingApiKeyError, ResendError,
                               ValidationError,
                               raise_for_code_and_type)


class TestResendError(unittest.TestCase):
    def test_raise_when_unknown_error(self):
        with pytest.raises(ResendError) as e:
            raise_for_code_and_type(999, "error_type", "msg")
        assert e.type is ResendError

    def test_raise_known_error(self):
        with pytest.raises(MissingApiKeyError) as e:
            raise_for_code_and_type(401, "missing_api_key", "err")
        assert e.type is MissingApiKeyError

    def test_validation_error_from_422(self):
        with pytest.raises(ValidationError) as e:
            raise_for_code_and_type(422, "validation_error", "err")
        assert e.type is ValidationError

    def test_validation_error_from_400(self):
        with pytest.raises(ValidationError) as e:
            raise_for_code_and_type(400, "validation_error", "err")
        assert e.type is ValidationError
