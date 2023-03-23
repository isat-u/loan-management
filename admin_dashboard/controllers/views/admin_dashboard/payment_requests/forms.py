from django import forms
from payments.models.payment_request.models import PaymentRequest


class PaymentRequestForm(forms.ModelForm):
    class Meta:
        model = PaymentRequest
        fields = '__all__'
