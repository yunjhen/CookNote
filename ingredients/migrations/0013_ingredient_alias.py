# Generated by Django 4.1.3 on 2023-01-28 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0012_ingredient_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='alias',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
