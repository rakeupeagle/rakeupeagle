# Generated by Django 3.1.3 on 2020-11-16 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20201116_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='hours',
            field=models.FloatField(blank=True, help_text='Actual Hours Worked', null=True),
        ),
    ]