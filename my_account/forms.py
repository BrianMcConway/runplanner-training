from django import forms
from django.contrib.auth.models import User


class EditProfileForm(forms.ModelForm):
    """
    A form for editing the user's profile information.
    """

    # Optional field for the user's first name
    first_name = forms.CharField(
        required=False,
        label='First Name'
    )

    # Optional field for the user's last name
    last_name = forms.CharField(
        required=False,
        label='Last Name'
    )

    # Required field for the user's email address
    email = forms.EmailField(
        required=True,
        label='Email Address'
    )

    class Meta:
        """
        Meta class to specify the model and fields for the form.
        """
        model = User
        fields = ['first_name', 'last_name', 'email']
