# Generated by Django 2.2.5 on 2020-10-24 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20201024_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='detail_color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
