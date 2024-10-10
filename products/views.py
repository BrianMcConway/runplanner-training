from django.shortcuts import render, redirect
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

# View to handle adding a training plan to the basket
def add_to_basket(request, distance, difficulty, terrain, elevation, event_date):
    # Capitalize difficulty and terrain before storing in session
    difficulty = difficulty.capitalize() if difficulty else difficulty
    terrain = terrain.capitalize() if terrain else terrain

    # Store the values in the session when the user clicks 'Add to Basket'
    request.session['distance'] = distance
    request.session['difficulty'] = difficulty
    request.session['terrain'] = terrain
    request.session['elevation'] = elevation
    request.session['event_date'] = event_date

    # Calculate the price based on the distance and difficulty, and store it
    price = calculate_price(distance, difficulty)
    request.session['grand_total'] = price

    # Redirect the user to the basket page after adding the plan
    return redirect('basket')

# View to handle the basket where the user confirms purchasing a training plan
def basket(request):
    # Retrieve values from the session
    distance = request.session.get('distance')
    difficulty = request.session.get('difficulty')
    terrain = request.session.get('terrain')
    elevation = request.session.get('elevation')
    event_date = request.session.get('event_date')
    price = request.session.get('grand_total', None)  # Get the price, default to None if not set

    # Check if the basket is empty (i.e., no grand_total set)
    if not price:
        # If the price isn't set, assume the basket is empty
        return render(request, 'products/basket.html', {
            'message': 'Your basket is empty.',
        })

    # If there's a price, show the basket details
    return render(request, 'products/basket.html', {
        'distance': distance,
        'difficulty': difficulty,
        'terrain': terrain,
        'elevation': elevation,
        'event_date': event_date,
        'price': price,
    })

# View to remove items from the basket by clearing the session
def remove_from_basket(request):
    # Clear specific session keys related to the basket
    keys_to_clear = ['distance', 'difficulty', 'terrain', 'elevation', 'event_date', 'grand_total']
    for key in keys_to_clear:
        request.session.pop(key, None)  # Safely remove the keys if they exist

    # Redirect back to the basket page after clearing
    return redirect('basket')
