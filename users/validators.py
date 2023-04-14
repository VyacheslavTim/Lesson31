import datetime

from dateutil.relativedelta import relativedelta
from rest_framework.exceptions import ValidationError


def check_birth_date(birth_date):
    year_diff = relativedelta(datetime.date.today(), birth_date).years
    if year_diff < 18:
        raise ValidationError(f"У пользователя возраст {year_diff} лет! Разрешено только с 18-ти")


def check_email(email):
    if "rambler.ru" in email.split("@")[-1]:
        raise ValidationError(f"Регистрация с домена rambler.ru запрещена")
