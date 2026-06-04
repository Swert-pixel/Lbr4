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

def read_dictionary(file_path):
    """Читает словарь из файла и возвращает список слов."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Читаем все строки, удаляем лишние пробелы и пустые строки
            words = [line.strip() for line in file if line.strip()]
        return words
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


def count_letters(word):
    """Подсчитывает количество каждой буквы в слове."""
    letter_count = {}
    for char in word:
        letter_count[char] = letter_count.get(char, 0) + 1
    return letter_count


def can_form_word(target_word, dict_word):
    """
    Проверяет, можно ли составить dict_word из букв target_word.
    Возвращает True, если можно, иначе False.
    """
    # Считаем буквы в исходном слове
    target_counts = count_letters(target_word)

    # Проверяем, хватает ли букв для составления слова из словаря
    for char in dict_word:
        if target_counts.get(char, 0) == 0:
            return False
        target_counts[char] -= 1

    return True


def find_matching_words(word, dictionary):
    """Находит все слова из словаря, которые можно составить из букв word."""
    result = []
    word = word.lower()  # Приводим к нижнему регистру

    for dict_word in dictionary:
        # Пропускаем слова, которые длиннее исходного
        if len(dict_word) > len(word):
            continue

        # Проверяем, можно ли составить слово
        if can_form_word(word, dict_word):
            result.append(dict_word)

    # Сортируем по убыванию длины, при одинаковой длине сохраняем порядок из словаря
    result.sort(key=lambda x: len(x), reverse=True)
    return result


def main():
    # Путь к файлу со словарем
    dictionary_file = "nouns.txt"

    print("Загрузка словаря...")
    dictionary = read_dictionary(dictionary_file)
    print(f"Словарь загружен. Всего слов: {len(dictionary)}")

    # Основной цикл обработки запросов
    while True:
        print("\n" + "=" * 50)
        word = input("Введите слово (или 'выход' для завершения): ").strip().lower()

        if word == 'выход':
            print("Программа завершена.")
            break

        if not word:
            print("Пожалуйста, введите слово.")
            continue

        # Ищем подходящие слова
        matching_words = find_matching_words(word, dictionary)

        if matching_words:
            print(f"\nНайдено слов: {len(matching_words)}")
            print("Слова в порядке уменьшения длины:")
            for w in matching_words:
                print(f"  {w} (длина: {len(w)})")
        else:
            print(f"Не найдено слов, которые можно составить из букв слова '{word}'.")


if __name__ == "__main__":
    main()
