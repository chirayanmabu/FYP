# Generated by Django 5.0 on 2024-02-05 05:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
