from django import forms
from .models import Order


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices = PRODUCT_QUANTITY_CHOICES, coerce= int)
    override = forms.BooleanField(required=False, initial = False, widget = forms.HiddenInput)

# create OrderCreateForm with:
# model: Order
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "postal_code", "address", "city"]


# field: firstname, lastname, email, address, postal code, city