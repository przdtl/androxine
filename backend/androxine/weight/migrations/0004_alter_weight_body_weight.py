# Generated by Django 5.1.1 on 2024-10-03 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weight', '0003_userworkoutsettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weight',
            name='body_weight',
            field=models.DecimalField(decimal_places=1, max_digits=4),
        ),
    ]