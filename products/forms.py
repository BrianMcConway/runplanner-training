from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import TrainingPlan

class TrainingPlanFilterForm(forms.Form):
    distance = forms.ChoiceField(
        choices=[('', 'Select Distance')] + TrainingPlan.DISTANCE_CHOICES,
        required=True,
        label='Distance'
    )
    difficulty = forms.ChoiceField(
        choices=[('', 'Select Fitness Level')] + TrainingPlan.DIFFICULTY_CHOICES,
        required=True,
        label='Fitness Level'
    )
    terrain = forms.ChoiceField(
        choices=[('', 'Select Terrain')] + TrainingPlan.TERRAIN_CHOICES,
        required=True,
        label='Terrain'
    )
    elevation = forms.ChoiceField(
        choices=[('', 'Select Elevation')] + TrainingPlan.ELEVATION_CHOICES,
        required=True,
        label='Elevation'
    )
    event_date = forms.DateField(
        widget=forms.SelectDateWidget(),
        required=True,
        label='Event Date'
    )

    def __init__(self, *args, **kwargs):
        super(TrainingPlanFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.add_input(Submit('submit', 'Find Training Plans'))

    def clean(self):
        cleaned_data = super().clean()
        distance = cleaned_data.get("distance")
        difficulty = cleaned_data.get("difficulty")
        terrain = cleaned_data.get("terrain")
        elevation = cleaned_data.get("elevation")
        event_date = cleaned_data.get("event_date")

        # Check if all fields are filled
        if not distance or not difficulty or not terrain or not elevation or not event_date:
            raise ValidationError("Please make sure all fields are selected, including the event date.")

        # Check if event date is in the past
        if event_date and event_date < timezone.now().date():
            raise ValidationError("The event date cannot be in the past.")

        return cleaned_data
