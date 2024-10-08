# Generated by Django 5.1 on 2024-09-13 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_recipient_name_recipient_phone_team_name_team_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='size',
            field=models.IntegerField(choices=[(110, 'Small (1-15 bags)'), (120, 'Medium (16-30 bags)'), (130, 'Large (31+ bags)')], help_text='Please provide the approximate yard size.'),
        ),
    ]
