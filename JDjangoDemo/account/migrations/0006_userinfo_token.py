# Generated by Django 3.0.8 on 2020-11-05 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_passwordresetlog_ensure'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='token',
            field=models.CharField(default=0, max_length=32, verbose_name='用户唯一标识码'),
            preserve_default=False,
        ),
    ]
