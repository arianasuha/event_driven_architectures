from django.db import models

class PaymentEvent(models.Model):
    """
    Stores details for incoming payment webhook events.
    """
    # Unique ID provided by the external service for the event itself
    event_id = models.CharField(max_length=100, unique=True, help_text="ID of the event from the external service.")

    # Status extracted from the payload (e.g., 'payment_intent.succeeded')
    status = models.CharField(max_length=150, help_text="Type/status of the event.")

    # The full, raw data sent by the webhook
    payload = models.JSONField(help_text="Full raw JSON payload received.")

    # Timestamp for when your server received it
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-received_at']

    def __str__(self):
        return f"[{self.received_at.strftime('%Y-%m-%d %H:%M')}] {self.status} for ID: {self.event_id}"
