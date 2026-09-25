"""Константы игрового баланса и начальных параметров.

Все магические числа вынесены сюда для удобной настройки баланса игры
и избежания дублирования значений в коде.
"""
# --- Кликер ---
DEFAULT_INCOME_PER_CLICK: int = 5

# --- Общие границы характеристик ---
STAT_MIN: int = 0
STAT_MAX: int = 100

# --- Начальные параметры тамагочи ---
INITIAL_HP: int = 100
INITIAL_ENERGY: int = 100
INITIAL_HUNGER: int = 0

# --- Пороги для определения болезни ---
HP_SICK_THRESHOLD: int = 50  # ниже этого HP питомец считается больным
HUNGER_SICK_THRESHOLD: int = 80  # при таком голоде питомец считается больным

# --- Изменения при действии play() ---
PLAY_HUNGER_DELTA: int = 7
PLAY_ENERGY_DELTA: int = 8
LOW_ENERGY_THRESHOLD: int = 20
PLAY_HP_DAMAGE_LOW_ENERGY: int = 3
PLAY_HP_DAMAGE_NORMAL: int = 1

# --- Изменения при действии rest() ---
REST_GAIN: int = 15
REST_GAIN_SICK: int = 8

# --- Естественное изменение при update() ---
UPDATE_HUNGER_DELTA: int = 2
UPDATE_ENERGY_DELTA: int = 1

# --- Пороги и урон от голода/усталости в update() ---
HUNGER_HEAVY_THRESHOLD: int = 70
HEAVY_HUNGER_DAMAGE: int = 2
ZERO_ENERGY_DAMAGE: int = 1
MODERATE_HUNGER_THRESHOLD: int = 30
MODERATE_HUNGER_DAMAGE: int = 1

# --- Игра ---
INITIAL_COINS: int = 0

# --- UI (консоль) ---
STATUS_TEMPLATE: str = (
    "\nСтатус: голод {hunger}, здоровье {hp}, "
    "энергия {energy}, монет {coins}\n"
)
MENU_TEXT: str = "\n".join(
    [
        "1. Пойти на работу",
        "2. Купить еду",
        "3. Купить лекарство",
        "4. Покормить",
        "5. Вылечить",
        "6. Играть",
        "7. Отдых",
        "0. Выход",
    ]
)
