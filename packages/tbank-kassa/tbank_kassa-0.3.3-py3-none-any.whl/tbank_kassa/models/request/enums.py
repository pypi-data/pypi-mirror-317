from enum import StrEnum


class PaymentType(StrEnum):
    ONE_STAGE = 'O'
    TWO_STAGE = 'T'


class Language(StrEnum):
    RUS = 'ru'
    ENG = 'en'
