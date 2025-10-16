import re
import random


def parse_readme(filename):
    """Парсит README.md и возвращает структурированные данные"""
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Разделяем на основные темы
    topic_pattern = r"^## (.+?)\n(.*?)(?=^## |\Z)"
    topics = {}

    for match in re.finditer(topic_pattern, content, re.MULTILINE | re.DOTALL):
        topic_name = match.group(1).strip()
        topic_content = match.group(2)

        # Извлекаем вопросы по уровням сложности
        questions = {"Простые": [], "Средние": [], "Сложные": []}

        # Ищем подразделы с уровнями сложности
        simple_match = re.search(
            r"### Простые вопросы\s*(.*?)(?=###|\n---|\Z)", topic_content, re.DOTALL
        )
        medium_match = re.search(
            r"### Средние вопросы\s*(.*?)(?=###|\n---|\Z)", topic_content, re.DOTALL
        )
        hard_match = re.search(
            r"### Сложные вопросы\s*(.*?)(?=###|\n---|\Z)", topic_content, re.DOTALL
        )

        # Парсим вопросы для каждого уровня
        if simple_match:
            questions["Простые"] = extract_questions_with_code(simple_match.group(1))
        if medium_match:
            questions["Средние"] = extract_questions_with_code(medium_match.group(1))
        if hard_match:
            questions["Сложные"] = extract_questions_with_code(hard_match.group(1))

        topics[topic_name] = questions

    return topics


def extract_questions_with_code(content):
    """Извлекает вопросы вместе с кодом Python, который следует за ними"""
    questions = []

    # Находим все блоки <details>
    details_matches = list(re.finditer(r"<details>.*?</details>", content, re.DOTALL))

    for i, match in enumerate(details_matches):
        question_block = match.group(0)

        # Проверяем, есть ли код Python после этого вопроса
        end_pos = match.end()
        next_details_start = (
            content.find("<details>", end_pos)
            if i < len(details_matches) - 1
            else len(content)
        )

        # Ищем код между текущим вопросом и следующим
        code_match = re.search(
            r"```python\s*(.*?)\s*```", content[end_pos:next_details_start], re.DOTALL
        )

        if code_match:
            # Добавляем код к вопросу
            code = code_match.group(1).strip()
            question_block += f"\n\n```python\n{code}\n```"

        questions.append(question_block)

    return questions


def select_random_questions(topics, simple_count=2, medium_count=2, hard_count=2):
    """Выбирает случайные вопросы из всех тем"""
    selected = {"Простые": [], "Средние": [], "Сложные": []}

    all_simple = []
    all_medium = []
    all_hard = []

    for topic_name, levels in topics.items():
        for question in levels["Простые"]:
            all_simple.append((topic_name, question))
        for question in levels["Средние"]:
            all_medium.append((topic_name, question))
        for question in levels["Сложные"]:
            all_hard.append((topic_name, question))

    if all_simple and simple_count > 0:
        selected["Простые"] = random.sample(
            all_simple, min(simple_count, len(all_simple))
        )

    if all_medium and medium_count > 0:
        selected["Средние"] = random.sample(
            all_medium, min(medium_count, len(all_medium))
        )

    if all_hard and hard_count > 0:
        selected["Сложные"] = random.sample(all_hard, min(hard_count, len(all_hard)))

    return selected


def create_questions_file(selected_questions, output_filename):
    """Создает итоговый .md файл с выбранными вопросами"""
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("# Случайно выбранные вопросы для подготовки\n\n")

        if selected_questions["Простые"]:
            f.write("## Простые вопросы\n\n")
            for topic_name, question in selected_questions["Простые"]:
                f.write(f"**Тема:** {topic_name}\n\n")
                f.write(question + "\n\n")

        if selected_questions["Средние"]:
            f.write("## Средние вопросы\n\n")
            for topic_name, question in selected_questions["Средние"]:
                f.write(f"**Тема:** {topic_name}\n\n")
                f.write(question + "\n\n")

        if selected_questions["Сложные"]:
            f.write("## Сложные вопросы\n\n")
            for topic_name, question in selected_questions["Сложные"]:
                f.write(f"**Тема:** {topic_name}\n\n")
                f.write(question + "\n\n")


def main():
    try:
        print("Парсим README.md...")
        topics = parse_readme("README.md")

        total_questions = 0
        for topic_name, levels in topics.items():
            for level, questions in levels.items():
                total_questions += len(questions)
                print(f"{topic_name} - {level}: {len(questions)} вопросов")

        if total_questions == 0:
            print("Не найдено ни одного вопроса в README.md!")
            return

        print("Выбираем случайные вопросы...")
        selected = select_random_questions(
            topics, simple_count=2, medium_count=2, hard_count=2
        )

        output_file = "selected_questions.md"
        create_questions_file(selected, output_file)

        total_selected = (
            len(selected["Простые"])
            + len(selected["Средние"])
            + len(selected["Сложные"])
        )

        print(f"Готово! Создан файл: {output_file}")
        print("Выбрано вопросов:")
        print(f"  - Простых: {len(selected['Простые'])}")
        print(f"  - Средних: {len(selected['Средние'])}")
        print(f"  - Сложных: {len(selected['Сложные'])}")
        print(f"  - Всего: {total_selected}")

    except FileNotFoundError:
        print("Ошибка: Файл README.md не найден!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
