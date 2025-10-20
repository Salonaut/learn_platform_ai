from django.test import SimpleTestCase
from unittest.mock import MagicMock, patch
from learning_plan.models import LearningPlan


class TestLearningPlanModel(SimpleTestCase):

    def test_calculate_progress_no_lessons(self):
        plan_mock = MagicMock(spec=LearningPlan)


        plan_mock.items.count.return_value = 0


        progress = LearningPlan.calculate_progress(plan_mock)


        self.assertEqual(progress, 0.0)
        plan_mock.save.assert_called_once_with(update_fields=["progress"])

    @patch("learning_plan.models.UserProgress.objects.filter")
    def test_calculate_progress_half_done(self, mock_filter):

        plan_mock = MagicMock(spec=LearningPlan)
        plan_mock.items.count.return_value = 4
        mock_filter.return_value.count.return_value = 2


        result = LearningPlan.calculate_progress(plan_mock)

        self.assertEqual(result, 50.0)
        plan_mock.save.assert_called_once_with(update_fields=["progress"])
        mock_filter.assert_called_once()
