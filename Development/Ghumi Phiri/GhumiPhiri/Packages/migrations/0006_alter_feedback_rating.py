# Generated by Django 5.0 on 2024-04-01 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Packages', '0005_remove_package_rating_feedback_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='rating',
            field=models.IntegerField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], null=True),
        ),
    ]
