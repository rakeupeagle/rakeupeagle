# Generated by Django 3.1.2 on 2020-10-29 02:30

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20201012_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipient',
            name='geo',
            field=models.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
        ),
        migrations.AlterField(
            model_name='recipient',
            name='is_dog',
            field=models.BooleanField(help_text='If you have a dog, it must be contained in your home for us to rake.\xa0 Also, you must clean up all animal waste before we arrive or our volunteer group will not be able to rake.'),
        ),
        migrations.AlterField(
            model_name='recipient',
            name='is_verified',
            field=models.BooleanField(help_text='We are only able to service yards for persons in one of these categories.'),
        ),
        migrations.AlterField(
            model_name='recipient',
            name='is_waiver',
            field=models.BooleanField(help_text='I agree to waive and release Rake Up Eagle and the sponsors of this event, including all persons and agencies connected with this event from all claims for damages, injuries or death, arising from my participation in  this event. I will provide my own insurance and care, if necessary. I also understand and agree that Rake Up Eagle or a sponsor may subsequently use for publicity and/or promotional purposes pictures of me and my team participating in this event without obligation of liability to me. I understand that the work done on my property is done by volunteers and will not hold them or Rake Up Eagle responsible for damage to personal property. I have read this waiver carefully and having done so, I am signing voluntarily.'),
        ),
        migrations.AlterField(
            model_name='recipient',
            name='size',
            field=models.IntegerField(choices=[(110, 'Small (1-15 bags)'), (120, 'Medium (16-30 bags)'), (130, 'Large (35+ bags)')], help_text='Yard Size'),
        ),
    ]
