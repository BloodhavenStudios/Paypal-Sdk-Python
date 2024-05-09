## PayPal REST SDK V2
The sdk provides Python APIs to create, process and manage payment. The [PayPal REST APIs](https://developer.paypal.com/api/rest/) are fully supported by the sdk.

> This is just a ALPHA branch and getting a semi version I like working

## What's New
Please see the [CHANGELOG.md](./CHANGELOG.md) for the latest changes.

## System Requirements
PayPal SDK depends on the following system libraries:
* requests
* base64
* time

## Installation
Install using `pip` and `git`:
```sh
pip install git+https://github.com/BloodhavenStudios/Paypal-Sdk-Python/tree/alpha
```

### Creating a Payment, Confirming, Authorizing, and Capturing a order. 
```python
# This could be subject to change.
import os
from paypal.client import PaypalSandbox
from paypal.templates import CreateOrderTemplate

# Create client using client_id and client_secret provided by https://developer.paypal.com
client = PaypalSandbox(
  client_id="id",
  client_secret="secret"
)

# Create the order template
create_order_template = CreateOrderTemplate(
  reference_id="reference id",
  purchase_units={
    "currency_code": "USD",
    "amount": "100.00",
  }
  shipping_address = {
    "address_line_1": "Company Address",
    "admin_area_2": "City",
    "admin_area_1": "State abbreviation: CA, MO, CO etc",
    "postal_code": "Costal Code",
    "country_code": "country code: US etc"
  },
  payment_source={
    "brand_name": "brand name",
    "locale": "locale: ex. en-US",
    "landing_page": "landing page",
    "return_url": "return url",
    "cancel_url": "cancel url"
  }
)

order_id = client.create_order(body=create_order_template)
client.confirm_order(order_id)
client.authorize_order(order_id)
order = client.capture_order(order_id)
```

*NOTE*: This API is still in alpha, is subject to change, and should not be used in production.
