# Generated by Django 5.0 on 2024-03-30 03:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Packages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='booked_by',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='feedback_author',
        ),
        migrations.RemoveField(
            model_name='package',
            name='package_author',
        ),
    ]
