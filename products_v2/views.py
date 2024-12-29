from django.shortcuts import render, redirect
from .forms import TrainingPlanFilterForm
from .models import Product


def training_plans(request):
    form = TrainingPlanFilterForm(request.GET or None)
    preview_plan = None

    if form.is_valid():
        distance = form.cleaned_data.get('distance')
        difficulty = form.cleaned_data.get('difficulty')
        terrain = form.cleaned_data.get('terrain')
        elevation = form.cleaned_data.get('elevation')

        # Ensure all fields are filled
        if not all([distance, difficulty, terrain, elevation]):
            form.add_error(None, "Please make sure all fields are selected.")
        else:
            # Query the database for a matching training plan
            preview_plan = Product.objects.filter(
                category='training_plan',  # Filter only training plans
                distance=distance,
                difficulty=difficulty,
                terrain=terrain,
                elevation=elevation,
            ).first()

            if not preview_plan:
                form.add_error(
                    None,
                    (
                        "No training plans available. "
                        "Please adjust your selections."
                    ),
                )

    return render(
        request,
        'products_v2/training_plans.html',
        {
            'form': form,
            'preview_plan': preview_plan,
        },
    )