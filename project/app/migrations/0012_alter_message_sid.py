# Generated by Django 5.1.1 on 2024-09-15 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_message_sid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sid',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]