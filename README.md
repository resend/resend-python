# Resend Python SDK

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Build](https://github.com/drish/resend-py/actions/workflows/ci.yaml/badge.svg)
[![codecov](https://codecov.io/gh/drish/resend-py/branch/main/graph/badge.svg?token=GGD39PPFM0)](https://codecov.io/gh/drish/resend-py)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/resend)](https://pypi.org/project/resend/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/resend)](https://pypi.org/project/resend)

---

## Installation

To install Resend Python SDK, simply execute the following command in a terminal:

```
pip install resend
```

## Setup

First, you need to get an API key, which is available in the [Resend Dashboard](https://resend.com).

```py
import resend
import os

resend.api_key = "re_yourkey"
```

## Example

You can get an overview about all parameters in the [Send Email](https://resend.com/docs/api-reference/emails/send-email) API reference.

```py
import os
import resend

resend.api_key = "re_yourkey"

params: resend.Emails.SendParams = {
    "from": "onboarding@resend.dev",
    "to": ["delivered@resend.dev"],
    "subject": "hi",
    "html": "<strong>hello, world!</strong>",
    "reply_to": "to@gmail.com",
    "bcc": "bcc@resend.dev",
    "cc": ["cc@resend.dev"],
    "tags": [
        {"name": "tag1", "value": "tagvalue1"},
        {"name": "tag2", "value": "tagvalue2"},
    ],
}

email: resend.Emails.SendResponse = resend.Emails.send(params)
print(email)
```
