from django import forms
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
        required=False,
        label='Event Date'
    )

    def clean(self):
        cleaned_data = super().clean()
        distance = cleaned_data.get("distance")
        difficulty = cleaned_data.get("difficulty")
        terrain = cleaned_data.get("terrain")
        elevation = cleaned_data.get("elevation")

        # Ensure that all required fields are selected
        if not distance or not difficulty or not terrain or not elevation:
            raise ValidationError("Please make sure all fields are selected.")

        return cleaned_data

    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        if event_date and event_date < timezone.now().date():
            raise ValidationError("The event date cannot be in the past.")
        return event_date
