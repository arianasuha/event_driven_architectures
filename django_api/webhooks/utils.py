import hashlib
import hmac
import os
import json
# Removed: from django.conf import settings (since settings.py is unavailable)

# This secret key is critical for HMAC verification.
# It is loaded from the environment variable WEBHOOK_SECRET or defaults to a hardcoded string
# if the environment variable is not set.
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET', 'my-super-secure-dev-secret-key-123')

def verify_webhook_signature(request_body, received_signature, secret=WEBHOOK_SECRET):
    """
    Verifies the HMAC signature of the request body against a received signature.

    :param request_body: The raw byte string of the HTTP request body.
    :param received_signature: The signature extracted from the custom HTTP header.
    :param secret: The shared secret key used for hashing.
    :return: True if signatures match, False otherwise.
    """

    # Ensure the secret is encoded to bytes
    secret_bytes = secret.encode('utf-8')

    # Compute the expected hash using the secret key and SHA256
    expected_signature = hmac.new(
        key=secret_bytes,
        msg=request_body, # We use the raw bytes directly
        digestmod=hashlib.sha256
    ).hexdigest()

    # Use hmac.compare_digest for secure, constant-time comparison (prevents timing attacks)
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