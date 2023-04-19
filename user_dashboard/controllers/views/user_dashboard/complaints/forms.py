from django import forms
from complaints.models.complaint.models import Complaint


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = (
            'title',
            'type',
            'content',
        )
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 15})
        }
