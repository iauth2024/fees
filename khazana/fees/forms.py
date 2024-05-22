# forms.py

from django import forms
from .models import Payment

class PaymentForm(forms.Form):
    admission_number = forms.CharField(label="Admission Number")
    amount_paid = forms.DecimalField(label="Amount Paid")
    receipt_number = forms.CharField(label="Receipt Number")

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file')
class PaymentUploadForm(forms.Form):
    excel_file = forms.FileField()