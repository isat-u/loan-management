from django.forms import ModelForm, widgets
from loans.models.loan.models import Loan


class LoanForm(ModelForm):
    class Meta:
        model = Loan
        fields = (
            'amount',
            'savings',
            'due_date',
            'years',
            'type',
        )

        widgets = {
            'due_date': widgets.DateInput(attrs={'type': 'date'})
        }
