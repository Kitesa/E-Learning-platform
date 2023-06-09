# Generated by Django 4.2 on 2023-04-25 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlequestion',
            name='add_options_under_article',
            field=models.BooleanField(default=1),
        ),
        migrations.AlterField(
            model_name='articlequestion',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='articles.article'),
        ),
    ]
