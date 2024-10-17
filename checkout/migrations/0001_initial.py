# Generated by Django 5.1.1 on 2024-10-16 13:42

import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0005_nutritionproduct_remove_trainingplan_file_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('country', django_countries.fields.CountryField(default='IE', max_length=2)),
                ('street_address1', models.CharField(max_length=80)),
                ('street_address2', models.CharField(blank=True, max_length=80)),
                ('town_or_city', models.CharField(max_length=40)),
                ('county', models.CharField(blank=True, max_length=80)),
                ('postal_code', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stripe_payment_id', models.CharField(blank=True, max_length=255)),
                ('currency', models.CharField(default='EUR', max_length=3)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='checkout.order')),
                ('training_plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.trainingplan')),
            ],
        ),
    ]
