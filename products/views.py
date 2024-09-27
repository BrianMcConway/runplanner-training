from django.shortcuts import render
from .models import TrainingPlan
from .forms import TrainingPlanFilterForm

def training_plans(request):
    # Initialize the form with GET parameters if available, or None if not
    form = TrainingPlanFilterForm(request.GET or None)
    
    # Get all training plans from the database
    training_plans = TrainingPlan.objects.all()

    # Check if the form is valid (i.e., it passed all validation checks)
    if form.is_valid():
        # Retrieve the filtered values from the form's cleaned data
        distance = form.cleaned_data.get('distance')
        difficulty = form.cleaned_data.get('difficulty')
        terrain = form.cleaned_data.get('terrain')
        elevation = form.cleaned_data.get('elevation')

        # Apply filters based on the form's input
        if distance:
            training_plans = training_plans.filter(distance=distance)
        if difficulty:
            training_plans = training_plans.filter(difficulty=difficulty)
        if terrain:
            training_plans = training_plans.filter(terrain=terrain)
        if elevation:
            training_plans = training_plans.filter(elevation=elevation)

    # Render the template and pass the form and filtered training plans to the context
    return render(request, 'products/training_plans.html', {
        'form': form,                  # The form is sent back to the template to display the current state
        'training_plans': training_plans  # The filtered list of training plans to be displayed
    })
