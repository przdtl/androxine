import math

from django.utils.translation import gettext as _

calculate_functions = {
    _("Epley's Formula"): lambda M, k: (M * k) / 30 + M,
    _("Brzycki's Formula"): lambda M, k: M * (36 / (37 - k)),
    _("Lander's Formula"): lambda M, k: (100 * M) / (101.3 - 2.67123 * k),
    _("O'Conner's Formula"): lambda M, k: M * (1 + 0.025 * k),
    _("Lombardi's Formula"): lambda M, k: M * k ** 0.1,
    _("Mayhew's Formula"): lambda M, k: (100 * M) / (52.2 + 41.9 * math.exp((-0.055 * k))),
    _("Wathen's Formula"): lambda M, k: (100 * M) / (48.8 + 53.8 * math.exp(-0.075 * k)),
}


def calculate_one_rep_maximum_weight(weight: float, reps: int, only_result: bool = True) -> float:
    functions_count = len(calculate_functions)
    intermediate_calculations = dict()
    calculated_sum = 0

    for function_name, function in calculate_functions.items():
        function_value = round(function(M=weight, k=reps), 2)
        calculated_sum += function_value
        intermediate_calculations[function_name] = function_value

    result = round(calculated_sum / functions_count, 2)
    result = round_up_to_barbell_weight(result)

    return result if only_result else result, intermediate_calculations


def round_up_to_barbell_weight(weight: float) -> float:
    fractional_part = weight - int(weight)
    number_before_point = int(weight) % 10
    number = number_before_point + fractional_part
    while number > 2.5:
        number -= 2.5

    result = weight
    if number >= 1.25:
        result += 2.5 - number
    else:
        result -= number

    return result
