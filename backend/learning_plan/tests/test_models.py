from django.test import TestCase
from django.utils import timezone
from parameterized import parameterized

from learning_plan.models import LearningPlan, Lesson, UserProgress
from learning_plan.tests.factories import (
    LearningPlanFactory,
    LessonFactory,
    UserProgressFactory
)
from users.tests.factories import UserFactory


class TestLearningPlanModel(TestCase):
    """Test LearningPlan model with real instances."""

    @classmethod
    def setUpTestData(cls):
        """Create shared test data."""
        cls.user = UserFactory()
        cls.plan = LearningPlanFactory(user=cls.user, topic="Python Basics")

    def test_str_representation(self):
        """Test __str__ method returns topic."""
        self.assertEqual(str(self.plan), "Python Basics")

    def test_calculate_progress_no_lessons(self):
        """Test calculate_progress returns 0 when no lessons exist."""
        empty_plan = LearningPlanFactory(user=self.user)
        
        progress = empty_plan.calculate_progress()
        
        self.assertEqual(progress, 0.0)
        empty_plan.refresh_from_db()
        self.assertEqual(empty_plan.progress, 0.0)

    def test_calculate_progress_no_completed_lessons(self):
        """Test calculate_progress returns 0 when no lessons are completed."""
        plan = LearningPlanFactory(user=self.user)
        LessonFactory.create_batch(5, plan=plan)
        
        progress = plan.calculate_progress()
        
        self.assertEqual(progress, 0.0)

    def test_calculate_progress_all_completed(self):
        """Test calculate_progress returns 100 when all lessons completed."""
        plan = LearningPlanFactory(user=self.user)
        lessons = LessonFactory.create_batch(4, plan=plan)
        
        # Mark all lessons as completed
        for lesson in lessons:
            UserProgressFactory(
                user=self.user,
                lesson=lesson,
                is_completed=True,
                completed_at=timezone.now()
            )
        
        progress = plan.calculate_progress()
        
        self.assertEqual(progress, 100.0)
        plan.refresh_from_db()
        self.assertEqual(plan.progress, 100.0)

    def test_calculate_progress_half_completed(self):
        """Test calculate_progress returns 50 when half lessons completed."""
        plan = LearningPlanFactory(user=self.user)
        lessons = LessonFactory.create_batch(4, plan=plan)
        
        # Mark half as completed
        for lesson in lessons[:2]:
            UserProgressFactory(
                user=self.user,
                lesson=lesson,
                is_completed=True,
                completed_at=timezone.now()
            )
        
        progress = plan.calculate_progress()
        
        self.assertEqual(progress, 50.0)

    @parameterized.expand([
        (1, 3, 33.33),  # 1 of 3 completed
        (2, 3, 66.67),  # 2 of 3 completed
        (3, 10, 30.0),  # 3 of 10 completed
        (7, 10, 70.0),  # 7 of 10 completed
    ])
    def test_calculate_progress_various_ratios(self, completed, total, expected):
        """Test calculate_progress with various completion ratios."""
        plan = LearningPlanFactory(user=self.user)
        lessons = LessonFactory.create_batch(total, plan=plan)
        
        # Mark specified number as completed
        for lesson in lessons[:completed]:
            UserProgressFactory(
                user=self.user,
                lesson=lesson,
                is_completed=True,
                completed_at=timezone.now()
            )
        
        progress = plan.calculate_progress()
        
        self.assertAlmostEqual(progress, expected, places=2)

    def test_calculate_progress_updates_database(self):
        """Test that calculate_progress saves to database."""
        plan = LearningPlanFactory(user=self.user, progress=0.0)
        lessons = LessonFactory.create_batch(2, plan=plan)
        UserProgressFactory(
            user=self.user,
            lesson=lessons[0],
            is_completed=True
        )
        
        plan.calculate_progress()
        
        # Fetch fresh instance from database
        fresh_plan = LearningPlan.objects.get(id=plan.id)
        self.assertEqual(fresh_plan.progress, 50.0)

    def test_calculate_progress_only_counts_completed(self):
        """Test that only is_completed=True lessons are counted."""
        plan = LearningPlanFactory(user=self.user)
        lessons = LessonFactory.create_batch(4, plan=plan)
        
        # Create progress records but not completed
        for lesson in lessons:
            UserProgressFactory(
                user=self.user,
                lesson=lesson,
                is_completed=False  # Not completed
            )
        
        progress = plan.calculate_progress()
        
        self.assertEqual(progress, 0.0)

    def test_calculate_progress_ignores_other_users(self):
        """Test that progress only counts current user's completions."""
        other_user = UserFactory()
        plan = LearningPlanFactory(user=self.user)
        lessons = LessonFactory.create_batch(2, plan=plan)
        
        # Other user completes a lesson
        UserProgressFactory(
            user=other_user,
            lesson=lessons[0],
            is_completed=True
        )
        
        progress = plan.calculate_progress()
        
        # Should be 0 because other user's progress doesn't count
        self.assertEqual(progress, 0.0)

    @parameterized.expand([
        ('beginner',),
        ('intermediate',),
        ('experienced',),
    ])
    def test_knowledge_level_choices(self, level):
        """Test valid knowledge level choices."""
        plan = LearningPlanFactory(user=self.user, knowledge_level=level)
        self.assertEqual(plan.knowledge_level, level)

    def test_default_knowledge_level(self):
        """Test default knowledge level is beginner."""
        plan = LearningPlan.objects.create(
            user=self.user,
            topic="Test Topic",
            time_commitment_per_week=5
        )
        self.assertEqual(plan.knowledge_level, 'beginner')

    def test_default_progress(self):
        """Test default progress is 0.0."""
        plan = LearningPlan.objects.create(
            user=self.user,
            topic="Test Topic"
        )
        self.assertEqual(plan.progress, 0.0)


class TestLessonModel(TestCase):
    """Test Lesson model with real instances."""

    def test_str_representation(self):
        """Test __str__ method returns title."""
        lesson = LessonFactory(title="Introduction to Python")
        self.assertEqual(str(lesson), "Introduction to Python")

    @parameterized.expand([
        ('theory',),
        ('practice',),
        ('quiz',),
        ('project',),
    ])
    def test_lesson_type_choices(self, lesson_type):
        """Test valid lesson type choices."""
        lesson = LessonFactory(lesson_type=lesson_type)
        self.assertEqual(lesson.lesson_type, lesson_type)

    def test_default_lesson_type(self):
        """Test default lesson type is theory."""
        plan = LearningPlanFactory()
        lesson = Lesson.objects.create(
            plan=plan,
            title="Test Lesson",
            theory_md="Content",
            task="Task",
            time_estimate=30,
            day_number=1
        )
        self.assertEqual(lesson.lesson_type, 'theory')

    def test_lesson_belongs_to_plan(self):
        """Test lesson is properly related to learning plan."""
        plan = LearningPlanFactory()
        lesson = LessonFactory(plan=plan)
        
        self.assertEqual(lesson.plan, plan)
        self.assertIn(lesson, plan.items.all())

    def test_extra_links_default_empty_list(self):
        """Test extra_links defaults to empty list."""
        lesson = LessonFactory()
        self.assertEqual(lesson.extra_links, [])


class TestUserProgressModel(TestCase):
    """Test UserProgress model with real instances."""

    def test_default_is_completed_false(self):
        """Test is_completed defaults to False."""
        progress = UserProgressFactory()
        self.assertFalse(progress.is_completed)

    def test_default_completed_at_none(self):
        """Test completed_at defaults to None."""
        progress = UserProgressFactory()
        self.assertIsNone(progress.completed_at)

    def test_mark_completed(self):
        """Test marking progress as completed."""
        progress = UserProgressFactory()
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()
        
        progress.refresh_from_db()
        self.assertTrue(progress.is_completed)
        self.assertIsNotNone(progress.completed_at)

    def test_user_can_have_multiple_progress_records(self):
        """Test user can have progress for multiple lessons."""
        user = UserFactory()
        plan = LearningPlanFactory(user=user)
        lessons = LessonFactory.create_batch(3, plan=plan)
        
        for lesson in lessons:
            UserProgressFactory(user=user, lesson=lesson)
        
        user_progress_count = UserProgress.objects.filter(user=user).count()
        self.assertEqual(user_progress_count, 3)
