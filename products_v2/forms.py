from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Product

class TrainingPlanFilterForm(forms.Form):
    distance = forms.ChoiceField(
        choices=[('', 'Select Distance')] + Product.DISTANCE_CHOICES,
        required=True,
        label='Distance'
    )
    difficulty = forms.ChoiceField(
        choices=[('', 'Select Fitness Level')] + Product.DIFFICULTY_CHOICES,
        required=True,
        label='Fitness Level'
    )
    terrain = forms.ChoiceField(
        choices=[('', 'Select Terrain')] + Product.TERRAIN_CHOICES,
        required=True,
        label='Terrain'
    )
    elevation = forms.ChoiceField(
        choices=[('', 'Select Elevation')] + Product.ELEVATION_CHOICES,
        required=True,
        label='Elevation'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.add_input(Submit('submit', 'Find Training Plan'))