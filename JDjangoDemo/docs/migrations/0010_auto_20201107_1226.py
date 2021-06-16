# Generated by Django 2.2.1 on 2020-11-07 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0009_limitlinkplugin_access_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='limitlinkplugin',
            options={'verbose_name': '授权码', 'verbose_name_plural': '授权码'},
        ),
        migrations.AlterField(
            model_name='limitlinkplugin',
            name='access_code',
            field=models.CharField(max_length=8, unique=True, verbose_name='授权码'),
        ),
        migrations.AlterField(
            model_name='plugin',
            name='only_code',
            field=models.CharField(max_length=32, unique=True, verbose_name='接口唯一标识'),
        ),
    ]