# Generated by Django 4.1.3 on 2023-01-02 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0003_alter_nutrition_facts_calories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='name',
            new_name='ingredient',
        ),
    ]
