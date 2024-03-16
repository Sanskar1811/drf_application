from django import forms
from .models import InvoiceDetail

class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the widget for the invoice field
        self.fields['invoice'].widget.attrs.update({'class': 'form-control'}) 