"""
Loan Management
Loan 0.0.1
Loan models
Loan

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

from .managers import LoanManager as manager


class Loan(models.Model):
    # === Basic ===
    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    # === Identifiers ===
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    savings = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, null=True, editable=True)

    # === Properties ===
    maturity = models.CharField(max_length=64, null=True, blank=True)
    due_date = models.DateField(null=False)
    years = models.PositiveSmallIntegerField(null=True, blank=True)
    monthly_amortization = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    yearly_interest = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    monthly_interest = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)

    # === State ===
    is_active = models.BooleanField(default=True)
    meta = models.JSONField(default=dict, blank=True, null=True)

    # === Relationship Fields ===
    type = models.ForeignKey(
        'loans.LoanType',
        on_delete=models.CASCADE
    )
    account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        db_index=False,
        on_delete=models.SET_NULL,
        related_name='loans_created_by_user'
    )
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        db_index=False,
        on_delete=models.SET_NULL,
        related_name='loans_updated_by_user'
    )

    objects = manager()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'
    
    ################################################################################
    # === Magic Methods ===
    ################################################################################
    def __str__(self):
        return f'{self.type} - {self.amount}'

    def monthly_percentage(self):
        return f'{round(self.monthly_interest * 100, 2)}%'

    def yearly_percentage(self):
        return f'{round(self.yearly_interest * 100, 2)}%'

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
@receiver(post_save, sender=Loan)
def scaffold_post_save(sender, instance=None, created=False, **kwargs):
    pass


@receiver(pre_save, sender=Loan)
def scaffold_pre_save(sender, instance=None, created=False, **kwargs):
    pass
