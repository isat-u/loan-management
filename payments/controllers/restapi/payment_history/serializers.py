from paypal.standard.ipn.models import PayPalIPN
from rest_framework import serializers
from payments.models.payment_history import PaymentHistory as Master


class PaymentHistoryPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'id',
        )


class PaymentHistoryPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'id',
        )


class PaymentHistoryPrivateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'id',
        )


class PaymentHistoryPrivateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'id',
        )


class PaypalIPNCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayPalIPN
        fields = '__all__'
