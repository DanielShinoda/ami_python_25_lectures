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

    text = re.sub(
        r"```python\s*(.*?)\s*```",
        r'<pre><code class="language-python">\1</code></pre>',
        text,
        flags=re.DOTALL,
    )

    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)

    text = text.replace("\n", "<br>")

    return text


def generate_html(selected_questions, output_filename):
    """Создает HTML-файл с вопросами, таблицей и таймером"""

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Вопросы для экзамена</title>
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
                padding: 10px 15px;
                border-radius: 5px;
                font-size: 18px;
                font-weight: bold;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }}
            .timer.urgent {{
                background: #ffcccc;
                color: #cc0000;
            }}
            button {{
                background: #4CAF50;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px 0;
            }}
            button:hover {{
                background: #45a049;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            details {{
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
            }}
            summary {{
                cursor: pointer;
                font-weight: bold;
            }}
            .answer {{
                margin-top: 10px;
                padding: 10px;
                background: #f9f9f9;
                border-radius: 4px;
            }}
            pre {{
                background: #f4f4f4;
                padding: 10px;
                border-radius: 4px;
                overflow-x: auto;
            }}
            .topic {{
                font-style: italic;
                color: #666;
                margin-bottom: 5px;
            }}
            .section {{
                margin-bottom: 30px;
            }}
            input, textarea {{
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }}
            .controls {{
                margin: 20px 0;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <h1>Вопросы для собеседования</h1>
        <p>Дата: {datetime.now().strftime("%d.%m.%Y %H:%M")}</p>
        
        <div class="controls">
            <button onclick="startTimer()">Запустить таймер (10 минут)</button>
            <button onclick="resetTimer()">Сбросить таймер</button>
            <button onclick="saveResults()">Сохранить результаты</button>
        </div>
        
        <div id="timer" class="timer">10:00</div>
        
        <form id="interviewForm">
    """

    html_content += '<div class="section"><h2>Основные вопросы</h2><table>'
    html_content += (
        "<tr><th>№</th><th>Вопрос</th><th>Оценка (1-10)</th><th>Комментарий</th></tr>"
    )

    question_num = 1
    for level in ["Простые", "Средние", "Сложные"]:
        for topic_name, question in selected_questions[level]:
            html_question = convert_markdown_to_html(question)
            html_content += f"""
            <tr>
                <td>{question_num}</td>
                <td>
                    <div class="topic">Тема: {topic_name} | Уровень: {level}</div>
                    {html_question}
                </td>
                <td><input type="number" name="score_{question_num}" min="1" max="10"></td>
                <td><textarea name="comment_{question_num}" rows="3"></textarea></td>
            </tr>
            """
            question_num += 1

    html_content += "</table></div>"

    html_content += '<div class="section"><h2>Дополнительные вопросы</h2><table>'
    html_content += (
        "<tr><th>№</th><th>Вопрос</th><th>Оценка (1-10)</th><th>Комментарий</th></tr>"
    )

    for i, (topic_name, question) in enumerate(selected_questions["Дополнительные"], 1):
        html_question = convert_markdown_to_html(question)
        html_content += f"""
        <tr>
            <td>{question_num}</td>
            <td>
                <div class="topic">Тема: {topic_name}</div>
                {html_question}
            </td>
            <td><input type="number" name="score_extra_{i}" min="1" max="10"></td>
            <td><textarea name="comment_extra_{i}" rows="3"></textarea></td>
        </tr>
        """
        question_num += 1

    html_content += "</table></div>"

    # Закрываем форму и добавляем JavaScript
    html_content += """
        </form>
        
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
            
            function saveResults() {
                const form = document.getElementById('interviewForm');
                const formData = new FormData(form);
                let results = "Результаты собеседования\\n\\n";
                
                for (let [key, value] of formData.entries()) {
                    if (value.trim() !== '') {
                        results += `${key}: ${value}\\n`;
                    }
                }
                
                const blob = new Blob([results], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'результаты_собеседования.txt';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                
                alert('Результаты сохранены в файл!');
            }

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
        topics = parse_readme("README.md")

        total_questions = 0
        for topic_name, levels in topics.items():
            for level, questions in levels.items():
                total_questions += len(questions)

        if total_questions == 0:
            print("Не найдено ни одного вопроса в README.md!")
            return

        selected = select_random_questions(
            topics, simple_count=2, medium_count=2, hard_count=2, extra_count=3
        )

        output_file = "interview_questions.html"
        generate_html(selected, output_file)

    except FileNotFoundError:
        print("Ошибка: Файл README.md не найден!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
