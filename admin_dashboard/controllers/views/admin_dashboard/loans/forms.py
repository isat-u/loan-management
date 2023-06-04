from django import forms
from loans.models.loan.models import Loan


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = [
            'type',
            'months',
            'savings',
            'amount',
            'maturity',
            'monthly_amortization',
            'account',
        ]
