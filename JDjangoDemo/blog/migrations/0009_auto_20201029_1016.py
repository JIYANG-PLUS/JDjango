# Generated by Django 3.0.8 on 2020-10-29 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_pluginsamples_pluginpk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pluginsamples',
            name='pluginPk',
        ),
        migrations.AddField(
            model_name='pluginsamples',
            name='pluginId',
            field=models.PositiveIntegerField(default=0, verbose_name='父id'),
            preserve_default=False,
        ),
    ]
