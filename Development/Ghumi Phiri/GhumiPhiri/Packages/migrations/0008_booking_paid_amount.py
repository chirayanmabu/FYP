# Generated by Django 5.0 on 2024-04-05 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Packages', '0007_alter_booking_package'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='paid_amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
