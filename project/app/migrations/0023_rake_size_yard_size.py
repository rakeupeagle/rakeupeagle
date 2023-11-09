# Generated by Django 4.2.6 on 2023-11-09 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_assignment_rake_alter_assignment_yard'),
    ]

    operations = [
        migrations.AddField(
            model_name='rake',
            name='size',
            field=models.IntegerField(blank=True, choices=[(105, 'Solo (1 Adult)'), (110, 'Extra-Small (2-5 Adults)'), (120, 'Small (6-10 Adults)'), (130, 'Medium (11-15 Adults)'), (140, 'Large (16-20 Adults)'), (150, 'Extra-Large (21+ Adults)')], null=True),
        ),
        migrations.AddField(
            model_name='yard',
            name='size',
            field=models.IntegerField(blank=True, choices=[(110, 'Small (1-15 bags)'), (120, 'Medium (16-30 bags)'), (130, 'Large (31+ bags)')], null=True),
        ),
    ]
