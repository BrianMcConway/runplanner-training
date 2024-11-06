from django.db import models

class Product(models.Model):
    """Model representing a product, which can be a training plan or nutrition item."""

    CATEGORY_CHOICES = [
        ('training_plan', 'Training Plan'),
        ('nutrition', 'Nutrition'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='training_plan')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True)

    DISTANCE_CHOICES = [
        ('5k', '5k'),
        ('10k', '10k'),
        ('half_marathon', 'Half Marathon'),
        ('marathon', 'Marathon'),
        ('50k', '50k'),
        ('80k', '80k'),
        ('100k', '100k'),
        ('160k', '160k'),
        ('200k', '200k'),
    ]
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    TERRAIN_CHOICES = [
        ('road', 'Road'),
        ('trail', 'Trail'),
        ('mixed', 'Mixed'),
    ]
    ELEVATION_CHOICES = [
        ('0-500m', '0-500m'),
        ('500-1000m', '500-1000m'),
        ('1000-1500m', '1000-1500m'),
        ('1500-2000m', '1500-2000m'),
        ('2000-2500m', '2000-2500m'),
        ('2500-3000m', '2500-3000m'),
        ('3000-3500m', '3000-3500m'),
        ('3500-4000m', '3500-4000m'),
        ('4000-4500m', '4000-4500m'),
        ('4500-5000m', '4500-5000m'),
        ('5000-5500m', '5000-5500m'),
        ('5500-6000m', '5500-6000m'),
        ('6000-6500m', '6000-6500m'),
        ('6500-7000m', '6500-7000m'),
        ('7000-7500m', '7000-7500m'),
        ('7500-8000m', '7500-8000m'),
        ('8000-8500m', '8000-8500m'),
        ('8500-9000m', '8500-9000m'),
        ('9000-9500m', '9000-9500m'),
        ('9500-10000m', '9500-10000m'),
    ]

    distance = models.CharField(max_length=20, choices=DISTANCE_CHOICES, blank=True, null=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, blank=True, null=True)
    terrain = models.CharField(max_length=20, choices=TERRAIN_CHOICES, blank=True, null=True)
    elevation = models.CharField(max_length=20, choices=ELEVATION_CHOICES, blank=True, null=True)

    def __str__(self):
        """String representation of the Product."""
        return self.name
