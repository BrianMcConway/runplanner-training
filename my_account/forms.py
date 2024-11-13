from django import forms
from django.contrib.auth.models import User

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, label='First Name')
    last_name = forms.CharField(required=False, label='Last Name')
    email = forms.EmailField(required=True, label='Email Address')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']