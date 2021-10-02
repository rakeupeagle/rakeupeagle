# Generated by Django 3.2.7 on 2021-10-02 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20211002_0704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipient',
            name='adults',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='children',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='adults',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='assignment',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='children',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='number',
        ),
        migrations.AddField(
            model_name='recipient',
            name='account',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='raccount', to='app.account'),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='account',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vaccount', to='app.account'),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='size',
            field=models.IntegerField(choices=[(110, 'Extra-Small (1-5 Adults)'), (120, 'Small (6-10 Adults)'), (130, 'Medium (11-15 Adults)'), (140, 'Large (16-20 Adults)'), (150, 'Extra-Large (21+ Adults)')], help_text='The size of your group.'),
        ),
    ]