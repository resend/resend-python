# Klotty Python SDK

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