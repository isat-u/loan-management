from django import forms
from complaints.models.complaint.models import Complaint


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = (
            'response',
            'status',
        )
        widgets = {
            'response': forms.Textarea(attrs={'rows': 4, 'cols': 15})
        }
