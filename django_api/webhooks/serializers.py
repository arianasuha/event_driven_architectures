from rest_framework import serializers
from .models import PaymentEvent

class PaymentEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentEvent
        fields = '__all__'
        read_only_fields = ['id', 'received_at']