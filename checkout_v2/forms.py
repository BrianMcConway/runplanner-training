from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number', 
            'street_address1', 'street_address2', 
            'town_or_city', 'country', 'county',
        )  # Removed 'postcode' from fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }  # Removed 'postcode' from placeholders

        self.fields['full_name'].widget.attrs.update({'autofocus': True})
        for field in self.fields:
            if field != 'country':
                self.fields[field].widget.attrs.update({
                    'placeholder': placeholders.get(field, ''),
                    'id': field,
                    'name': field
                })
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
