"""Точка входа для консольного запуска игры.

Скрипт запускает интерактивный цикл: работа, покупки, кормление,
лечение, игры и отдых с питомцем.
"""
import os

from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi
from game.clicker import SimpleClicker
from game.game import SimpleGame
from game.exceptions import TamagochiIsGone
from game.constants import STATUS_TEMPLATE, MENU_TEXT


def main():
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15)
    ]

    all_medicine = [
        Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2)
    ]

    # Создаём экземпляры наших реализаций
    tamagochi = SimpleTamagochi()
    clicker = SimpleClicker(10)
    game = SimpleGame(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine
    )

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ''

    while True:
        # Подготовим все строки и выведем одним принтом
        lines: list[str] = []
        if output:
            lines.append(output)
        lines.append(f"Сумка с едой: {game.food}")
        lines.append(f"Сумка с лекарствами: {game.medicine}")
        lines.append(STATUS_TEMPLATE.format(**game.get_status()))
        if game.tamagochi.is_sick():
            lines.append("=======Тамагочи болеет======")
            lines.append("=======Отдых действует менее эффективно=======")
        lines.append(MENU_TEXT)
        print("\n".join(lines))

        try:
            choice = input("Выберите действие: ")
            match choice:
                case "1":
                    income = game.work()
                    output = f"Вы заработали {income} монет"
                    game.tamagochi.update()
                case "2":
                    game.buy_food()
                case "3":
                    game.buy_medicine()
                case "4":
                    game.feed_tamagochi()
                case "5":
                    game.heal_tamagochi()
                case "6":
                    game.play_with_tamagochi()
                    output = "Вы поиграли с питомцем"
                case "7":
                    game.rest_tamagochi()
                    output = "Питомец отдохнул"
                case "0":
                    break
                case _:
                    output = "Неверная команда"
        except TamagochiIsGone as e:
            print(f"Игра окончена: {e}")
            break

        os.system('clear')


if __name__ == "__main__":
    main()
