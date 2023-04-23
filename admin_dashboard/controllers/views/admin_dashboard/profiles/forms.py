from django import forms
from django.forms import widgets
from profiles.models.profile_models import Profile
from bootstrap_datepicker_plus.widgets import DatePickerInput


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'contact_number',
            'gender',
            'date_of_birth',
            'civil_status',
            'address',
            'region',
            'province',
            'city',
            'monthly_salary',
            'spouse_first_name',
            'spouse_middle_name',
            'spouse_last_name',
        )
        widgets = {
            'date_of_birth': widgets.DateInput(attrs={'type': 'date'})
        }
