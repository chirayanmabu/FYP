# Generated by Django 5.0 on 2024-02-01 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_packages_package'),
    ]

    operations = [
        migrations.RenameField(
            model_name='package',
            old_name='packages_desc',
            new_name='package_desc',
        ),
    ]