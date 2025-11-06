from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from .models import PaymentEvent
from .utils import verify_webhook_signature, extract_payload_data

@method_decorator(csrf_exempt, name='dispatch')
class WebhookListenerView(APIView):
    """
    Webhook endpoint to receive payment status updates.
    1. Verifies the HMAC signature (Security).
    2. Saves the event payload to the database (Logging/Processing).
    """

    def post(self, request, *args, **kwargs):
        try:
            raw_body = request.body

            received_signature = request.META.get('HTTP_X_PAYMENT_SIGNATURE')

            if not received_signature:
                return Response({'detail': 'Missing X-Payment-Signature header'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response({'error': 'Invalid request format or missing data'}, status=status.HTTP_400_BAD_REQUEST)

        if not verify_webhook_signature(raw_body, received_signature):
            print("SECURITY ALERT: Webhook signature verification failed.")
            return Response({'detail': 'Signature verification failed'}, status=status.HTTP_401_UNAUTHORIZED)

        extracted_data = extract_payload_data(raw_body.decode('utf-8'))

        if not extracted_data:
             return Response({'error': 'Invalid JSON payload'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            PaymentEvent.objects.create(
                event_id=extracted_data['id'],
                status=extracted_data['type'],
                payload=extracted_data['payload']
            )

            return Response({'message': f"Event {extracted_data['id']} successfully processed"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"INTERNAL PROCESSING ERROR: {e}")
            return Response({'error': 'Internal processing error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)