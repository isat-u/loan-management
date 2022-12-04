"""
Loan Management
Amortization 0.0.1
Amortization models
Amortization

Author: Maayon
"""

import uuid as uuid
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

from .managers import AmortizationManager as manager


class Amortization(models.Model):
    # === Basic ===
    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    # === Identifiers ===
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, null=True, editable=True)

    # === Properties ===
    month = models.PositiveSmallIntegerField(null=True, blank=True)
    ideal_principal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ideal_interest = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ideal_monthly_amortization = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ideal_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    actual_principal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    actual_interest = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    actual_monthly_amortization = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    actual_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # === State ===
    is_active = models.BooleanField(default=True)
    meta = models.JSONField(default=dict, blank=True, null=True)

    # === Relationship Fields ===
    loan = models.ForeignKey(
        'loans.Loan',
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        db_index=False,
        on_delete=models.SET_NULL,
        related_name='amortizations_created_by_user'
    )
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        db_index=False,
        on_delete=models.SET_NULL,
        related_name='amortizations_updated_by_user'
    )

    objects = manager()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Amortization'
        verbose_name_plural = 'Amortizations'
    
    ################################################################################
    # === Magic Methods ===
    ################################################################################
    def __str__(self):
        return f'{self.loan} - {self.uuid}'

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
@receiver(post_save, sender=Amortization)
def scaffold_post_save(sender, instance=None, created=False, **kwargs):
    pass


@receiver(pre_save, sender=Amortization)
def scaffold_pre_save(sender, instance=None, created=False, **kwargs):
    pass
