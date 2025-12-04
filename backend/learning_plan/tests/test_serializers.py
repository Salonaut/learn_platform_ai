from django.test import TestCase
from django.utils import timezone

from learning_plan.models import UserProgress
from learning_plan.serializers import (
    LearningPlanSerializer,
    LessonItemSerializer,
    LessonDetailSerializer
)
from learning_plan.tests.factories import (
    LearningPlanFactory,
    LessonFactory,
    UserProgressFactory
)
from users.tests.factories import UserFactory


class TestLearningPlanSerializer(TestCase):
    """Test LearningPlanSerializer with real instances."""

    @classmethod
    def setUpTestData(cls):
        """Create shared test data."""
        cls.user = UserFactory()
        cls.plan = LearningPlanFactory(
            user=cls.user,
            topic="Django REST Framework",
            progress=25.5
        )

    def test_serialization(self):
        """Test basic serialization of learning plan."""
        serializer = LearningPlanSerializer(instance=self.plan)
        data = serializer.data

        self.assertEqual(data['id'], self.plan.id)
        self.assertEqual(data['topic'], "Django REST Framework")
        self.assertEqual(float(data['progress']), 25.5)
        self.assertIn('created_at', data)

    def test_all_expected_fields_present(self):
        """Verify all expected fields are in serialized output."""
        serializer = LearningPlanSerializer(instance=self.plan)
        data = serializer.data

        expected_fields = {'id', 'topic', 'progress', 'created_at'}
        self.assertEqual(set(data.keys()), expected_fields)

    def test_sensitive_fields_excluded(self):
        """Verify sensitive fields are not in output."""
        serializer = LearningPlanSerializer(instance=self.plan)
        data = serializer.data

        self.assertNotIn('user', data)
        self.assertNotIn('time_commitment_per_week', data)
        self.assertNotIn('knowledge_level', data)

    def test_multiple_plans_serialization(self):
        """Test serializing multiple learning plans."""
        plans = [
            self.plan,
            LearningPlanFactory(user=self.user, topic="Python Advanced"),
            LearningPlanFactory(user=self.user, topic="React Basics"),
        ]

        serializer = LearningPlanSerializer(plans, many=True)
        data = serializer.data

        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['topic'], "Django REST Framework")


class TestLessonItemSerializer(TestCase):
    """Test LessonItemSerializer with real instances."""

    @classmethod
    def setUpTestData(cls):
        """Create shared test data."""
        cls.user = UserFactory()
        cls.plan = LearningPlanFactory(user=cls.user)
        cls.lesson = LessonFactory(
            plan=cls.plan,
            title="Introduction to Views",
            day_number=1,
            time_estimate=45
        )

    def test_get_is_completed_no_user_in_context(self):
        """Test is_completed returns False when no user in context."""
        serializer = LessonItemSerializer(instance=self.lesson, context={})
        data = serializer.data

        self.assertFalse(data['is_completed'])

    def test_get_is_completed_user_not_completed(self):
        """Test is_completed returns False when user hasn't completed."""
        serializer = LessonItemSerializer(
            instance=self.lesson,
            context={'user': self.user}
        )
        data = serializer.data

        self.assertFalse(data['is_completed'])

    def test_get_is_completed_user_completed(self):
        """Test is_completed returns True when user completed."""
        UserProgressFactory(
            user=self.user,
            lesson=self.lesson,
            is_completed=True,
            completed_at=timezone.now()
        )

        serializer = LessonItemSerializer(
            instance=self.lesson,
            context={'user': self.user}
        )
        data = serializer.data

        self.assertTrue(data['is_completed'])

    def test_get_is_completed_not_marked_completed(self):
        """Test is_completed False when progress exists but not completed."""
        UserProgressFactory(
            user=self.user,
            lesson=self.lesson,
            is_completed=False  # Explicitly not completed
        )

        serializer = LessonItemSerializer(
            instance=self.lesson,
            context={'user': self.user}
        )
        data = serializer.data

        self.assertFalse(data['is_completed'])

    def test_serialization_fields(self):
        """Test all expected fields are serialized."""
        serializer = LessonItemSerializer(
            instance=self.lesson,
            context={'user': self.user}
        )
        data = serializer.data

        expected_fields = {'id', 'title', 'day_number', 'time_estimate', 'is_completed'}
        self.assertEqual(set(data.keys()), expected_fields)

    def test_serialization_values(self):
        """Test serialized values match model instance."""
        serializer = LessonItemSerializer(
            instance=self.lesson,
            context={'user': self.user}
        )
        data = serializer.data

        self.assertEqual(data['id'], self.lesson.id)
        self.assertEqual(data['title'], "Introduction to Views")
        self.assertEqual(data['day_number'], 1)
        self.assertEqual(data['time_estimate'], 45)

    def test_is_completed_is_read_only(self):
        """Verify is_completed is a read-only field."""
        serializer = LessonItemSerializer()
        field = serializer.fields['is_completed']

        self.assertTrue(field.read_only)

    def test_multiple_lessons_serialization(self):
        """Test serializing multiple lessons."""
        lessons = [
            self.lesson,
            LessonFactory(plan=self.plan, day_number=2),
            LessonFactory(plan=self.plan, day_number=3),
        ]

        # Mark first as completed
        UserProgressFactory(
            user=self.user,
            lesson=lessons[0],
            is_completed=True
        )

        serializer = LessonItemSerializer(
            lessons,
            many=True,
            context={'user': self.user}
        )
        data = serializer.data

        self.assertEqual(len(data), 3)
        self.assertTrue(data[0]['is_completed'])
        self.assertFalse(data[1]['is_completed'])
        self.assertFalse(data[2]['is_completed'])

    def test_different_users_have_different_completion_status(self):
        """Test that is_completed is user-specific."""
        other_user = UserFactory()

        # Only other_user completed the lesson
        UserProgressFactory(
            user=other_user,
            lesson=self.lesson,
            is_completed=True
        )

        # Serialize for self.user
        serializer1 = LessonItemSerializer(
            instance=self.lesson,
            context={'user': self.user}
        )

        # Serialize for other_user
        serializer2 = LessonItemSerializer(
            instance=self.lesson,
            context={'user': other_user}
        )

        self.assertFalse(serializer1.data['is_completed'])
        self.assertTrue(serializer2.data['is_completed'])


class TestLessonDetailSerializer(TestCase):
    """Test LessonDetailSerializer with real instances."""

    @classmethod
    def setUpTestData(cls):
        """Create shared test data."""
        cls.lesson = LessonFactory(
            title="Advanced Django",
            theory_md="# Theory Content",
            task="Complete the exercise",
            time_estimate=60,
            day_number=5,
            extra_links=["https://docs.djangoproject.com", "https://example.com"]
        )

    def test_serialization(self):
        """Test basic serialization of lesson detail."""
        serializer = LessonDetailSerializer(instance=self.lesson)
        data = serializer.data

        self.assertEqual(data['id'], self.lesson.id)
        self.assertEqual(data['title'], "Advanced Django")
        self.assertEqual(data['theory_md'], "# Theory Content")
        self.assertEqual(data['task'], "Complete the exercise")
        self.assertEqual(data['time_estimate'], 60)
        self.assertEqual(data['day_number'], 5)
        self.assertEqual(data['extra_links'], ["https://docs.djangoproject.com", "https://example.com"])

    def test_all_expected_fields_present(self):
        """Verify all expected fields are in serialized output."""
        serializer = LessonDetailSerializer(instance=self.lesson)
        data = serializer.data

        expected_fields = {
            'id', 'title', 'theory_md', 'task',
            'time_estimate', 'extra_links', 'day_number'
        }
        self.assertEqual(set(data.keys()), expected_fields)

    def test_plan_not_in_output(self):
        """Verify plan relationship is not exposed."""
        serializer = LessonDetailSerializer(instance=self.lesson)
        data = serializer.data

        self.assertNotIn('plan', data)

    def test_lesson_type_not_in_output(self):
        """Verify lesson_type is not in detail serializer."""
        serializer = LessonDetailSerializer(instance=self.lesson)
        data = serializer.data

        self.assertNotIn('lesson_type', data)

    def test_empty_extra_links(self):
        """Test serialization with empty extra_links."""
        lesson = LessonFactory(extra_links=[])
        serializer = LessonDetailSerializer(instance=lesson)
        data = serializer.data

        self.assertEqual(data['extra_links'], [])

    def test_extra_links_with_multiple_urls(self):
        """Test serialization with multiple extra links."""
        lesson = LessonFactory(
            extra_links=[
                "https://link1.com",
                "https://link2.com",
                "https://link3.com"
            ]
        )
        serializer = LessonDetailSerializer(instance=lesson)
        data = serializer.data

        self.assertEqual(len(data['extra_links']), 3)
        self.assertIn("https://link1.com", data['extra_links'])
