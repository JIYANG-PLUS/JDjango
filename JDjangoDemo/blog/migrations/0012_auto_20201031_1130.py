# Generated by Django 3.0.8 on 2020-10-31 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20201029_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='title',
            field=models.CharField(max_length=100, verbose_name='公告标题'),
        ),
    ]
