# Generated by Django 4.1.3 on 2023-01-12 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_recipe_delicacy_photo_alter_step_step_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
        ),
    ]
