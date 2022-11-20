from django import forms
from loans.models.loan_type.models import LoanType


class LoanTypeForm(forms.ModelForm):
    class Meta:
        model = LoanType
        fields = [
            'name',
        ]
