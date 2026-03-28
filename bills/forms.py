from django import forms
from .models import Bill

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['product_name', 'purchase_date', 'expiry_date', 'bill_image']