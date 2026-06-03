"""
# Поиск слов из словаря по заданным буквам

Программа загружает словарь русских существительных и позволяет быстро находить все слова,
которые можно составить из букв заданного пользователем слова.

## Особенности:
- Предварительная обработка словаря (инициализация) — до 1 минуты.
- Поиск по заданному слову — менее 2 секунд.
- Сортировка результатов по убыванию длины слова.
- Поддержка кодировки UTF-8.

## Алгоритм

1. **Инициализация** (выполняется один раз при запуске):
   - Загружаем словарь из файла `nouns.txt`.
   - Для каждого слова в словаре создаём его "сигнатуру" — кортеж из отсортированных букв.
   - Группируем слова по сигнатурам в словарь `index`.

2. **Поиск** (выполняется для каждого запроса):
   - Вычисляем сигнатуру запроса (отсортированные буквы).
   - Находим в индексе все слова с такой же сигнатурой.
   - Сортируем по убыванию длины.
"""
#Код программы

import sys
import time
from collections import defaultdict


def load_dictionary(filepath):
    """
    Загружает словарь из файла в кодировке UTF-8.
    Возвращает список слов.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            words = [line.strip().lower() for line in f if line.strip()]
        return words
    except FileNotFoundError:
        print(f"Ошибка: файл {filepath} не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)


def build_index(words):
    """
    Строит индекс: для каждой сигнатуры (отсортированные буквы)
    хранит список слов, которые можно из них составить.
    """
    index = defaultdict(list)
    for word in words:
        signature = tuple(sorted(word))
        index[signature].append(word)
    return index


def find_words_by_letters(letters, index):
    """
    Находит все слова из индекса, которые можно составить из заданных букв.
    Возвращает список слов, отсортированный по убыванию длины.
    """
    signature = tuple(sorted(letters.lower()))
    return sorted(index.get(signature, []), key=lambda w: (-len(w), w))


def main():
    dictionary_file = "nouns.txt"

    print("Загрузка словаря...")
    start_time = time.time()

    # Загружаем словарь
    all_words = load_dictionary(dictionary_file)
    print(f"Загружено слов: {len(all_words)}")

    # Строим индекс для быстрого поиска
    index = build_index(all_words)

    load_time = time.time() - start_time
    print(f"Инициализация завершена за {load_time:.2f} секунд.")
    print("Можно выполнять поиск.\n")

    while True:
        # Запрос слова у пользователя
        user_word = input("Введите слово (или 'exit' для выхода): ").strip()
        if user_word.lower() == 'exit':
            break

        if not user_word:
            print("Пожалуйста, введите слово.\n")
            continue

        # Замер времени поиска
        search_start = time.time()
        results = find_words_by_letters(user_word, index)
        search_time = time.time() - search_start

        print(f"\nСлова, которые можно составить из букв слова '{user_word}':")
        if results:
            for word in results:
                print(f"  {word} (длина: {len(word)})")
            print(f"Всего найдено: {len(results)} слов.")
        else:
            print("Слова не найдены.")

        print(f"Время поиска: {search_time:.4f} секунд.\n")


if __name__ == "__main__":
    main()