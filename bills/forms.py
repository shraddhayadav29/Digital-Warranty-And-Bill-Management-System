from django import forms
from .models import Bill
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['product_name', 'purchase_date', 'expiry_date', 'bill_image']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }




class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']