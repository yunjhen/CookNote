# Generated by Django 4.1.3 on 2023-01-06 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0004_rename_name_ingredient_ingredient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='used_ingredient',
            old_name='quantity',
            new_name='serving',
        ),
    ]
