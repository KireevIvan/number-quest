import random
import time
from datetime import datetime

def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Пожалуйста, введите целое число.")


def get_yes_no(prompt):
    while True:
        response = input(prompt).lower()
        if response in ("да", "нет"):
            return response
        print("Введите да или нет.")


def generate_random_number(low, high):
    return random.randint(low, high)


def calculate_score(attempts, duration, max_attempts):
    score = 0

    score += max(0, 50 - attempts * 5)
    if duration < 10:
        score *= 2
    return score


def save_result(date_str, secret_number, attempts_used, duration, total_score):

    with open("history.txt", "a", encoding="utf-8") as file:
        line = f"{date_str} | {secret_number} | {attempts_used} | {duration:.2f} | {total_score}\n"
        file.write(line)


def randoming():
    start_points = 15
    hint_mode = get_yes_no("Включить режим подсказок? да/нет\n")
    interval1 = get_int_input("Введите минимальное число в интервале:\n")
    interval2 = get_int_input("Введите максимальное число в интервале:\n")
    max_attempts = get_int_input("Введите количество попыток:\n")

    points = start_points

    game_number = 0
    total_attempts = 0
    total_time_spent = 0

    while True:
        game_number += 1
        secret_number = generate_random_number(interval1, interval2)
        attempts = 0

        start_time = time.time()

        while attempts < max_attempts:
            attempt_start_time = time.time()
            user_input = input("Попытайтесь угадать число:\n")
            if not user_input.isdigit():
                print("Это не число")
                continue
            guess = int(user_input)
            attempts += 1
            total_attempts += 1

            if guess == secret_number:
                end_time = time.time()
                duration = end_time - start_time
                total_time_spent += duration

                print(f"Вы угадали! Загаданное число: {secret_number}")
                print(f"Затраченное время: {duration} секунд")

                score = calculate_score(attempts, duration, max_attempts)
                points += score
                print(f"Вы заработали {score} очков")
                print(f"Общий балл: {points}")

                date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_result(date_str, secret_number, attempts, duration, score)

                restart = get_yes_no("Начать новую игру? да/нет\n")
                if restart == "да":
                    break
                else:
                    print(f"Игра завершена. Итог: {points} очков сыграно игр: {game_number}")
                    return
            else:
                print("вы не угадали")
                points -= 5
                if points < 0:
                    points = 0
                if hint_mode == "да":
                    if secret_number > guess:
                        print("Это число больше")
                    else:
                        print("Это число меньше")
                print(f"Осталось попыток: {max_attempts - attempts}")
                print(f"Ваш текущий баланс: {points} очков")
                if attempts >= max_attempts:
                    end_time = time.time()
                    duration = end_time - start_time
                    total_time_spent += duration
                    print(f"Игра окончена загаданное число было: {secret_number}")
                    print(f"Затраченное время: {duration:.2f} секунд")

                    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_result(date_str, secret_number, attempts, duration, 0)

        continue_game = get_yes_no("Хотите сыграть еще раз? да/нет\n")
        if continue_game != "да":
            print(f"Игра завершена. Итог: {points} очков, всего игр: {game_number}")
            print(f"Общее время всех игр: {total_time_spent} секунд")
            break



randoming()
