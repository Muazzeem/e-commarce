from django import forms


class CheckoutForm(forms.Form):
    address = forms.CharField(required=True)
    phone = forms.CharField(required=True)
