from django import forms
from payments.models import PaymentRequest


class PaymentRequestForm(forms.ModelForm):
    class Meta:
        model = PaymentRequest
        fields = [
            'payment_source',
            'phone_number',
            'amount',
            'account',
            'loan',
        ]
