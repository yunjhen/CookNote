# Generated by Django 4.1.3 on 2022-12-27 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='delicacy_type',
            field=models.CharField(choices=[('a', '開胃菜(appetizer)'), ('m', '主餐(main course)'), ('sf', '主食(staple food)'), ('s', '副菜(side)'), ('d', '甜點(dessert)'), ('b', '飲品(beverages)')], default='a', max_length=5),
        ),
    ]
