from rest_framework import serializers

from payments.models.payment_request import PaymentRequest as Master


class PaymentRequestPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'id',
        )


class PaymentRequestPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'id',
            'created',
            'updated',
            'phone_number',
            'uuid',
            'payment_source',
            'amount',
            'currency',
            'attachment',
            'status',
            'is_active',
            'meta',
        )


class PaymentRequestPrivateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'id',
        )


class PaymentRequestPrivateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'id',
        )
