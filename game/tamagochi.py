"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from .models import Food, Medicine
from .exceptions import TamagochiIsGone


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True, если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи
        """
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Простая реализация тамагочи со следующими параметрами:

    - hp (здоровье): 0..100
    - energy (энергия): 0..100
    - hunger (голод): 0..100 (чем больше — тем голоднее)

    Правила:
    - `play()` повышает голод, понижает энергию, может немного снижать hp,
      особенно при низкой энергии.
    - `rest()` увеличивает энергию.
    - `feed(food)` снижает голод на `food.satiety` (не ниже 0).
    - `heal(medicine)` увеличивает hp на `medicine.heal_hp` (не выше 100).
    - `update()` со временем повышает голод, немного снижает энергию и
      наносит урон hp при сильном голоде/истощении. При hp <= 0 — конец игры.
    """

    def __init__(self) -> None:
        self._hp = 100
        self._energy = 100
        self._hunger = 0
        self._alive = True
        self._sick = False

    # ---------- Вспомогательные методы ----------
    @staticmethod
    def _clamp(value: int, lo: int = 0, hi: int = 100) -> int:
        return max(lo, min(hi, int(value)))

    def _recalc_sick(self) -> None:
        # Простое правило болезни: при сильном голоде или низком hp
        self._sick = self._hp < 50 or self._hunger > 80

    # ---------- Реализация интерфейса ----------
    def feed(self, food: Food) -> None:
        """Накормить питомца, уменьшая голод.

        :param food: Объект еды
        """
        if not self._alive:
            return
        self._hunger = self._clamp(self._hunger - food.satiety)
        # Лёгкая усталость от еды не моделируем — достаточно уменьшения голода
        self._recalc_sick()

    def play(self) -> None:
        """Поиграть: повышает голод, снижает энергию, может снизить hp."""
        if not self._alive:
            return
        self._hunger = self._clamp(self._hunger + 7)
        self._energy = self._clamp(self._energy - 8)
        if self._energy < 20:
            self._hp = self._clamp(self._hp - 3)
        else:
            self._hp = self._clamp(self._hp - 1)
        if self._hp <= 0:
            self._alive = False
        self._recalc_sick()

    def rest(self) -> None:
        """Отдых: увеличивает энергию (менее эффективно при болезни)."""
        if not self._alive:
            return
        gain = 15
        if self.is_sick():
            gain = 8
        self._energy = self._clamp(self._energy + gain)
        self._recalc_sick()

    def heal(self, medicine: Medicine) -> None:
        """Лечение: увеличивает hp.

        Использования лекарства (uses) не изменяются здесь —
        этим может управлять логика игры.
        """
        if not self._alive:
            return
        self._hp = self._clamp(self._hp + medicine.heal_hp)
        self._recalc_sick()

    @property
    def status(self) -> dict[str, int]:
        """Текущий статус питомца: hunger, hp, energy (все int)."""
        return {
            "hunger": int(self._hunger),
            "hp": int(self._hp),
            "energy": int(self._energy),
        }

    def is_alive(self) -> bool:
        """Жив ли питомец."""
        return self._alive and self._hp > 0

    def is_sick(self) -> bool:
        """Болен ли питомец (простая эвристика по hp/голоду)."""
        return bool(self._sick)

    def update(self) -> None:
        """Обновить состояние.

        Время идёт — голод растёт, энергия падает, hp страдает.
        При достижении hp <= 0 питомец умирает: устанавливается
        `_alive = False` и выбрасывается исключение `TamagochiIsGone`.
        """
        if not self._alive:
            raise TamagochiIsGone("Питомец уже умер")

        # Естественная динамика
        self._hunger = self._clamp(self._hunger + 2)
        self._energy = self._clamp(self._energy - 1)

        # Урон от сильного голода или полной усталости
        damage = 0
        if self._hunger >= 70:
            damage += 2
        if self._energy == 0:
            damage += 1
        if damage == 0 and self._hunger >= 30:
            damage = 1  # понемногу слабеет при умеренном голоде

        self._hp = self._clamp(self._hp - damage)
        if self._hp <= 0:
            self._alive = False
            raise TamagochiIsGone("Питомец погиб")

        self._recalc_sick()
