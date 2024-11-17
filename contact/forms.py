from django import forms
from .models import ContactMessage
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'name', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'autocomplete': 'email', 'placeholder': 'Enter your email'}),
            'subject': forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'Enter the subject'}),
            'message': forms.Textarea(attrs={'autocomplete': 'off', 'placeholder': 'Enter your message'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send Message', css_class='btn-primary'))
