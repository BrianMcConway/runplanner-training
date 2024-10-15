from django.shortcuts import render, redirect, get_object_or_404
from products.models import TrainingPlan

# Add a training plan to the basket
def add_to_basket(request, distance, difficulty, terrain, elevation, event_date):
    # Retrieve or create a session basket
    basket = request.session.get('basket', {'training_plans': []})

    # Create a unique identifier for the training plan
    plan_id = f"{distance}-{difficulty}-{terrain}-{elevation}-{event_date}"

    # Add the training plan if it's not already in the basket
    if not any(plan['id'] == plan_id for plan in basket['training_plans']):
        basket['training_plans'].append({
            'id': plan_id,
            'distance': distance,
            'difficulty': difficulty,
            'terrain': terrain,
            'elevation': elevation,
            'event_date': event_date,
            'price': calculate_price(distance, difficulty),  # Calculate price based on distance and difficulty
        })

    # Update session with the new basket
    request.session['basket'] = basket
    request.session.modified = True  # Ensure the session is saved

    return redirect('basket:show_basket')

# Show the basket (retrieves session details)
def show_basket(request):
    # Retrieve the basket from the session, default to an empty basket
    basket = request.session.get('basket', {'training_plans': []})
    training_plans = basket.get('training_plans', [])

    # Calculate the total price
    total_price = sum(float(item['price']) for item in training_plans)

    # Pass the training plans and total price to the template
    context = {
        'training_plans': training_plans,
        'total_price': total_price,
    }

    return render(request, 'basket/basket.html', context)

# Remove an item from the basket
def remove_from_basket(request, item_type, item_id):
    basket = request.session.get('basket', {'training_plans': []})

    # Remove the training plan from the basket
    if item_type == 'training_plan':
        basket['training_plans'] = [item for item in basket['training_plans'] if item['id'] != item_id]

    # Update the session with the modified basket
    request.session['basket'] = basket
    request.session.modified = True  # Ensure session changes are saved

    return redirect('basket:show_basket')

# Empty the basket (clears all items)
def empty_basket(request):
    request.session['basket'] = {'training_plans': []}  # Clear the basket
    request.session.modified = True  # Ensure session changes are saved

    return redirect('basket:show_basket')

# Helper function to calculate price based on distance and difficulty
def calculate_price(distance, difficulty):
    base_price = 15
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
