import requests
from requests.auth import HTTPBasicAuth
import uuid

class MoMoPSBAPI:
    """
    A Python SDK for integrating with the MTN MoMo API (Payment Service Bank).
    """

    def __init__(self, base_url, subscription_key):
        """
        Initialize the MoMoPSBAPI.

        :param base_url: Base URL for the Wallet Platform API.
        :param subscription_key: Subscription key for the API Manager portal.
        """
        self.base_url = base_url.rstrip("/")
        self.subscription_key = subscription_key
        self.headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key
        }

    def create_api_user(self, reference_id, provider_callback_host):
        """
        Create a new API User.

        :param reference_id: UUID Reference ID to be used as the User ID.
        :param provider_callback_host: Callback host for the provider.
        :return: Response object.
        """
        url = f"{self.base_url}/v1_0/apiuser"
        self.headers["X-Reference-Id"] = reference_id
        payload = {"providerCallbackHost": provider_callback_host}
        response = requests.post(url, json=payload, headers=self.headers)
        return response

    def create_api_key(self, api_user):
        """
        Create a new API Key for an existing API User.

        :param api_user: The API User ID.
        :return: Response object containing the API Key.
        """
        url = f"{self.base_url}/v1_0/apiuser/{api_user}/apikey"
        response = requests.post(url, headers=self.headers)
        return response

    def get_api_user_details(self, api_user):
        """
        Retrieve details of an API User.

        :param api_user: The API User ID.
        :return: Response object containing API User details.
        """
        url = f"{self.base_url}/v1_0/apiuser/{api_user}"
        response = requests.get(url, headers=self.headers)
        return response

    def get_oauth_token(self, api_user, api_key):
        """
        Obtain an OAuth 2.0 access token.

        :param api_user: API User ID for basic authentication.
        :param api_key: API Key for basic authentication.
        :return: Response object containing the access token.
        """
        url = f"{self.base_url}/collection/token/"
        auth = HTTPBasicAuth(api_user, api_key)
        headers = {
            "X-Target-Environment": "sandbox",
            **self.headers  # Include other headers like 'Ocp-Apim-Subscription-Key'
        }
        payload = {"grant_type": "client_credentials"}
        
        # Use `auth` to handle the Authorization header
        response = requests.post(url, data=payload, headers=headers, auth=auth)
        
        # Debugging output to inspect the Authorization header
        prepared_request = response.request
        print(f"Request Headers: {prepared_request.headers}")
        
        return response


    def request_to_pay(self, reference_id, access_token, amount, currency, external_id, payer, payer_message, payee_note):
        """
        Request a payment from a consumer (Payer).

        :param reference_id: UUID Reference ID for the transaction.
        :param access_token: Bearer Authentication Token.
        :param amount: Amount to be debited from the payer account.
        :param currency: ISO4217 Currency code.
        :param external_id: External ID used as a reference to the transaction.
        :param payer: Dictionary with 'partyIdType' and 'partyId' keys identifying the payer.
        :param payer_message: Message written in the payer transaction history message field.
        :param payee_note: Message written in the payee transaction history note field.
        :return: Response object.
        """
        url = f"{self.base_url}/collection/v1_0/requesttopay"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Callback-Url": "https://clinic.com",  # Add your callback URL here if needed
            "X-Reference-Id": reference_id,
            "X-Target-Environment": "sandbox",
            **self.headers  # Include other headers like 'Ocp-Apim-Subscription-Key'
        }
        payload = {
            "amount": float(amount),
            "currency": currency,
            "externalId": external_id,
            "payer": payer,
            "payerMessage": payer_message,
            "payeeNote": payee_note
        }
        response = requests.post(url, json=payload, headers=headers)
        return response

    def validate_response(self, response):
        """
        Validate the API response.

        :param response: The response object.
        :return: Parsed JSON data if the response is successful; raises an error otherwise.
        """
        if response.status_code in (200, 201, 202):
            return response.json()
        else:
            response.raise_for_status()


