# Generated by Django 3.0.8 on 2020-10-26 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_notice'),
    ]

    operations = [
        migrations.AddField(
            model_name='remark',
            name='isroot',
            field=models.BooleanField(default=True, verbose_name='是否根评论'),
        ),
    ]
