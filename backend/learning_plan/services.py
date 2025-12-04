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

# Initialize OpenAI client only if API key is available
try:
    client = OpenAI(api_key=settings.OPEN_API_KEY) if settings.OPEN_API_KEY else None
except Exception:
    client = None



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

    plan_data = json.loads(text)
    return plan_data


def generate_quiz_questions(lesson_theory, lesson_title, num_questions=5):
    """
    @brief Generate quiz questions from lesson theory using AI.
    
    @details Uses OpenAI GPT to analyze lesson content and create
    multiple-choice questions with explanations for testing understanding.
    
    @param lesson_theory The lesson's theory content in Markdown (string)
    @param lesson_title Title of the lesson (string)
    @param num_questions Number of questions to generate (int, default=5)
    
    @return List of dictionaries containing question data, or None on failure
    
    @throws json.JSONDecodeError if AI response is not valid JSON
    
    @example
    questions = generate_quiz_questions(
        "# Python Basics\\n\\nVariables store data...",
        "Introduction to Python",
        5
    )
    for q in questions:
        print(f"Q: {q['question']}")
    """
    prompt = f"""
    На основі наступної теорії уроку "{lesson_title}" створи {num_questions} тестових питань
    для перевірки розуміння матеріалу.
    
    Теорія:
    {lesson_theory[:3000]}
    
    Кожне питання має містити:
    - Текст питання
    - 4 варіанти відповіді (A, B, C, D)
    - Правильну відповідь (A/B/C/D)
    - Коротке пояснення чому це правильна відповідь
    
    Відповідь **тільки у форматі JSON**, без пояснень.
    Формат:
    [
      {{
        "question": string,
        "option_a": string,
        "option_b": string,
        "option_c": string,
        "option_d": string,
        "correct_answer": string (A/B/C/D),
        "explanation": string
      }}
    ]
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    text = response.output_text.strip()

    # clean ```json ... ```
    text = re.sub(r"^```(?:json)?", "", text)
    text = re.sub(r"```$", "", text)
    text = text.strip()

    questions_data = json.loads(text)
    return questions_data
