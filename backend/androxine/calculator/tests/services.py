from django.test import TestCase

from ddt import data, unpack, ddt

from calculator.services import calculate_one_rep_maximum_weight, round_up_to_barbell_weight


@ddt
class RoundUpToBarbellWeightTestCase(TestCase):
    @data(
        (61.4, 62.5),
        (33.11, 32.5),
        (16.09, 15.0),
        (67.75, 67.5),
        (16.69, 17.5),
        (55.29, 55.0),
        (5.3, 5.0),
    )
    @unpack
    def test_round_weight(self, value, result):
        self.assertEqual(round_up_to_barbell_weight(value), result)


@ddt
class CalculateOneRepMaxWeightTestCase(TestCase):
    @data(
        (100, 10, 130.0),
        (100, 5, 115.0),
        (65, 5, 75.0),
        (95, 8, 117.5),
        (70, 6, 82.5),
        (90, 6, 107.5),
        (90, 10, 117.5),
        (60, 7, 72.5),
    )
    @unpack
    def test_one_rep_max_weight_calculator(self, weight, reps, result):
        self.assertEqual(calculate_one_rep_maximum_weight(
            weight, reps, only_result=True), result
        )
