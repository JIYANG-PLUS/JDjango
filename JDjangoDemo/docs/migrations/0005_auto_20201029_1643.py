# Generated by Django 3.0.8 on 2020-10-29 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0004_article_iswrite'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': '接口', 'verbose_name_plural': '接口'},
        ),
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name': '菜单', 'verbose_name_plural': '菜单'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='votes',
        ),
        migrations.CreateModel(
            name='ArticleA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_time', models.PositiveIntegerField(default=0, verbose_name='调用次数')),
                ('votes', models.PositiveIntegerField(default=0, verbose_name='支持数')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articleA', to='docs.Article', verbose_name='接口')),
            ],
            options={
                'verbose_name': '接口互动',
                'verbose_name_plural': '接口互动',
            },
        ),
    ]
