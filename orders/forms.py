from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['f_name', 'l_name', 'email', 'tel', 'address', 'country', 'state', 'city', 'zipcode', 'order_note']