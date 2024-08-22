# Generated by Django 5.1 on 2024-08-22 09:13

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0006_rename_temp_id_userexercisesettings_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, blank=True, editable=False, max_length=255, populate_from='name', unique=True),
        ),
    ]