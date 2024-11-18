from datetime import date
from django.utils.text import slugify
from products_v2.models import Product

# Define the possible options for each field
distance_options = [
    '5k', '10k', 'half_marathon', 'marathon', '50k', '80k',
    '100k', '160k', '200k'
]
difficulty_options = ['beginner', 'intermediate', 'advanced']
terrain_options = ['road', 'trail', 'mixed']
elevation_options = [
    '0-500m', '500-1000m', '1000-1500m', '1500-2000m', '2000-2500m',
    '2500-3000m', '3000-3500m', '3500-4000m', '4000-4500m', '4500-5000m',
    '5000-5500m', '5500-6000m', '6000-6500m', '6500-7000m', '7000-7500m',
    '7500-8000m', '8000-8500m', '8500-9000m', '9000-9500m', '9500-10000m'
]

# Helper function to calculate the price based on distance and difficulty


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

# Iterate through all combinations of distance,
    difficulty, terrain, elevation


def generate_training_plans():
    for distance in distance_options:
        for difficulty in difficulty_options:
            for terrain in terrain_options:
                for elevation in elevation_options:
                    # Generate the name for the plan
                    name = (
                        f"{distance.capitalize()} {difficulty.capitalize()} "
                        f"({terrain.capitalize()} {elevation})"
                    )

                    # Calculate price using the helper function
                    price = calculate_price(distance, difficulty)

                    # Generate a slug for the training plan
                    slug = slugify(name)

                    # Check if the plan already exists to avoid duplicates
                    if not TrainingPlan.objects.filter(
                        name=name,
                        distance=distance,
                        difficulty=difficulty,
                        terrain=terrain,
                        elevation=elevation,
                        slug=slug
                    ).exists():
                        # Create and save the training plan
                        training_plan = TrainingPlan(
                            name=name,
                            distance=distance,
                            difficulty=difficulty,
                            terrain=terrain,
                            elevation=elevation,
                            price=price,
                            slug=slug
                        )
                        training_plan.save()


# Run the script
generate_training_plans()