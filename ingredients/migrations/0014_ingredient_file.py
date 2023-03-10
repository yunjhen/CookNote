# Generated by Django 4.1.3 on 2023-01-28 13:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0013_ingredient_alias'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient_File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='ingredients/files')),
                ('upload_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]
