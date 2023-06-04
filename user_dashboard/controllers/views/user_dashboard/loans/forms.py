from datetime import date
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ModelForm, widgets, FloatField
from loans.models.loan.models import Loan


class LoanForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(LoanForm, self).__init__(*args, **kwargs)
        self.fields['due_date'].initial = date.today()

    
    class Meta:
        model = Loan
        fields = (
            'type',
            'months',
            'amount',
            'due_date',
        )

        widgets = {
            'due_date': widgets.DateInput(attrs={'type': 'date'})
        }
    
    amount = forms.IntegerField(validators=[MinValueValidator(1)])
    months = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(36)])
