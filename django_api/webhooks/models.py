from django.db import models

class PaymentEvent(models.Model):
    """
    Stores details for incoming payment webhook events.
    """
    event_id = models.CharField(max_length=100, unique=True, help_text="ID of the event from the external service.")
    status = models.CharField(max_length=150, help_text="Type/status of the event.")
    payload = models.JSONField(help_text="Full raw JSON payload received.")
    received_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"[{self.received_at.strftime('%Y-%m-%d %H:%M')}] {self.status} for ID: {self.event_id}"
