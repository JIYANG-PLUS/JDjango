# Generated by Django 2.2.1 on 2020-11-02 20:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0012_auto_20201031_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion',
            name='isvalid',
            field=models.BooleanField(default=False, verbose_name='参与投票'),
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='votes',
            field=models.PositiveIntegerField(default=0, verbose_name='投票数'),
        ),
        migrations.CreateModel(
            name='SuggestVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isvote', models.BooleanField(default=False, verbose_name='已投票')),
                ('suggest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='svotes', to='blog.Suggestion', verbose_name='建议')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to=settings.AUTH_USER_MODEL, verbose_name='投票人')),
            ],
            options={
                'verbose_name': '建议投票情况',
                'verbose_name_plural': '建议投票情况',
            },
        ),
    ]
