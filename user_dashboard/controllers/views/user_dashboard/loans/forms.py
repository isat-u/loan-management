from django.forms import ModelForm, DateField, widgets
from loans.models.loan.models import Loan


class LoanForm(ModelForm):
    class Meta:
        model = Loan
        fields = (
            'amount',
            'savings',
            'maturity',
            'due_date',
            'years',
            'monthly_amortization',
            'yearly_interest',
            'monthly_interest',
            'type',
        )

        widgets = {
            'due_date': widgets.DateInput(attrs={'type': 'date'})
        }
