# Klotty Python SDK

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Build](https://github.com/drish/klotty-py/actions/workflows/test.yaml/badge.svg)
![](https://img.shields.io/badge/license-MIT-blue.svg)
[![codecov](https://codecov.io/gh/drish/klotty-py/branch/main/graph/badge.svg?token=GGD39PPFM0)](https://codecov.io/gh/drish/klotty-py)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
---

## Installation

To install Klotty Python SDK, simply execute the following command in a terminal:

```
pip install klotty
```

## Example

```py
from klotty import Klotty

client = Klotty(api_key=os.environ["KLOTTY_API_KEY"])

client.send_email(
    to="to@email.com",
    sender="from@email.com",
    subject="hi",
    html="<strong>hello, world!</strong>"
)
```