# Generated by Django 4.1.3 on 2023-01-12 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_alter_step_recipe'),
        ('ingredients', '0010_alter_nutrition_facts_ingredient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='used_ingredient',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
        ),
    ]
