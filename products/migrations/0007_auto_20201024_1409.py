# Generated by Django 2.2.5 on 2020-10-24 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20201024_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='power',
            name='CYL',
        ),
        migrations.RemoveField(
            model_name='power',
            name='SPH',
        ),
    ]
