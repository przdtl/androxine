# Generated by Django 5.0.7 on 2024-08-11 11:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout_template', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exerciseapproachinworkouttemplate',
            name='ordinal_number',
            field=models.SmallIntegerField(default=1, editable=False, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='exerciseinworkouttemplate',
            name='ordinal_number',
            field=models.SmallIntegerField(default=1, editable=False, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
