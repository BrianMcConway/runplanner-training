from django.db import models
from django.contrib.auth.models import User
from products_v2.models import Product

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    training_plan = models.ForeignKey(Product, on_delete=models.CASCADE, limit_choices_to={'category': 'training_plan'})
    purchase_date = models.DateTimeField(auto_now_add=True)
    payment_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.training_plan.title}"
