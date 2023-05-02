from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ModelForm, widgets, FloatField
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
    
    years = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])
