from django.shortcuts import render, redirect
from PIL import Image, ImageDraw, ImageFont
import io
from django.http import HttpResponse
from .forms import TrainingPlanFilterForm
from django.utils.dateformat import format as date_format
from django.utils import timezone

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
    # Create a new image with hex background color
    img = Image.new('RGB', (600, 400), color='#496D89')  # Increased the image size for more space
    draw = ImageDraw.Draw(img)

    try:
        # Try loading fonts
        font = ImageFont.truetype("arial.ttf", 20)  # Standard font for plan details
        sample_font = ImageFont.truetype("arial.ttf", 50)  # Larger font for 'SAMPLE'
    except IOError:
        # Use default font if custom font fails
        font = ImageFont.load_default()
        sample_font = ImageFont.load_default()

    # Add 'SAMPLE' text prominently in the center of the image
    # Use textbbox to calculate text size
    sample_bbox = draw.textbbox((0, 0), "SAMPLE", font=sample_font)
    text_width = sample_bbox[2] - sample_bbox[0]  # Calculate the width
    text_height = sample_bbox[3] - sample_bbox[1]  # Calculate the height
    sample_x = (img.width - text_width) // 2  # Center 'SAMPLE' horizontally
    sample_y = 20  # Position 'SAMPLE' near the top
    draw.text((sample_x, sample_y), "SAMPLE", font=sample_font, fill=(255, 255, 255))

    # Add selected plan details lower down
    draw.text((10, 150), f"Training Plan", font=font, fill=(255, 255, 255))
    draw.text((10, 180), f"Distance: {distance}", font=font, fill=(255, 255, 255))
    draw.text((10, 210), f"Difficulty: {difficulty}", font=font, fill=(255, 255, 255))
    draw.text((10, 240), f"Terrain: {terrain}", font=font, fill=(255, 255, 255))
    draw.text((10, 270), f"Elevation: {elevation}", font=font, fill=(255, 255, 255))
    draw.text((10, 300), f"Event Date: {event_date}", font=font, fill=(255, 255, 255))  # Date in dd-mm-yyyy format

    # Save the image to a buffer
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    # Return the image as an HTTP response
    return HttpResponse(buffer, content_type='image/png')

# View to handle the basket where the user confirms purchasing a training plan
def basket(request, distance, difficulty, terrain, elevation, event_date):
    # Render the basket.html
    return render(request, 'products/basket.html', {
        'distance': distance,
        'difficulty': difficulty,
        'terrain': terrain,
        'elevation': elevation,
        'event_date': event_date
    })
