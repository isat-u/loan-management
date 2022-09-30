from django import forms
from accounts.models.account.models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
