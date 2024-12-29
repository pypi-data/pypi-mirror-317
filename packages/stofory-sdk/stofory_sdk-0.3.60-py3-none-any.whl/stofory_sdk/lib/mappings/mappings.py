import enum
from typing import Dict, List, TypeVar, Generic, get_origin, get_args, Type

from stofory_sdk.catalog.models.enums import Locale as AdminLocale, Currency as AdminCurrency, \
    ParameterType as AdminParameterType, ModifierOperator as AdminModifierOperator

from stofory_sdk.digiseller.schemas import Locale as DigisellerLocale, Currency as DigisellerCurrency, \
    OptionTypes as DigisellerOptionTypes, VariantTypes as DigisellerVariantTypes

__all__ = [
    "LocaleMapper",
    "ReversedLocaleMapper",
    "CurrencyMapper",
    "ParameterTypeMapper",
    "ModifierOperatorMapper",
    "ReversedCurrencyMapper",
    "ReversedParameterTypeMapper",
]

T = TypeVar('T')
U = TypeVar('U')


class EnumMapper(Generic[T, U]):
    model: str
    mapping: Dict[T, U]
    key_type: Type[T]
    value_type: Type[U]

    def __init__(self, mapping: Dict[T, U]):
        if not isinstance(mapping, dict):
            raise ValueError("Mapping must be a dictionary")

        self.key_type, self.value_type = get_args(self.__orig_bases__[0])
        # print(self.key_type, self.value_type)
        # print(type(self.key_type), type(self.value_type))

        if not all(isinstance(k, self.key_type) for k in mapping.keys()):
            raise ValueError(f"Keys must be of type {self.key_type.__class__}")

        if not all(isinstance(v, self.value_type) for v in mapping.values()):
            raise ValueError(f"Values must be of type {self.value_type}")

        self.mapping = mapping

    def add(self, key: T, value: U) -> bool:
        if not isinstance(key, self.key_type):
            raise ValueError(f"Key must be of type {self.key_type}")

        if not isinstance(value, self.value_type):
            raise ValueError(f"Value must be of type {self.value_type}")

        self.mapping[key] = value
        return True

    def get(self, key: T) -> U:
        if not isinstance(key, self.key_type):
            raise ValueError(f"Key must be of type {self.key_type}")

        if key not in self.mapping:
            raise KeyError(f"Key {key} not found in {self.model}`s mapping")

        return self.mapping[key]


class LocaleMapper(EnumMapper[AdminLocale, DigisellerLocale]):
    model = "Locale"

    def __init__(self):
        super().__init__({
            AdminLocale.RU_RU: DigisellerLocale.RU_RU,
            AdminLocale.EN_EN: DigisellerLocale.EN_US,
        })


class ReversedLocaleMapper(EnumMapper[DigisellerLocale, AdminLocale]):
    model = "Locale"

    def __init__(self):
        super().__init__({
            DigisellerLocale.RU_RU: AdminLocale.RU_RU,
            DigisellerLocale.EN_US: AdminLocale.EN_EN,
            DigisellerLocale.EN_EN: AdminLocale.EN_EN,
        })


class CurrencyMapper(EnumMapper[AdminCurrency, DigisellerCurrency]):
    model = "Currency"

    def __init__(self):
        super().__init__({
            AdminCurrency.RUB: DigisellerCurrency.RUB,
            # AdminCurrency.KZT: DigisellerCurrency.KZT,
            AdminCurrency.USD: DigisellerCurrency.USD,
        })


class ReversedCurrencyMapper(EnumMapper[DigisellerCurrency, AdminCurrency]):
    model = "Currency"

    def __init__(self):
        super().__init__({
            DigisellerCurrency.RUB: AdminCurrency.RUB,
            DigisellerCurrency.USD: AdminCurrency.USD,
        })


class ParameterTypeMapper(EnumMapper[AdminParameterType, DigisellerOptionTypes]):
    model = "ParameterType"

    def __init__(self):
        super().__init__({
            AdminParameterType.TEXT: DigisellerOptionTypes.TEXT,
            AdminParameterType.RADIO: DigisellerOptionTypes.RADIO,
            AdminParameterType.CHECKBOX: DigisellerOptionTypes.CHECKBOX,
        })


class ReversedParameterTypeMapper(EnumMapper[DigisellerOptionTypes, AdminParameterType]):
    model = "ParameterType"

    def __init__(self):
        super().__init__({
            DigisellerOptionTypes.TEXT: AdminParameterType.TEXT,
            DigisellerOptionTypes.RADIO: AdminParameterType.RADIO,
            DigisellerOptionTypes.CHECKBOX: AdminParameterType.CHECKBOX,
        })


class ModifierOperatorMapper(EnumMapper[AdminModifierOperator, DigisellerVariantTypes]):
    model = "ModifierOperator"

    def __init__(self):
        super().__init__({
            AdminModifierOperator.PLUS: DigisellerVariantTypes.PRICEPLUS,
            AdminModifierOperator.MINUS: DigisellerVariantTypes.PRICEMINUS,
            AdminModifierOperator.PLUS_PERCENT: DigisellerVariantTypes.PERCENTPLUS,
            AdminModifierOperator.MINUS_PERCENT: DigisellerVariantTypes.PERCENTMINUS,
        })
