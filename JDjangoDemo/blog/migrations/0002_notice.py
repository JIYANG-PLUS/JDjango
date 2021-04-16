# Generated by Django 3.0.8 on 2020-10-26 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='公告内容')),
                ('accept', models.PositiveIntegerField(default=0, verbose_name='收到')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('noticer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notices', to=settings.AUTH_USER_MODEL, verbose_name='发布人')),
            ],
            options={
                'verbose_name': '公告',
                'verbose_name_plural': '公告',
            },
        ),
    ]
