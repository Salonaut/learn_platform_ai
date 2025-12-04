"""
@file services.py
@brief AI-powered learning plan generation service.

This module provides functions to generate personalized learning plans
using OpenAI's GPT models.
"""

from django.conf import settings

from openai import OpenAI
import json
import re

client = OpenAI(api_key=settings.OPEN_API_KEY)



def generate_learning_plan(topic, level, daily_hours):
    """
    @brief Generate a structured learning plan using AI.
    
    @details Uses OpenAI GPT to create a detailed learning plan with
    daily lessons, theory in Markdown, practical tasks, time estimates,
    and additional resources.
    
    @param topic The subject or topic to learn (string)
    @param level User's knowledge level: 'beginner', 'intermediate', or 'experienced'
    @param daily_hours Time commitment per day in hours (int)
    
    @return List of dictionaries containing lesson information, or None on failure
    
    @throws json.JSONDecodeError if AI response is not valid JSON
    
    @example
    plan = generate_learning_plan("Python Programming", "beginner", 2)
    for lesson in plan:
        print(f"Day {lesson['day']}: {lesson['title']}")
    """
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
