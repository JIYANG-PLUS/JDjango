# Generated by Django 2.2.1 on 2020-11-06 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20201106_1139'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name': '账户扩展信息', 'verbose_name_plural': '账户扩展信息'},
        ),
    ]
