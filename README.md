# Resend Python SDK

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Build](https://github.com/drish/resend-py/actions/workflows/test.yaml/badge.svg)
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
from resend import Resend

client = Resend(api_key="kl_123")
```

## Example

```py
import os
from resend import Resend

client = Resend(api_key=os.environ["RESEND_API_KEY"])

client.send_email(
    to="to@email.com",
    sender="from@email.com",
    subject="hi",
    html="<strong>hello, world!</strong>"
)
```

## Example sending email using React

Coming soon.