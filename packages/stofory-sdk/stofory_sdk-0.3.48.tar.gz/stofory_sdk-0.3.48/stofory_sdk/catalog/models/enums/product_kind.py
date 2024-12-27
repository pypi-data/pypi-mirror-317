import enum


class ProductKind(enum.StrEnum):
    ACCOUNT = enum.auto()  # "Аккаунты (Accounts)"
    KEY = enum.auto()  # "Ключи (Keys)"
    OTHER = enum.auto()  # "Другое (Others)"
    SERVICE = enum.auto()  # "Услуги (Services)"
