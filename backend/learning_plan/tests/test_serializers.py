from django.test import SimpleTestCase
from unittest.mock import MagicMock, patch
from learning_plan.serializers import LessonItemSerializer
from learning_plan.models import Lesson


class TestLessonItemSerializer(SimpleTestCase):

    def test_get_is_completed_no_user(self):
        lesson = Lesson.__new__(Lesson)
        serializer = LessonItemSerializer(context={})

        result = serializer.get_is_completed(lesson)

        self.assertFalse(result)

    @patch("learning_plan.serializers.UserProgress.objects.filter")
    def test_get_is_completed_with_user(self, mock_filter):
        mock_filter.return_value.exists.return_value = True
        lesson = Lesson.__new__(Lesson)
        user = MagicMock()
        serializer = LessonItemSerializer(context={"user": user})

        result = serializer.get_is_completed(lesson)

        self.assertTrue(result)
        mock_filter.assert_called_once_with(user=user, lesson=lesson, is_completed=True)
