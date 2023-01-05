"""
Loan Management
Payment 0.0.1
Payment History models
Payment History

Author: Maayon
"""

import uuid as uuid
from decimal import Decimal

from django.conf import settings
from django.db import models as models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from utils.payment import random_string_digits
from .constants import PAYMENT_SOURCES, CURRENCY_CHOICES, PAYMENT_STATUS_CHOICES, INVOICE_PAD
from .managers import PaymentHistoryManager as manager


def increment_invoice_number():
    last_invoice = PaymentHistory.objects.all().order_by('id').last()
    if not last_invoice:
        return 'MAA0000000001'
    invoice_no = last_invoice.invoice_number
    invoice_int = int(invoice_no.split('MAA')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_no = INVOICE_PAD[:-len(str(new_invoice_int))] + str(new_invoice_int)
    new_invoice_no = 'MAA' + str(new_invoice_no)
    return new_invoice_no


def generate_invoice_key():
    invoice = random_string_digits(string_length=64)
    while PaymentHistory.objects.filter(key=invoice).count() > 0:
        invoice = random_string_digits(string_length=64)
    return invoice


def get_default_data():
    return {'business': [], 'custom': []}


class PaymentHistory(models.Model):
    """
        provider_data
      - paypal
        - business
        - custom (user email)
        - receiver_email (email for paypal)
        - receiver_id
        - residence_country
        - txn_id
        - txn_type
        - address_country
        - address_city
        - address_country_code
        - address_country_name
        - address_country_state
        - address_country_status
        - address_country_street
        - address_country_zip
        - contact_phone
        - first_name
        - last_name
        - payer_business_name
        - payer_email
        - payer_id
        - exchange_rate
        - invoice
        - item_name
        - item_number
        - mc_currency
        - mc_fee
        - mc_gross
        - mc_handling
        - mc_shipping
        - memo
        - num_cart_items
        - option_name1
        - option_name2
        - option_selection1
        - option_selection2
        - payer_status
        - payment_date
        - payment_status
        - payment_type
        - pending_reason
        - protection_eligibility
        - quantity
        - reason_code
        - remaining_settle
        - settle_amount
        - settle_currency
        - shipping
        - shipping_method
        - tax
    """
    # === Basic ===
    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    # === Identifiers ===
    invoice_number = models.CharField(blank=True, max_length=20, unique=True, default=increment_invoice_number)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, null=True, editable=True)
    key = models.CharField(max_length=64, blank=True, default=generate_invoice_key)

    # === Properties ===
    payment_date = models.DateTimeField(default=timezone.now)
    payment_source = models.CharField(max_length=64, choices=PAYMENT_SOURCES, default='paypal')
    amount = models.DecimalField(max_digits=19, decimal_places=4, default=Decimal(0.0))
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='PHP')

    # === State ===
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=17, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    provider_data = models.JSONField(default=get_default_data, blank=True, null=True)

    # === Relationship Fields ===
    account = models.ForeignKey(
        'accounts.Account',
        related_name='payment_histories_account',
        on_delete=models.SET_NULL,
        null=True
    )
    loan = models.ForeignKey(
        'loans.Loan',
        related_name='payment_histories_loan',
        on_delete=models.SET_NULL,
        null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        db_index=False,
        on_delete=models.SET_NULL,
        related_name='payment_histories_created_by_user'
    )
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        db_index=False,
        on_delete=models.SET_NULL,
        related_name='payment_histories_updated_by_user'
    )

    objects = manager()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Payment History'
        verbose_name_plural = 'Payment Histories'

    ################################################################################
    # === Magic Methods ===
    ################################################################################
    def __str__(self):
        return f'{self.currency} {self.amount:.2f} via {self.payment_source}'

        ################################################################################

    # === Model overrides ===
    ################################################################################
    def clean(self, *args, **kwargs):
        # add custom validation here
        super().clean()

    def save(self, *args, **kwargs):
        # self.full_clean()
        super().save(*args, **kwargs)

    ################################################################################
    # === Model-specific methods ===
    ################################################################################


class PaymentHistoryError(models.Model):
    created = models.DateTimeField(null=False, auto_now_add=True)
    last_updated = models.DateTimeField(null=False, auto_now=True)

    payment_source = models.CharField(max_length=64, choices=PAYMENT_SOURCES, default='paypal')
    reason = models.CharField(max_length=1024)

    provider_data = models.JSONField(null=True, blank=True, default=dict)

    invoice_number = models.CharField(max_length=16)

    class Meta:
        ordering = ('-created', '-invoice_number')

    def __str__(self):
        return f'{self.invoice_number}: {self.reason} ({self.payment_source})'


################################################################################
# === Signals ===
################################################################################
@receiver(post_save, sender=PaymentHistory)
def scaffold_post_save(sender, instance=None, created=False, **kwargs):
    pass


@receiver(pre_save, sender=PaymentHistory)
def scaffold_pre_save(sender, instance=None, created=False, **kwargs):
    pass


