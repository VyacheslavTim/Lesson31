from rest_framework.exceptions import ValidationError


def not_true(value):
    if value:
        raise ValidationError("Данное объявление было уже опубликовано")
