from django.contrib import admin
from .models import TrainingPlan

@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'distance', 'difficulty', 'terrain', 'price')
    search_fields = ('name', 'distance', 'difficulty')
