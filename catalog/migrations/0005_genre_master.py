# Generated by Django 3.0.1 on 2020-01-23 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20200123_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='genre', to='catalog.Genre'),
        ),
    ]
