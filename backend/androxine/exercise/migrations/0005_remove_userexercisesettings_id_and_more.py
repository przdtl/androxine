# Generated by Django 5.0.6 on 2024-08-21 03:40

import config.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0004_userexercisesettings_temp_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userexercisesettings',
            name='id',
        ),
        migrations.AlterField(
            model_name='userexercisesettings',
            name='temp_id',
            field=models.UUIDField(default=config.utils.current_timestamp_ulid, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]