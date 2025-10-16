import re
import random
from datetime import datetime


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


def select_random_questions(
    topics, simple_count=2, medium_count=2, hard_count=2, extra_count=3
):
    """Выбирает случайные вопросы из всех тем"""
    selected = {"Простые": [], "Средние": [], "Сложные": [], "Дополнительные": []}

    # Собираем все вопросы каждого уровня из всех тем
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

    # Выбираем случайные основные вопросы
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

    # Для дополнительных вопросов исключаем уже выбранные
    all_questions = all_simple + all_medium + all_hard
    selected_questions = selected["Простые"] + selected["Средние"] + selected["Сложные"]

    # Оставляем только вопросы, которые не были выбраны в основные
    remaining_questions = [q for q in all_questions if q not in selected_questions]

    # Выбираем дополнительные вопросы
    if remaining_questions and extra_count > 0:
        selected["Дополнительные"] = random.sample(
            remaining_questions, min(extra_count, len(remaining_questions))
        )

    return selected


def convert_markdown_to_html(text):
    """Конвертирует Markdown в HTML"""
    # Обрабатываем блоки details
    text = re.sub(
        r"<details>\s*<summary>(.*?)</summary>\s*(.*?)\s*</details>",
        r'<details><summary>\1</summary><div class="answer">\2</div></details>',
        text,
        flags=re.DOTALL,
    )

    # Обрабатываем код с нумерацией строк
    text = re.sub(
        r"```python\s*(.*?)\s*```",
        lambda match: format_code_with_line_numbers(match.group(1)),
        text,
        flags=re.DOTALL,
    )

    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)

    text = text.replace("\n", "<br>")

    return text


def format_code_with_line_numbers(code):
    """Форматирует код Python с нумерацией строк"""
    lines = code.strip().split("\n")
    numbered_lines = []

    for i, line in enumerate(lines, 1):
        numbered_lines.append(
            f'<div class="code-line"><span class="line-number">{i}</span><span class="line-content">{line}</span></div>'
        )

    return f'<div class="code-block"><div class="code-lines">{chr(10).join(numbered_lines)}</div></div>'


def generate_html(selected_questions, output_filename):
    """Создает HTML-файл с вопросами, таблицей и таймером"""

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Вопросы для экзамена</title>
        
        <!-- Подключение Highlight.js для подсветки кода -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
        <script>hljs.highlightAll();</script>
        
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                line-height: 1.6;
            }}
            .timer {{
                position: fixed;
                top: 20px;
                right: 20px;
                background: #f0f0f0;
                padding: 20px 25px;
                border-radius: 10px;
                font-size: 48px;
                font-weight: bold;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                z-index: 1000;
                min-width: 150px;
                text-align: center;
            }}
            .timer.urgent {{
                background: #ffcccc;
                color: #cc0000;
                animation: pulse 1s infinite;
            }}
            @keyframes pulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
                100% {{ transform: scale(1); }}
            }}
            button {{
                background: #4CAF50;
                color: white;
                border: none;
                padding: 15px 25px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 18px;
                margin: 10px 5px;
                transition: background 0.3s;
            }}
            button:hover {{
                background: #45a049;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }}
            .question-container {{
                margin: 20px 0;
                padding: 20px;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background: #fafafa;
            }}
            details {{
                margin: 15px 0;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 15px;
                background: white;
            }}
            summary {{
                cursor: pointer;
                font-weight: bold;
                font-size: 18px;
                padding: 10px;
                background: #f5f5f5;
                border-radius: 4px;
                margin: -15px;
                padding: 15px;
            }}
            .answer {{
                margin-top: 15px;
                padding: 15px;
                background: #f9f9f9;
                border-radius: 6px;
                border-left: 4px solid #4CAF50;
            }}
            .code-block {{
                background: #2d2d2d;
                border-radius: 6px;
                overflow: hidden;
                margin: 15px 0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .code-lines {{
                font-family: 'Courier New', monospace;
                color: #f8f8f2;
                padding: 15px 0;
                overflow-x: auto;
            }}
            .code-line {{
                display: flex;
                padding: 2px 15px;
            }}
            .line-number {{
                color: #6c6c6c;
                min-width: 40px;
                text-align: right;
                padding-right: 15px;
                user-select: none;
                border-right: 1px solid #444;
                margin-right: 15px;
            }}
            .line-content {{
                flex: 1;
                white-space: pre;
            }}
            .topic {{
                font-style: italic;
                color: #666;
                margin-bottom: 10px;
                font-size: 16px;
                padding: 5px 10px;
                background: #e9e9e9;
                border-radius: 4px;
                display: inline-block;
            }}
            .section {{
                margin-bottom: 40px;
                padding: 20px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .controls {{
                margin: 30px 0;
                text-align: center;
                padding: 20px;
                background: #f8f8f8;
                border-radius: 8px;
            }}
            .score-section {{
                margin: 20px 0;
                padding: 15px;
                background: #e8f4fd;
                border-radius: 8px;
                border-left: 4px solid #2196F3;
            }}
            .score-input {{
                margin: 10px 0;
                display: flex;
                align-items: center;
            }}
            .score-input label {{
                margin-right: 10px;
                font-weight: bold;
                min-width: 150px;
            }}
            .score-input input {{
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                width: 80px;
            }}
            .total-score {{
                font-size: 24px;
                font-weight: bold;
                text-align: center;
                margin: 20px 0;
                padding: 15px;
                background: #e8f5e9;
                border-radius: 8px;
                border: 2px solid #4CAF50;
            }}
            .formula-info {{
                text-align: center;
                margin: 10px 0;
                color: #666;
                font-style: italic;
            }}
            h1 {{
                color: #2c3e50;
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #eee;
                padding-bottom: 15px;
            }}
            h2 {{
                color: #34495e;
                border-left: 4px solid #3498db;
                padding-left: 15px;
            }}
        </style>
    </head>
    <body>
        <h1>Вопросы для экзамена</h1>
        <p style="text-align: center; color: #666;">Дата: {datetime.now().strftime("%d.%m.%Y %H:%M")}</p>
        
        <div class="controls">
            <button onclick="startTimer()">Запустить таймер (10 минут)</button>
            <button onclick="resetTimer()">Сбросить таймер</button>
        </div>
        
        <div id="timer" class="timer">10:00</div>
    """

    # Основные вопросы
    html_content += '<div class="section"><h2>Основные вопросы</h2>'

    question_num = 1
    weights = {"Простые": 0.5, "Средние": 1, "Сложные": 2}

    for level in ["Простые", "Средние", "Сложные"]:
        for topic_name, question in selected_questions[level]:
            html_question = convert_markdown_to_html(question)
            weight = weights[level]
            html_content += f"""
            <div class="question-container">
                <div class="topic">Вопрос {question_num} | Тема: {topic_name} | Уровень: {level} | Вес: {weight}</div>
                {html_question}
                <div class="score-section">
                    <div class="score-input">
                        <label>Оценка (0-10):</label>
                        <input type="number" min="0" max="10" step="0.1" id="score_{question_num}" data-weight="{weight}" onchange="calculateTotal()">
                    </div>
                </div>
            </div>
            """
            question_num += 1

    html_content += "</div>"

    # Дополнительные вопросы
    if selected_questions["Дополнительные"]:
        html_content += '<div class="section"><h2>Дополнительные вопросы</h2>'

        for i, (topic_name, question) in enumerate(
            selected_questions["Дополнительные"], 1
        ):
            html_question = convert_markdown_to_html(question)
            weight = 1  # Вес дополнительных вопросов
            html_content += f"""
            <div class="question-container">
                <div class="topic">Дополнительный вопрос {i} | Тема: {topic_name} | Вес: {weight}</div>
                {html_question}
                <div class="score-section">
                    <div class="score-input">
                        <label>Оценка (0-10):</label>
                        <input type="number" min="0" max="10" step="0.1" id="score_extra_{i}" data-weight="{weight}" onchange="calculateTotal()">
                    </div>
                </div>
            </div>
            """

    html_content += "</div>"

    # Секция с итоговой оценкой
    html_content += """
        <div class="formula-info">
            Формула расчета: (Простые × 0.5) + (Средние × 1) + (Сложные × 2) + (Дополнительные × 1)
        </div>
        <div class="total-score">
            Итоговая оценка: <span id="total-score">0</span> / 10
        </div>
    """

    # Закрываем body и добавляем JavaScript
    html_content += """
        <script>
            let timerInterval;
            let timeLeft = 600; // 10 минут в секундах
            
            function updateTimer() {
                const minutes = Math.floor(timeLeft / 60);
                const seconds = timeLeft % 60;
                document.getElementById('timer').textContent = 
                    `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                
                if (timeLeft <= 60) {
                    document.getElementById('timer').classList.add('urgent');
                }
                
                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    alert('Время вышло!');
                } else {
                    timeLeft--;
                }
            }
            
            function startTimer() {
                if (timerInterval) {
                    clearInterval(timerInterval);
                }
                timeLeft = 600;
                updateTimer();
                timerInterval = setInterval(updateTimer, 1000);
            }
            
            function resetTimer() {
                if (timerInterval) {
                    clearInterval(timerInterval);
                }
                timeLeft = 600;
                document.getElementById('timer').textContent = '10:00';
                document.getElementById('timer').classList.remove('urgent');
            }
            
            function calculateTotal() {
                let total = 0;
                let maxPossible = 0;
                
                // Основные вопросы
                const basicQuestions = document.querySelectorAll('input[id^="score_"]:not([id^="score_extra_"])');
                basicQuestions.forEach(input => {
                    const score = parseFloat(input.value) || 0;
                    const weight = parseFloat(input.dataset.weight);
                    total += score * weight / 10; // Делим на 10, так как оценка вводится по 10-балльной шкале
                    maxPossible += 10 * weight / 10; // Максимальная оценка для этого вопроса
                });
                
                // Дополнительные вопросы
                const extraQuestions = document.querySelectorAll('input[id^="score_extra_"]');
                extraQuestions.forEach(input => {
                    const score = parseFloat(input.value) || 0;
                    const weight = parseFloat(input.dataset.weight);
                    total += score * weight / 10; // Делим на 10, так как оценка вводится по 10-балльной шкале
                    maxPossible += 10 * weight / 10; // Максимальная оценка для этого вопроса
                });
                
                // Ограничиваем максимальную оценку 10
                total = Math.min(total, 10);
                
                document.getElementById('total-score').textContent = total.toFixed(2);
            }

            // Автоматически закрывать все ответы при загрузке
            document.querySelectorAll('details').forEach(detail => {
                detail.open = false;
            });
        </script>
    </body>
    </html>
    """

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_content)


def main():
    try:
        # Парсим README.md
        print("Парсим README.md...")
        topics = parse_readme("README.md")

        # Проверяем, что нашли вопросы
        total_questions = 0
        for topic_name, levels in topics.items():
            for level, questions in levels.items():
                total_questions += len(questions)
                print(f"{topic_name} - {level}: {len(questions)} вопросов")

        if total_questions == 0:
            print("Не найдено ни одного вопроса в README.md!")
            return

        # Выбираем случайные вопросы
        print("Выбираем случайные вопросы...")
        selected = select_random_questions(
            topics, simple_count=2, medium_count=2, hard_count=2, extra_count=3
        )

        # Создаем HTML-файл
        output_file = "exam_questions.html"
        generate_html(selected, output_file)

    except FileNotFoundError:
        print("Ошибка: Файл README.md не найден!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
