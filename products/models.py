from django.db import models

class TrainingPlan(models.Model):
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
        ('0-500m', '0m-500m'),
        ('500-1000m', '500m-1000m'),
        ('1000-1500m', '1000m-1500m'),
        ('1500-2000m', '1500m-2000m'),
        ('2000-2500m', '2000m-2500m'),
        ('2500-3000m', '2500m-3000m'),
        ('3000-3500m', '3000m-3500m'),
        ('3500-4000m', '3500m-4000m'),
        ('4000-4500m', '4000m-4500m'),
        ('4500-5000m', '4500m-5000m'),
        ('5000-5500m', '5000m-5500m'),
        ('5500-6000m', '5500m-6000m'),
        ('6000-6500m', '6000m-6500m'),
        ('6500-7000m', '6500m-7000m'),
        ('7000-7500m', '7000m-7500m'),
        ('7500-8000m', '7500m-8000m'),
        ('8000-8500m', '8000m-8500m'),
        ('8500-9000m', '8500m-9000m'),
        ('9000-9500m', '9000m-9500m'),
        ('9500-10000m', '9500m-10000m'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    distance = models.CharField(choices=DISTANCE_CHOICES, max_length=20)
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, max_length=20)
    terrain = models.CharField(choices=TERRAIN_CHOICES, max_length=20)
    elevation = models.CharField(choices=ELEVATION_CHOICES, max_length=20)
    event_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.distance}, {self.difficulty}, {self.terrain}, {self.elevation})"

    # Helper method to calculate the price
    def calculate_price(self):
        base_price = 15  # Starting base price
        difficulty_increment = 3
        distance_increment = {
            '5k': 0, '10k': 3, 'half_marathon': 6,
            'marathon': 9, '50k': 12, '80k': 15,
            '100k': 18, '160k': 21, '200k': 24,
        }

        price = base_price + distance_increment.get(self.distance, 0)
        if self.difficulty == 'intermediate':
            price += difficulty_increment
        elif self.difficulty == 'advanced':
            price += 2 * difficulty_increment
        return price

class NutritionProduct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    brand = models.CharField(max_length=100)
    weight = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.brand})"