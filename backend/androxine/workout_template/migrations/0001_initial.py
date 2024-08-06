# Generated by Django 5.0.7 on 2024-08-06 10:27

import config.utils
import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exercise', '0003_remove_exercisecategory_slug_alter_exercise_slug_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseInWorkoutTemplate',
            fields=[
                ('id', models.UUIDField(default=config.utils.current_timestamp_ulid, editable=False, primary_key=True, serialize=False, unique=True)),
                ('ordinal_number', models.SmallIntegerField(default=1, editable=False, unique=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.exercise')),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseApproachInWorkoutTemplate',
            fields=[
                ('id', models.UUIDField(default=config.utils.current_timestamp_ulid, editable=False, primary_key=True, serialize=False, unique=True)),
                ('relative_weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('absolute_weight', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('reps', models.PositiveIntegerField(default=0)),
                ('ordinal_number', models.SmallIntegerField(default=1, editable=False, unique=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('exercise_in_workout_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approaches', to='workout_template.exerciseinworkouttemplate')),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutTemplate',
            fields=[
                ('id', models.UUIDField(default=config.utils.current_timestamp_ulid, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('break_between_approaches', models.PositiveSmallIntegerField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='exerciseinworkouttemplate',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='workout_template.workouttemplate'),
        ),
        migrations.AddConstraint(
            model_name='workouttemplate',
            constraint=models.UniqueConstraint(fields=('created_by', 'name'), name='unique template name for every user'),
        ),
        migrations.AddConstraint(
            model_name='exerciseinworkouttemplate',
            constraint=models.UniqueConstraint(fields=('exercise', 'template'), name='unique exercise for every template'),
        ),
    ]
