from django import forms
from .models import Order

# create OrderCreateForm with:
# model: Order
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "postal_code", "address", "city"]


# field: firstname, lastname, email, address, postal code, city