# Generated by Django 2.2.5 on 2020-10-24 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20201024_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='detail_color',
            field=models.CharField(max_length=50, null=True),
        ),
    ]