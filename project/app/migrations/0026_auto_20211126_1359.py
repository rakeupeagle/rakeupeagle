# Generated by Django 3.2.9 on 2021-11-26 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20211126_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipients', to='app.event'),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='volunteers', to='app.event'),
        ),
    ]
