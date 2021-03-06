# Generated by Django 2.2.5 on 2020-10-24 05:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20201024_1354'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='colortype',
            options={'verbose_name': 'Color Type'},
        ),
        migrations.AlterModelOptions(
            name='lenstype',
            options={'verbose_name': 'Lens Type'},
        ),
        migrations.AlterModelOptions(
            name='power',
            options={'verbose_name': 'Power'},
        ),
        migrations.AlterField(
            model_name='power',
            name='AXIS',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(180)]),
        ),
    ]
