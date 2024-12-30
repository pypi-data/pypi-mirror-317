import os
import uuid
import pytest
from unittest.mock import patch, MagicMock
from momo_psb import MoMoPSBAPI

@pytest.fixture
def momo_psb_api():
    base_url = os.getenv("BASE_URL", "https://sandbox.momodeveloper.mtn.com")
    subscription_key = os.getenv("SUBSCRIPTION_KEY", "test_subscription_key")
    return MoMoPSBAPI(base_url, subscription_key)

@patch("requests.post")
def test_create_api_user(mock_post, momo_psb_api):
    reference_id = str(uuid.uuid4())
    provider_callback_host = "https://example.com/callback"

    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"message": "API user created successfully"}
    mock_post.return_value = mock_response

    response = momo_psb_api.create_api_user(reference_id, provider_callback_host)

    assert response.status_code == 201
    assert response.json() == {"message": "API user created successfully"}

@patch("requests.post")
def test_create_api_key(mock_post, momo_psb_api):
    api_user = str(uuid.uuid4())

    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"apiKey": "test_api_key"}
    mock_post.return_value = mock_response

    response = momo_psb_api.create_api_key(api_user)

    assert response.status_code == 201
    assert response.json() == {"apiKey": "test_api_key"}

@patch("requests.get")
def test_get_api_user_details(mock_get, momo_psb_api):
    api_user = str(uuid.uuid4())

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "active"}
    mock_get.return_value = mock_response

    response = momo_psb_api.get_api_user_details(api_user)

    assert response.status_code == 200
    assert response.json() == {"status": "active"}

@patch("requests.post")
def test_get_oauth_token(mock_post, momo_psb_api):
    api_user = str(uuid.uuid4())
    api_key = "test_api_key"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": "test_access_token"}
    mock_post.return_value = mock_response

    response = momo_psb_api.get_oauth_token(api_user, api_key)

    assert response.status_code == 200
    assert response.json()["access_token"] == "test_access_token"

@patch("requests.post")
def test_request_to_pay(mock_post, momo_psb_api):
    reference_id = str(uuid.uuid4())
    access_token = "test_access_token"
    amount = "100.00"
    currency = "EUR"
    external_id = "ext_id_123"
    payer = {
        "partyIdType": "MSISDN",
        "partyId": "256774000000"
    }
    payer_message = "Payment for services"
    payee_note = "Thank you for your payment"

    mock_response = MagicMock()
    mock_response.status_code = 202
    mock_response.json.return_value = {"status": "pending"}
    mock_post.return_value = mock_response

    response = momo_psb_api.request_to_pay(
        reference_id, access_token, amount, currency, external_id, payer, payer_message, payee_note
    )

    assert response.status_code == 202
    assert response.json()["status"] == "pending"
