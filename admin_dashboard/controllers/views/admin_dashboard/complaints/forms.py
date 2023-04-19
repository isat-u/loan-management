from django import forms
from complaints.models.complaint.models import Complaint


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = '__all__'
