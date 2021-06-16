# Generated by Django 3.0.8 on 2020-10-28 15:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20201027_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='title',
            field=models.CharField(default=django.utils.timezone.now, max_length=15, verbose_name='公告标题'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notice',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='公告时间'),
        ),
    ]