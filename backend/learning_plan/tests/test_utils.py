import json
from unittest.mock import MagicMock, patch

from django.test import TestCase
from parameterized import parameterized

from learning_plan.services import generate_learning_plan


class TestGenerateLearningPlan(TestCase):
    """Test generate_learning_plan service function."""

    @patch("learning_plan.services.client.responses.create")
    def test_generate_learning_plan_parses_valid_json(self, mock_create):
        """Test successful parsing of valid JSON response."""
        fake_json = json.dumps([
            {
                "day": 1,
                "title": "Introduction to Python",
                "theory_md": "# Python Basics",
                "task": "Print Hello World",
                "task_type": "practice",
                "time_estimate": 30,
                "extra_links": ["https://python.org"]
            }
        ])
        mock_create.return_value = MagicMock(output_text=fake_json)

        result = generate_learning_plan("Python", "beginner", 2)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Introduction to Python")
        self.assertEqual(result[0]["day"], 1)
        self.assertEqual(result[0]["time_estimate"], 30)
        mock_create.assert_called_once()

    @patch("learning_plan.services.client.responses.create")
    def test_generate_learning_plan_multiple_days(self, mock_create):
        """Test parsing multiple days in learning plan."""
        fake_json = json.dumps([
            {"day": 1, "title": "Day 1", "theory_md": "Theory", "task": "Task 1",
             "task_type": "theory", "time_estimate": 30, "extra_links": []},
            {"day": 2, "title": "Day 2", "theory_md": "Theory 2", "task": "Task 2",
             "task_type": "practice", "time_estimate": 45, "extra_links": []},
            {"day": 3, "title": "Day 3", "theory_md": "Theory 3", "task": "Task 3",
             "task_type": "quiz", "time_estimate": 20, "extra_links": []}
        ])
        mock_create.return_value = MagicMock(output_text=fake_json)

        result = generate_learning_plan("Django", "intermediate", 3)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["day"], 1)
        self.assertEqual(result[1]["day"], 2)
        self.assertEqual(result[2]["day"], 3)

    @patch("learning_plan.services.client.responses.create")
    def test_generate_learning_plan_invalid_json_raises(self, mock_create):
        """Test that invalid JSON raises JSONDecodeError."""
        mock_create.return_value = MagicMock(output_text="invalid-json-content")

        with self.assertRaises(json.JSONDecodeError):
            generate_learning_plan("Python", "beginner", 2)

    @patch("learning_plan.services.client.responses.create")
    def test_generate_learning_plan_strips_json_markers(self, mock_create):
        """Test that ```json markers are stripped from response."""
        fake_json_with_markers = '```json\n[{"day":1,"title":"Test"}]\n```'
        mock_create.return_value = MagicMock(output_text=fake_json_with_markers)

        result = generate_learning_plan("React", "beginner", 1)

        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["title"], "Test")

    @patch("learning_plan.services.client.responses.create")
    def test_generate_learning_plan_strips_backticks_only(self, mock_create):
        """Test that only backticks without json keyword are stripped."""
        fake_json_with_backticks = '```\n[{"day":1,"title":"Test"}]\n```'
        mock_create.return_value = MagicMock(output_text=fake_json_with_backticks)

        result = generate_learning_plan("Vue", "beginner", 1)

        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["title"], "Test")

    @patch("learning_plan.services.client.responses.create")
    def test_generate_learning_plan_with_extra_whitespace(self, mock_create):
        """Test that extra whitespace is handled correctly."""
        fake_json_with_space = '  \n\n  [{"day":1,"title":"Test"}]  \n  '
        mock_create.return_value = MagicMock(output_text=fake_json_with_space)

        result = generate_learning_plan("JavaScript", "beginner", 2)

        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["title"], "Test")

    @patch("learning_plan.services.client.responses.create")
    def test_generate_learning_plan_called_with_correct_args(self, mock_create):
        """Test that OpenAI API is called with correct parameters."""
        fake_json = '[{"day":1,"title":"Test"}]'
        mock_create.return_value = MagicMock(output_text=fake_json)

        generate_learning_plan("Python", "beginner", 2)

        mock_create.assert_called_once()
        call_kwargs = mock_create.call_args.kwargs
        self.assertEqual(call_kwargs['model'], "gpt-4.1-mini")
        self.assertIn('Python', call_kwargs['input'])
        self.assertIn('beginner', call_kwargs['input'])

    @parameterized.expand([
        ("Python", "beginner", 1),
        ("Django", "intermediate", 3),
        ("React", "experienced", 5),
    ])
    @patch("learning_plan.services.client.responses.create")
    def test_generate_learning_plan_various_inputs(self, topic, level, hours, mock_create):
        """Test with various topic, level, and hours combinations."""
        fake_json = '[{"day":1,"title":"Test"}]'
        mock_create.return_value = MagicMock(output_text=fake_json)

        result = generate_learning_plan(topic, level, hours)

        self.assertIsInstance(result, list)
        # Verify prompt contains the parameters
        call_kwargs = mock_create.call_args.kwargs
        prompt = call_kwargs['input']
        self.assertIn(topic, prompt)
        self.assertIn(level, prompt)
        self.assertIn(str(hours * 60), prompt)

    @patch("learning_plan.services.client.responses.create")
    def test_generate_learning_plan_empty_array(self, mock_create):
        """Test handling of empty JSON array response."""
        fake_json = '[]'
        mock_create.return_value = MagicMock(output_text=fake_json)

        result = generate_learning_plan("EmptyTopic", "beginner", 1)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    @patch("learning_plan.services.client.responses.create")
    def test_generate_learning_plan_with_extra_links(self, mock_create):
        """Test that extra_links are properly parsed."""
        fake_json = json.dumps([{
            "day": 1,
            "title": "Test",
            "theory_md": "Theory",
            "task": "Task",
            "task_type": "theory",
            "time_estimate": 30,
            "extra_links": [
                "https://link1.com",
                "https://link2.com",
                "https://link3.com"
            ]
        }])
        mock_create.return_value = MagicMock(output_text=fake_json)

        result = generate_learning_plan("Test Topic", "beginner", 2)

        self.assertEqual(len(result[0]["extra_links"]), 3)
        self.assertIn("https://link1.com", result[0]["extra_links"])

    @patch("learning_plan.services.client.responses.create")
    def test_generate_learning_plan_handles_unicode(self, mock_create):
        """Test that unicode characters in response are handled."""
        fake_json = json.dumps([{
            "day": 1,
            "title": "Вивчення Python",
            "theory_md": "# Теорія",
            "task": "Завдання з Unicode: 你好",
            "task_type": "practice",
            "time_estimate": 30,
            "extra_links": []
        }])
        mock_create.return_value = MagicMock(output_text=fake_json)

        result = generate_learning_plan("Python Basics", "beginner", 2)

        self.assertEqual(result[0]["title"], "Вивчення Python")
        self.assertIn("你好", result[0]["task"])

    @patch("learning_plan.services.client.responses.create")
    def test_generate_learning_plan_api_exception_propagates(self, mock_create):
        """Test that API exceptions are propagated."""
        mock_create.side_effect = Exception("API Error")

        with self.assertRaises(Exception) as context:
            generate_learning_plan("Python", "beginner", 2)

        self.assertIn("API Error", str(context.exception))
