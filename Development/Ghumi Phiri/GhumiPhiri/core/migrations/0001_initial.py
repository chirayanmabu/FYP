# Generated by Django 5.0 on 2023-12-31 15:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('username', models.CharField(max_length=200)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.CharField(max_length=200)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('profile_pic', models.ImageField(blank=True, default='profile_pic/default_picture.jpg', null=True, upload_to='profile_pictures/')),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('dob', models.DateField(blank=True, max_length=200, null=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
            ],
        ),
    ]