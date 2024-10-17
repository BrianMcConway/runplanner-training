from django import forms
from .models import Order
from django_countries.widgets import CountrySelectWidget  # For country dropdown

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone_number', 'country', 'street_address1',
                  'street_address2', 'town_or_city', 'county', 'postal_code']
        widgets = {
            'country': CountrySelectWidget(layout='{widget}'),  # Remove the flag
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add autocomplete attributes to form fields for better browser autofill support
        self.fields['full_name'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'name'  # Full name autofill
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'email'  # Email autofill
        })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'tel'  # Phone number autofill
        })
        self.fields['street_address1'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'address-line1'  # Address line 1 autofill
        })
        self.fields['street_address2'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'address-line2'  # Address line 2 autofill (optional)
        })
        self.fields['town_or_city'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'address-level2'  # City autofill
        })
        self.fields['county'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'address-level1'  # State or County autofill
        })
        self.fields['postal_code'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'postal-code'  # Postal code autofill
        })
        self.fields['country'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'country'  # Country autofill
        })
