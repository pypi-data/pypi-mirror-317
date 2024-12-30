# MoMoPSBAPI Python SDK Documentation

Welcome to the **MoMoPSBAPI Python SDK**! This SDK enables developers to integrate with the MTN MoMo API for managing API users, API keys, OAuth 2.0 tokens, and payment processing in a seamless manner. Below, you'll find a comprehensive guide on installation, usage, and functionality.

---

## Features
- **Create and manage API Users**
- **Generate API Keys for secure communication**
- **Obtain OAuth 2.0 tokens for authentication**
- **Initiate and manage payment requests**
- **Validate API responses**

---

## Requirements
### Sandbox/Testing Users:
1. MTN MoMo Developer Account: [Sign Up Here](https://momodeveloper.mtn.com/signin?ReturnUrl=%2F)
2. Collection and Disbursement subscription keys

### Production Users:
1. Collection and Disbursement subscription keys
2. API User ID and API Key

---

## Installation
Install the required dependencies:
```bash
pip install requests
```

---

## Quickstart Guide

### Initialize the SDK
```python
from momo_psb import MoMoPSBAPI

# Replace with your details
BASE_URL = "https://sandbox.momodeveloper.mtn.com"
SUBSCRIPTION_KEY = "your_subscription_key"

# Initialize the API client
api = MoMoPSBAPI(base_url=BASE_URL, subscription_key=SUBSCRIPTION_KEY)
```

---

### Key API Operations

#### 1. Create API User
Generate a unique API User.
```python
import uuid

reference_id = str(uuid.uuid4())  # Generate a unique reference ID
callback_host = "https://your-callback-host.com"

response = api.create_api_user(reference_id, callback_host)
print("Status Code:", response.status_code)
print("Response:", response.json())
```

#### 2. Generate API Key
Create an API Key for the generated API User.
```python
api_user = "your_api_user_id"
response = api.create_api_key(api_user)
print("Status Code:", response.status_code)
print("API Key:", response.json().get("apiKey"))
```

#### 3. Retrieve API User Details
Fetch details of an API User.
```python
response = api.get_api_user_details(api_user)
print("Status Code:", response.status_code)
print("User Details:", response.json())
```

#### 4. Obtain OAuth 2.0 Token
Generate an access token for authorization.
```python
api_key = "your_api_key"
response = api.get_oauth_token(api_user, api_key)
print("Status Code:", response.status_code)
token_data = response.json()
access_token = token_data.get("access_token")
print("Access Token:", access_token)
```

#### 5. Request to Pay
Initiate a payment request from a consumer.
```python
payer_info = {
    "partyIdType": "MSISDN",
    "partyId": "+2348056042384"
}
reference_id = str(uuid.uuid4())

response = api.request_to_pay(
    reference_id=reference_id,
    access_token=access_token,
    amount="100.00",
    currency="EUR",
    external_id=str(uuid.uuid4()),
    payer=payer_info,
    payer_message="Payment for services",
    payee_note="Thank you for your payment"
)

print("Status Code:", response.status_code)
print("Response:", response.json())
```

---

## Error Handling
Use the `validate_response` method to handle errors gracefully.
```python
try:
    data = api.validate_response(response)
    print("Success:", data)
except Exception as e:
    print("Error:", e)
```

---

## Notes
1. **Environment Setup**:
   - Default environment is `sandbox`. Update the base URL for production use.
2. **Status Codes**:
   - `200`, `201`, `202`: Successful operations.
   - Other codes indicate errors and should be handled appropriately.
3. **Unique Identifiers**:
   - Use `uuid.uuid4()` to generate reference IDs for requests.

---

## Additional Resources
- [MTN MoMo API Documentation](https://momodeveloper.mtn.com/)
- [Python Requests Documentation](https://docs.python-requests.org/en/latest/)

---