"""Модуль с интерфейсом и реализацией кликера"""

from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self) -> None:
        """Инициализация кликера.

        Реализации могут принимать любые параметры, необходимые для
        расчёта дохода за клик.
        """
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Совершить клик для накапливания монет."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Количество монет за один клик."""
        raise NotImplementedError


class SimpleClicker(AbstractClicker):
    """Простая реализация кликера с фиксированным доходом за клик."""

    def __init__(self, income_per_click: int = 5) -> None:
        """Создать кликер.

        :param income_per_click: Доход за один клик (целое число >= 0)
        """
        if income_per_click < 0:
            raise ValueError("income_per_click must be >= 0")
        self._income_per_click = int(income_per_click)
        self._clicks = 0

    @property
    def income_per_click(self) -> int:
        """Возвращает доход за один клик."""
        return self._income_per_click

    def click(self) -> None:
        """Зарегистрировать клик (увеличивает внутренний счётчик кликов)."""
        self._clicks += 1

    @property
    def clicks(self) -> int:
        """Количество совершённых кликов (внутренний счётчик)."""
        return self._clicks
