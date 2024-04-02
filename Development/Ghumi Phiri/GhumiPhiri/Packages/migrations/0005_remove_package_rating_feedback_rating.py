# Generated by Django 5.0 on 2024-03-31 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Packages', '0004_package_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='rating',
        ),
        migrations.AddField(
            model_name='feedback',
            name='rating',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]