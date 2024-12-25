import enum


class ProductType(enum.StrEnum):
    DLC = enum.auto()  # "Дополнения (DLC)"
    GAME = enum.auto()  # "Игры (Games)"
    GAME_ITEMS = enum.auto()  # "Игровые вещи (Game Items)"
    GIFT_CARDS = enum.auto()  # "Подарочные карты (Gift Cards)"
    OTHERS = enum.auto()  # "Другое (Others)"
    PRE_ORDERS = enum.auto()  # "Предзаказы (Pre-Orders)"
    SOFTWARE = enum.auto()  # "Программное обеспечение (Software)"
    SUBSCRIPTIONS = enum.auto()  # "Подписки (Subscriptions/Subs)"
    TOP_UP = enum.auto()  # "Прямое пополнение (Top-Up)"
