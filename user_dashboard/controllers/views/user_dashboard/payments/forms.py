from django import forms
from payments.models import PaymentRequest
from django.conf import settings
from django.utils.html import format_html
from paypal.standard.forms import PayPalStandardBaseForm
from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.widgets import ValueHiddenInput
from paypal.utils import warn_untested
from warnings import warn

from paypal.standard.conf import (
    BUY_BUTTON_IMAGE, DONATION_BUTTON_IMAGE, PAYPAL_CERT, PAYPAL_CERT_ID, PAYPAL_PRIVATE_CERT, PAYPAL_PUBLIC_CERT, POSTBACK_ENDPOINT, SANDBOX_POSTBACK_ENDPOINT, SUBSCRIPTION_BUTTON_IMAGE
)


class PaymentRequestForm(forms.ModelForm):
    class Meta:
        model = PaymentRequest
        fields = [
            'payment_source',
            'phone_number',
            'attachment',
            'amount',
            'account',
            'loan',
        ]


class PayPalIPNForm(PayPalStandardBaseForm):
  """
  Form used to receive and record PayPal IPN notifications.
  PayPal IPN test tool:
  https://developer.paypal.com/us/cgi-bin/devscr?cmd=_tools-session
  """

  class Meta:
    model = PayPalIPN
    exclude = []
