# Generated by Django 3.0.8 on 2020-10-23 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20201023_1340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passwordresetlog',
            name='ensure',
        ),
    ]
