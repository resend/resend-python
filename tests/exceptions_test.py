import unittest

import pytest

from resend.exceptions import (ApplicationError, MissingApiKeyError,
                               RateLimitError, ResendError, ValidationError,
                               raise_for_code_and_type)


class TestResendError(unittest.TestCase):
    def test_raise_when_unknown_error(self) -> None:
        with pytest.raises(ResendError) as e:
            raise_for_code_and_type(999, "error_type", "msg")
        assert e.type is ResendError

    def test_raise_known_error(self) -> None:
        with pytest.raises(MissingApiKeyError) as e:
            raise_for_code_and_type(401, "missing_api_key", "err")
        assert e.type is MissingApiKeyError

    def test_validation_error_from_422(self) -> None:
        with pytest.raises(ValidationError) as e:
            raise_for_code_and_type(422, "validation_error", "err")
        assert e.type is ValidationError

    def test_validation_error_from_400(self) -> None:
        with pytest.raises(ValidationError) as e:
            raise_for_code_and_type(400, "validation_error", "err")
        assert e.type is ValidationError

    def test_error_500(self) -> None:
        with pytest.raises(ApplicationError) as e:
            raise_for_code_and_type(500, "application_error", "err")
        assert e.type is ApplicationError

    def test_rate_limit_exceeded_error(self) -> None:
        with pytest.raises(RateLimitError) as e:
            raise_for_code_and_type(429, "rate_limit_exceeded", "Rate limit exceeded")
        assert e.type is RateLimitError
        assert e.value.code == 429
        assert e.value.error_type == "rate_limit_exceeded"

    def test_daily_quota_exceeded_error(self) -> None:
        with pytest.raises(RateLimitError) as e:
            raise_for_code_and_type(429, "daily_quota_exceeded", "Daily quota exceeded")
        assert e.type is RateLimitError
        assert e.value.code == 429
        assert e.value.error_type == "daily_quota_exceeded"

    def test_monthly_quota_exceeded_error(self) -> None:
        with pytest.raises(RateLimitError) as e:
            raise_for_code_and_type(429, "monthly_quota_exceeded", "Monthly quota exceeded")
        assert e.type is RateLimitError
        assert e.value.code == 429
        assert e.value.error_type == "monthly_quota_exceeded"
