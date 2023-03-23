from rest_framework import serializers

from loans.controllers.restapi.loan_type.serializers import LoanTypePrivateSerializer
from loans.models.loan import Loan as Master
from payments.controllers.restapi.payment_request.serializers import PaymentRequestPrivateSerializer


class LoanPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'id',
        )


class LoanPrivateSerializer(serializers.ModelSerializer):
    payment_requests_loan = PaymentRequestPrivateSerializer(many=True, read_only=True)
    type = LoanTypePrivateSerializer(many=False, read_only=True)

    class Meta:
        model = Master
        fields = (
            'id',
            'amount',
            'savings',
            'uuid',
            'maturity',
            'due_date',
            'years',
            'monthly_amortization',
            'monthly_interest',
            'yearly_interest',
            'is_active',
            'type',
            'payment_requests_loan',
        )


class LoanPrivateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'id',
        )


class LoanPrivateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'id',
        )
