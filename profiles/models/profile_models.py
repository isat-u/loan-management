from django.contrib.postgres.forms import JSONField
from django.db import models, IntegrityError
from django_extensions.db import fields as extension_fields
from profiles.models.constants import CIVIL_STATUS_CHOICES, SINGLE
from profiles.models.managers import ProfileManager, GenderManager


class Gender(models.Model):
    name = models.CharField(max_length=32, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)

    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    objects = GenderManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Profile(models.Model):
    # Fields
    first_name = models.CharField(max_length=32, blank=True, null=True, default='')
    middle_name = models.CharField(max_length=32, blank=True, null=True, default='')
    last_name = models.CharField(max_length=32, blank=True, null=True, default='')
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    civil_status = models.CharField(choices=CIVIL_STATUS_CHOICES, default=SINGLE, max_length=24)
    contact_number = models.CharField(max_length=13, blank=True, null=True)
    address = models.CharField(max_length=254, blank=True, null=True)
    monthly_salary = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, blank=True, null=True)
    spouse_last_name = models.CharField(max_length=32, blank=True, null=True, default='')
    spouse_middle_name = models.CharField(max_length=32, blank=True, null=True, default='')
    spouse_first_name = models.CharField(max_length=32, blank=True, null=True, default='')
    barangay = models.CharField(max_length=254, blank=True, null=True, default='')
    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    # Relationship Fields
    gender = models.ForeignKey(Gender, related_name='gender_profiles', on_delete=models.SET_NULL, null=True, blank=True)
    account = models.OneToOneField(
        'accounts.Account',
        on_delete=models.CASCADE,
    )

    meta = JSONField()

    objects = ProfileManager()

    class Meta:
        ordering = ('account', '-created')

    def __str__(self):
        return self.get_full_name()

    def as_html(self):
        html = f"<p class='kv-pair kv-pair-center'><span class='kv-key'>Full Name</span><span class='kv-value'>{self.get_full_name()}</p>" \
               f"<p class='kv-pair kv-pair-center'><span class='kv-key'>Sex</span><span class='kv-value'>{self.gender}</p>" \
               f"<p class='kv-pair kv-pair-center'><span class='kv-key'>Date of Birth</span><span class='kv-value'>{self.date_of_birth}</p>"
        return html

    def get_casual_name(self):
        if self.first_name != '':
            return self.first_name
        return 'Unnamed'

    def get_name(self):
        if self.first_name != '' and self.last_name != '':
            return '{} {}'.format(
                self.first_name, self.last_name
            )
        else:
            if self.account.username is not None:
                return self.account.username
            return self.account.email

    def get_full_name(self):
        if self.first_name != '' and self.last_name != '':
            return '{}, {}'.format(
                self.last_name, self.first_name
            )
        else:
            try:
                if self.account.username is not None:
                    return self.account.username
            except AttributeError:
                return 'Unnamed'
            return 'Unnamed'

    def get_spouse_full_name(self):
        if self.spouse_first_name is not None and self.spouse_last_name is not None:
            print(self.spouse_first_name)
            return '{}, {}'.format(
                self.spouse_last_name, self.spouse_first_name
            )
        else:
            try:
                if self.account.username is not None:
                    return self.account.username
            except AttributeError:
                return 'Unnamed'
            return 'Unnamed'
