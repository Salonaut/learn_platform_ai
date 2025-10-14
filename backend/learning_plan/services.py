from django.conf import settings

from openai import OpenAI
import json
import re

client = OpenAI(api_key=settings.OPEN_API_KEY)



def generate_learning_plan(topic, level, daily_hours):
    prompt = f"""
    Створи навчальний план по темі "{topic}".
    Рівень знань: {level}.
    Кожен день має містити:
    - Назву мікроуроку
    - Теорію (у форматі Markdown)
    - Практичне завдання
    - Орієнтовний час (у хвилинах, не перевищуючи {daily_hours * 60})
    - 2-3 посилання на додаткові ресурси

    Відповідь **тільки у форматі JSON**, без пояснень.
    Формат:
    [
      {{
        "day": int,
        "title": string,
        "theory_md": string,
        "task": string,
        "task_type": string,
        "time_estimate": int,
        "extra_links": [string]
      }}
    ]
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    text = response.output_text.strip()

    # clear ```json ... ```
    text = re.sub(r"^```(?:json)?", "", text)
    text = re.sub(r"```$", "", text)
    text = text.strip()


    try:
        plan_data = json.loads(text)
    except json.JSONDecodeError as e:
        raise e

    return plan_data
