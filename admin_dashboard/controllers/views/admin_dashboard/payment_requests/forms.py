from django import forms
from payments.models.payment_history.constants import CASH_ONLY
from payments.models.payment_request.models import PaymentRequest


class PaymentRequestForm(forms.ModelForm):
    class Meta:
        model = PaymentRequest
        fields = (
            'phone_number',
            'payment_source',
            'amount',
            'currency',
            'attachment',
            'status',
            'account',
            'loan',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_source'].choices = CASH_ONLY
