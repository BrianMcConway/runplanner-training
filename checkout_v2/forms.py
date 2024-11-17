from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number', 
            'street_address1', 'street_address2', 
            'town_or_city', 'country', 'county',
            'postcode',  # Include postcode for complete address form
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Define placeholders and autocomplete attributes
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
            'postcode': 'Postcode',  # Placeholder for postcode
        }
        
        autocomplete_attributes = {
            'full_name': 'name',
            'email': 'email',
            'phone_number': 'tel',
            'town_or_city': 'address-level2',
            'street_address1': 'address-line1',
            'street_address2': 'address-line2',
            'county': 'address-level1',
            'postcode': 'postal-code',
            'country': 'country-name',
        }

        # Autofocus the first field and set attributes for all fields
        self.fields['full_name'].widget.attrs.update({'autofocus': True})
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'placeholder': placeholders.get(field, ''),
                'id': field,
                'name': field,
                'autocomplete': autocomplete_attributes.get(field, 'on'),
            })
            # Add a consistent CSS class for styling
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # Remove field labels
            self.fields[field].label = False
