import factory
from factory.django import DjangoModelFactory

from learning_plan.models import LearningPlan, Lesson, UserProgress
from users.tests.factories import UserFactory


class LearningPlanFactory(DjangoModelFactory):
    """Factory for creating LearningPlan instances in tests."""

    class Meta:
        model = LearningPlan

    user = factory.SubFactory(UserFactory)
    topic = factory.Faker('sentence', nb_words=3)
    time_commitment_per_week = factory.Faker('random_int', min=1, max=20)
    knowledge_level = factory.Iterator(['beginner', 'intermediate', 'experienced'])
    progress = 0.0


class LessonFactory(DjangoModelFactory):
    """Factory for creating Lesson instances in tests."""

    class Meta:
        model = Lesson

    plan = factory.SubFactory(LearningPlanFactory)
    title = factory.Faker('sentence', nb_words=5)
    theory_md = factory.Faker('text', max_nb_chars=500)
    task = factory.Faker('text', max_nb_chars=300)
    lesson_type = factory.Iterator(['theory', 'practice', 'quiz', 'project'])
    time_estimate = factory.Faker('random_int', min=15, max=120)
    day_number = factory.Sequence(lambda n: n + 1)
    extra_links = factory.List([])


class UserProgressFactory(DjangoModelFactory):
    """Factory for creating UserProgress instances in tests."""

    class Meta:
        model = UserProgress

    user = factory.SubFactory(UserFactory)
    lesson = factory.SubFactory(LessonFactory)
    is_completed = False
    completed_at = None
