from django import forms
from loans.models.loan_type.models import LoanType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class LoanTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LoanTypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('attachment', css_class='form-control-file mt-2 mb-3'),
        )
    class Meta:
        model = LoanType
        fields = [
            'name',
            'attachment',
        ]
