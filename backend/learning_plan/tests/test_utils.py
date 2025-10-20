from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock
from learning_plan.services import generate_learning_plan
import pytest

class TestGenerateLearningPlan(SimpleTestCase):

    @patch("learning_plan.services.client.responses.create")
    def test_generate_learning_plan_parses_json(self, mock_create):
        fake_json = '[{"day":1,"title":"Intro"}]'
        mock_create.return_value = MagicMock(output_text=fake_json)

        result = generate_learning_plan("Python", "beginner", 2)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["title"], "Intro")
        mock_create.assert_called_once()

    @patch("learning_plan.services.client.responses.create")
    def test_generate_learning_plan_invalid_json_raises(self, mock_create):
        mock_create.return_value = MagicMock(output_text="invalid-json")
        with pytest.raises(Exception):
            generate_learning_plan("Python", "beginner", 2)
