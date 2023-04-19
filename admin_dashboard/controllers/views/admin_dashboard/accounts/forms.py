from django import forms

from accounts.models.account.constants import MEMBER_CHOICES, YES_NO
from accounts.models.account.models import Account


class AccountForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=50)
    email = forms.EmailField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    is_member = forms.ChoiceField(choices=MEMBER_CHOICES)
    is_active = forms.ChoiceField(choices=YES_NO)

    class Meta:
        model = Account
        fields = ('user_type',)
