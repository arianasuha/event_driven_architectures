import hashlib
import hmac
import json
from django.conf import settings

WEBHOOK_SECRET = settings.WEBHOOK_SECRET

def verify_webhook_signature(request_body, received_signature, secret=WEBHOOK_SECRET):
    """
    Verifies the HMAC signature of the request body against a received signature.

    :param request_body: The raw byte string of the HTTP request body.
    :param received_signature: The signature extracted from the custom HTTP header.
    :param secret: The shared secret key used for hashing.
    """

    secret_bytes = secret.encode('utf-8')

    # Computing the expected hash using the secret key and SHA256
    expected_signature = hmac.new(
        key=secret_bytes,
        msg=request_body, # using the raw bytes directly
        digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_signature, received_signature)

def extract_payload_data(raw_body):
    """
    Safely loads and extracts required data points from the raw JSON body.
    """
    try:
        payload = json.loads(raw_body)
        return {
            'id': payload.get('id', 'N/A'),
            'type': payload.get('type', 'event.unknown'),
            'payload': payload,
        }
    except json.JSONDecodeError:
        return None