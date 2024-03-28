# Generated by Django 5.0 on 2024-03-10 03:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_booking_booking_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank=True, null=True, upload_to='package_pictures/')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.package')),
            ],
        ),
    ]