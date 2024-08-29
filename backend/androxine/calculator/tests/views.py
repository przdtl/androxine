import uuid

from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import NotAuthenticated, NotFound

from calculator.services import calculate_one_rep_maximum_weight
from calculator.serializers import CalculateSerializer
from exercise.models import Exercise, ExerciseCategory
from workout.models import Workout, ExerciseInWorkout, ExerciseApproachInWorkout

UserModel = get_user_model()


class CalculateViewTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url_name = 'calculator:calculate'

    def test_calculate_weight_by_non_auth_user(self):
        request_data = {
            'weight': 55,
            'reps': 10,
            'only_result': True
        }
        url = f'{reverse_lazy(self.url_name)}?{urlencode(request_data)}'
        response = self.client.get(url)
        result = calculate_one_rep_maximum_weight(**request_data)
        result_data = {'result': result}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, result_data)

    def test_calculate_weight_by_auth_user(self):
        self.user = UserModel.objects.create_user(
            username='user',
            email='test@test.com',
            password='asdSsd4223_ssas42?',
        )
        self.client.login(
            username='user',
            password='asdSsd4223_ssas42?',
        )
        request_data = {
            'weight': 94,
            'reps': 8,
            'only_result': True
        }
        url = f'{reverse_lazy(self.url_name)}?{urlencode(request_data)}'
        response = self.client.get(url)
        result = calculate_one_rep_maximum_weight(**request_data)
        result_data = {'result': result}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, result_data)

    def test_pass_reps_less_than_2(self):
        request_data = {
            'weight': 100,
            'reps': 1,
            'only_result': True
        }
        url = f'{reverse_lazy(self.url_name)}?{urlencode(request_data)}'
        response = self.client.get(url)
        serializer = CalculateSerializer(data=request_data)
        serializer.is_valid()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)

    def test_pass_reps_more_than_15(self):
        request_data = {
            'weight': 50,
            'reps': 20,
            'only_result': True
        }
        url = f'{reverse_lazy(self.url_name)}?{urlencode(request_data)}'
        response = self.client.get(url)
        serializer = CalculateSerializer(data=request_data)
        serializer.is_valid()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)

    def test_pass_weight_more_than_1000(self):
        request_data = {
            'weight': 1001,
            'reps': 3,
            'only_result': True
        }
        url = f'{reverse_lazy(self.url_name)}?{urlencode(request_data)}'
        response = self.client.get(url)
        serializer = CalculateSerializer(data=request_data)
        serializer.is_valid()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)

    def test_pass_weight_less_than_0_1(self):
        request_data = {
            'weight': 0,
            'reps': 10,
            'only_result': True
        }
        url = f'{reverse_lazy(self.url_name)}?{urlencode(request_data)}'
        response = self.client.get(url)
        serializer = CalculateSerializer(data=request_data)
        serializer.is_valid()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)


class CalculateByApproachViewTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url_name = 'calculator:calculate_by_approach'

    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='user',
            email='test@test.com',
            password='asdSsd4223_ssas42?',
        )
        self.client.login(
            username='user',
            password='asdSsd4223_ssas42?',
        )
        self.nogi = ExerciseCategory.objects.create(
            name='ноги',
        )
        self.prised = Exercise.objects.create(
            category=self.nogi,
            name='присед'
        )
        self.workout = Workout.objects.create(
            created_by=self.user,
        )
        self.nogi_in_workout = ExerciseInWorkout.objects.create(
            workout=self.workout,
            exercise=self.prised,
        )
        self.approach = ExerciseApproachInWorkout.objects.create(
            exercise_in_workout=self.nogi_in_workout,
            weight=100,
            reps=5,
        )

    def test_calculate_by_approach_by_non_auth_user(self):
        self.client.logout()
        request_data = {
            'approach_id': self.approach.id,
            'only_result': True
        }
        url = f'{reverse_lazy(self.url_name)}?{urlencode(request_data)}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {
            'detail': NotAuthenticated.default_detail
        })

    def test_calculate_by_non_exists_approach_id(self):
        request_data = {
            'approach_id': uuid.uuid4(),
            'only_result': True
        }
        url = f'{reverse_lazy(self.url_name)}?{urlencode(request_data)}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {
            'detail': NotFound('No ExerciseApproachInWorkout matches the given query.').detail
        })

    def test_calculate_by_approach_only_result(self):
        request_data = {
            'approach_id': self.approach.id,
            'only_result': True
        }
        url = f'{reverse_lazy(self.url_name)}?{urlencode(request_data)}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'result': 115.0})

    def test_calculate_by_approach_verbose_response(self):
        request_data = {
            'approach_id': self.approach.id,
            'only_result': False
        }
        url = f'{reverse_lazy(self.url_name)}?{urlencode(request_data)}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'result': 115.0,
            'functions': {
                "Epley's Formula": 116.67,
                "Brzycki's Formula": 112.5,
                "Lander's Formula": 113.71,
                "O'Conner's Formula": 112.5,
                "Lombardi's Formula": 117.46,
                "Mayhew's Formula": 119.01,
                "Wathen's Formula": 116.58
            }})
