from django.shortcuts import render
from .forms import TrainingPlanFilterForm
from django.utils.dateformat import format as date_format
from .models import TrainingPlan

# Helper function to calculate price based on distance and difficulty
def calculate_price(distance, difficulty):
    base_price = 15  # Starting price
    difficulty_increment = 3
    distance_increment = {
        '5k': 0,
        '10k': 3,
        'half_marathon': 6,
        'marathon': 9,
        '50k': 12,
        '80k': 15,
        '100k': 18,
        '160k': 21,
        '200k': 24,
    }
    price = base_price + distance_increment.get(distance, 0)
    if difficulty == 'intermediate':
        price += difficulty_increment
    elif difficulty == 'advanced':
        price += 2 * difficulty_increment
    return price

# View for selecting the training plan
def training_plans(request):
    form = TrainingPlanFilterForm(request.GET or None)

    # Validate form data using Django's built-in validation
    if form.is_valid():
        distance = form.cleaned_data.get('distance')
        difficulty = form.cleaned_data.get('difficulty')
        terrain = form.cleaned_data.get('terrain')
        elevation = form.cleaned_data.get('elevation')
        event_date = form.cleaned_data.get('event_date')

        # Capitalize difficulty and terrain values for proper display
        difficulty = difficulty.capitalize() if difficulty else difficulty
        terrain = terrain.capitalize() if terrain else terrain

        # Convert distance to readable version
        distance_choices = dict(TrainingPlan.DISTANCE_CHOICES)
        distance_display = distance_choices.get(distance, distance)  # Get the readable value

        # Calculate price, but do not store it in the session yet
        price = calculate_price(distance, difficulty)

        return render(request, 'products/plan_preview.html', {
            'distance': distance_display,
            'difficulty': difficulty,
            'terrain': terrain,
            'elevation': elevation,
            'event_date': date_format(event_date, 'd-m-Y'),  # Use URL-safe format
            'price': price,
        })

    # Render the form with validation errors if not valid
    return render(request, 'products/training_plans.html', {
        'form': form,
    })
