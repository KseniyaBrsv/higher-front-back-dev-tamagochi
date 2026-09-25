"""Модуль с интерфейсом и реализацией класса игры.

Определяет абстрактный класс `AbstractGame` и реализацию `SimpleGame`.
"""

from abc import ABC, abstractmethod
from typing import Any
from dataclasses import replace

from .tamagochi import AbstractTamagochi
from .clicker import AbstractClicker
from .models import Food, Medicine
from . import constants


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

    @abstractmethod
    def __init__(
        self,
        _tamagochi: AbstractTamagochi,
        _clicker: AbstractClicker,
        _all_food: list[Food],
        _all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры.

        :param _tamagochi: Экземпляр тамагочи
        :param _clicker: экземпляр кликера
        :param _all_food: все доступные варианты еды
        :param _all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа".

        :return: Количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи.

        :return: Словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой.

        :return: Список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами.

        :return: Список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Простая реализация игры.

    Управляет монетами, инвентарём еды и лекарств и делегирует действия
    питомцу. Покупки осуществляются через консольный ввод.
    """

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ) -> None:
        """Инициализировать игру.

        Сохраняет переданные зависимости (тамагочи, кликер) и списки
        доступной еды и лекарств. Создаёт пустой инвентарь и обнуляет монеты.
        """
        self.tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = list(all_food)
        self._all_medicine = list(all_medicine)
        self._bag_food: list[Food] = []
        self._bag_medicine: list[Medicine] = []
        self._coins = constants.INITIAL_COINS

    # ---------- Вспомогательные методы ----------
    @staticmethod
    def _input(prompt: str) -> str:
        return input(prompt)

    def _choose_from(self, items: list[Any], title: str) -> int:
        if not items:
            print("Нечего выбирать.")
            return 0
        print(title)
        for i, item in enumerate(items, start=1):
            print(f"{i}. {item}")
        print("0. Выход")
        # Читаем ввод пользователи и обрабатываем ожидаемые ошибки точечно
        try:
            raw = self._input("Выберите пункт: ")
        except (EOFError, KeyboardInterrupt):
            return 0
        try:
            return int(raw)
        except (ValueError, TypeError):
            return 0

    # ---------- Реализация интерфейса ----------
    def work(self) -> int:
        """Сходить на работу: вызывает кликер и добавляет монеты."""
        self._clicker.click()
        inc = int(self._clicker.income_per_click)
        self._coins += inc
        return inc

    def buy_food(self) -> None:
        """Покупка еды: позволяет выбрать позиции и добавить их в инвентарь."""
        while True:
            idx = self._choose_from(self._all_food, "Доступная еда:")
            if idx <= 0:
                break
            if 1 <= idx <= len(self._all_food):
                item = self._all_food[idx - 1]
                if item.price > self._coins:
                    # Для простоты не выбрасываем исключение в интерактиве
                    print("Недостаточно монет для покупки еды.")
                    continue
                self._coins -= item.price
                self._bag_food.append(item)
                print(f"Куплено: {item.name}")

    def buy_medicine(self) -> None:
        """Покупка лекарств: аналогично покупке еды."""
        while True:
            idx = self._choose_from(self._all_medicine, "Доступные лекарства:")
            if idx <= 0:
                break
            if 1 <= idx <= len(self._all_medicine):
                item = self._all_medicine[idx - 1]
                if item.price > self._coins:
                    print("Недостаточно монет для покупки лекарства.")
                    continue
                self._coins -= item.price
                # Создаём копию (uses=0) через dataclasses.replace,
                # чтобы не делить один объект между покупками.
                med = replace(item, uses=0)
                self._bag_medicine.append(med)
                print(f"Куплено: {item.name}")

    def feed_tamagochi(self) -> None:
        """Покормить питомца выбранной из инвентаря едой.

        Единица выбранной еды расходуется.
        """
        if not self._bag_food:
            print("Еды нет.")
            return
        idx = self._choose_from(self._bag_food, "Инвентарь: еда")
        if 1 <= idx <= len(self._bag_food):
            food = self._bag_food.pop(idx - 1)
            self.tamagochi.feed(food)

    def heal_tamagochi(self) -> None:
        """Вылечить питомца выбранным лекарством.

        Использование выбранного лекарства расходуется.
        """
        if not self._bag_medicine:
            print("Лекарств нет.")
            return
        idx = self._choose_from(self._bag_medicine, "Инвентарь: лекарства")
        if 1 <= idx <= len(self._bag_medicine):
            med = self._bag_medicine[idx - 1]
            if med.is_empty():
                print("Лекарство закончилось.")
                # удалить пустое
                self._bag_medicine.pop(idx - 1)
                return
            self.tamagochi.heal(med)
            med.uses += 1
            if med.is_empty():
                self._bag_medicine.pop(idx - 1)

    def rest_tamagochi(self) -> None:
        """Отдых питомца."""
        self.tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        """Игра с питомцем."""
        self.tamagochi.play()

    def get_status(self) -> dict[str, Any]:
        """Статус игры: показатели питомца + монеты."""
        s = dict(self.tamagochi.status)
        s["coins"] = int(self._coins)
        return s

    @property
    def food(self) -> list[Food]:
        """Сумка с едой (инвентарь)."""
        return self._bag_food

    @property
    def medicine(self) -> list[Medicine]:
        """Сумка с лекарствами (инвентарь)."""
        return self._bag_medicine
