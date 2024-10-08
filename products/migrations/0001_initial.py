# Generated by Django 5.1.1 on 2024-09-27 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('distance', models.CharField(choices=[('5K', '5K'), ('10K', '10K'), ('HALF_MARATHON', 'Half Marathon'), ('MARATHON', 'Marathon'), ('50K', '50K'), ('80K', '80K'), ('100K', '100K'), ('160K', '160K'), ('200K', '200K')], max_length=20)),
                ('difficulty', models.CharField(choices=[('BEGINNER', 'Beginner'), ('INTERMEDIATE', 'Intermediate'), ('ADVANCED', 'Advanced')], max_length=20)),
                ('terrain', models.CharField(choices=[('ROAD', 'Road'), ('TRAIL', 'Trail')], max_length=10)),
                ('elevation', models.CharField(choices=[('0', '0m'), ('500', '500m'), ('1000', '1000m'), ('1500', '1500m'), ('2000', '2000m'), ('2500', '2500m'), ('3000', '3000m'), ('3500', '3500m'), ('4000', '4000m'), ('4500', '4500m'), ('5000', '5000m'), ('5500', '5500m'), ('6000', '6000m'), ('6500', '6500m'), ('7000', '7000m'), ('7500', '7500m'), ('8000', '8000m'), ('8500', '8500m'), ('9000', '9000m'), ('9500', '9500m'), ('10000', '10000m')], max_length=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='training_plans/')),
                ('file', models.FileField(blank=True, null=True, upload_to='training_plans/')),
                ('sample_file', models.FileField(blank=True, null=True, upload_to='training_plans/samples/')),
            ],
        ),
    ]
