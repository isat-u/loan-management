from django import forms
from loans.models.loan.models import Loan


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = [
            'type',
            'savings',
            'amount',
            'maturity',
            'due_date',
        ]
