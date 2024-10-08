from django.shortcuts import render, redirect
from PIL import Image, ImageDraw, ImageFont
import io
from django.http import HttpResponse
from .forms import TrainingPlanFilterForm
from django.utils.dateformat import format as date_format
from django.utils import timezone

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

        # Format the date in a URL-safe format (dd-mm-yyyy)
        formatted_event_date = date_format(event_date, 'd-m-Y')

        return render(request, 'products/plan_preview.html', {
            'distance': distance,
            'difficulty': difficulty,
            'terrain': terrain,
            'elevation': elevation,
            'event_date': formatted_event_date,  # Use URL-safe format
        })

    # Render the form with validation errors if not valid
    return render(request, 'products/training_plans.html', {
        'form': form,
    })

# Generate dynamic training plan image with 'SAMPLE' text
def generate_plan_image(request, distance, difficulty, terrain, elevation, event_date):
    # Calculate the price using the helper function
    price = calculate_price(distance, difficulty)

    # Capitalize the first letter of difficulty and terrain
    difficulty = difficulty.title()
    terrain = terrain.title()

    # Create a new image with hex background color
    img = Image.new('RGB', (600, 400), color='#496D89')
    draw = ImageDraw.Draw(img)

    try:
        # Try loading fonts
        font = ImageFont.truetype("DejaVuSans.ttf", 20)
        price_font = ImageFont.truetype("DejaVuSans.ttf", 30)
        sample_font = ImageFont.truetype("DejaVuSans.ttf", 50)
    except IOError:
        # Use default font if custom font fails
        font = ImageFont.load_default()
        price_font = ImageFont.load_default()
        sample_font = ImageFont.load_default()

    # Add 'SAMPLE' text prominently in the center of the image
    sample_bbox = draw.textbbox((0, 0), "SAMPLE", font=sample_font)
    text_width = sample_bbox[2] - sample_bbox[0]
    sample_x = (img.width - text_width) // 2
    sample_y = 20
    draw.text((sample_x, sample_y), "SAMPLE", font=sample_font, fill=(255, 255, 255))

    # Add selected plan details lower down
    draw.text((10, 150), f"Training Plan", font=font, fill=(255, 255, 255))
    draw.text((10, 180), f"Distance: {distance}", font=font, fill=(255, 255, 255))
    draw.text((10, 210), f"Difficulty: {difficulty}", font=font, fill=(255, 255, 255))
    draw.text((10, 240), f"Terrain: {terrain}", font=font, fill=(255, 255, 255))
    draw.text((10, 270), f"Elevation: {elevation}", font=font, fill=(255, 255, 255))
    draw.text((10, 300), f"Event Date: {event_date}", font=font, fill=(255, 255, 255))  # Date in dd-mm-yyyy format
    # Handle Euro symbol for default font
    euro_symbol = "€" if font.getmask("€") else "EUR"  # Check if the font supports Euro symbol
    # Add the price to the image with a larger font
    draw.text((10, 340), f"Price: {euro_symbol}{price:.2f}", font=price_font, fill=(255, 255, 255))

    # Save the image to a buffer
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    # Return the image as an HTTP response
    return HttpResponse(buffer, content_type='image/png')

# View to handle the basket where the user confirms purchasing a training plan
def basket(request, distance, difficulty, terrain, elevation, event_date):
    # Calculate the price using the same logic
    price = calculate_price(distance, difficulty)

    # Capitalize the first letter of difficulty and terrain
    difficulty = difficulty.title()
    terrain = terrain.title()

    # Render the basket.html
    return render(request, 'products/basket.html', {
        'distance': distance,
        'difficulty': difficulty,  # Capitalized Difficulty
        'terrain': terrain,  # Capitalized Terrain
        'elevation': elevation,
        'event_date': event_date,
        'price': price,  # Pass the calculated price to the template
    })
