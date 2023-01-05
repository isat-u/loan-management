"""
Loan Management
Payment 0.0.1
Payment Request models
Payment Request

Author: Maayon
"""

import uuid as uuid
from decimal import Decimal

from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.db.models import CharField
from django.db.models import DateTimeField
from django_extensions.db.fields import AutoSlugField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models
from django_extensions.db import fields as extension_fields
from django.apps import apps
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .managers import PaymentRequestManager as manager
from ..payment_history.constants import CURRENCY_CHOICES, PAYMENT_SOURCES, PAYMENT_REQUEST_STATUS_CHOICES


def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'uploads/payment/attachment/{filename}'


class PaymentRequest(models.Model):
    # === Basic ===
    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    # === Identifiers ===
    phone_number = models.CharField(max_length=20)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, null=True, editable=True)

    # === Properties ===
    payment_source = models.CharField(max_length=32, default='paypal', choices=PAYMENT_SOURCES)
    amount = models.DecimalField(max_digits=19, decimal_places=4, default=Decimal(0.0))
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='PHP')
    attachment = models.FileField(upload_to=upload_path, blank=True, null=True)

    # === State ===
    status = models.CharField(max_length=20, default='pending', choices=PAYMENT_REQUEST_STATUS_CHOICES)
    is_active = models.BooleanField(default=True)
    meta = models.JSONField(default=dict, blank=True, null=True)

    # === Relationship Fields ===
    account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.CASCADE,
        related_name='payment_requests_account'
    )
    loan = models.ForeignKey(
        'loans.Loan',
        on_delete=models.CASCADE,
        related_name='payment_requests_loan'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        db_index=False,
        on_delete=models.SET_NULL,
        related_name='payment_requests_created_by_user'
    )
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        db_index=False,
        on_delete=models.SET_NULL,
        related_name='payment_requests_updated_by_user'
    )

    objects = manager()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Payment Request'
        verbose_name_plural = 'Payment Requests'
    
    ################################################################################
    # === Magic Methods ===
    ################################################################################
    def __str__(self):
        return f'{self.account} via {self.payment_source}'

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


################################################################################
# === Signals ===
################################################################################
@receiver(post_save, sender=PaymentRequest)
def scaffold_post_save(sender, instance=None, created=False, **kwargs):
    pass


@receiver(pre_save, sender=PaymentRequest)
def scaffold_pre_save(sender, instance=None, created=False, **kwargs):
    pass
