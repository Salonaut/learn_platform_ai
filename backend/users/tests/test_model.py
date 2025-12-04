from django.test import TestCase
from parameterized import parameterized

from users.models import User
from users.tests.factories import UserFactory


class TestUserModel(TestCase):
    """Test User model behavior with real instances."""

    @classmethod
    def setUpTestData(cls):
        """Create shared test data once for all test methods."""
        cls.user = UserFactory(
            first_name="Іван",
            last_name="Петренко",
            email="ivan@example.com"
        )

    @parameterized.expand([
        ("Іван", "Петренко", "Іван Петренко"),
        ("Марія", "", "Марія"),
        ("", "Шевченко", "Шевченко"),
        ("", "", ""),
        ("  Петро  ", "  Коваль  ", "Петро    Коваль"),
        ("Single", None, "Single"),
        (None, "LastOnly", "LastOnly"),
        (None, None, ""),
    ])
    def test_full_name_property(self, first_name, last_name, expected):
        """Test full_name property with various input combinations."""
        user = User(first_name=first_name or "", last_name=last_name or "")
        self.assertEqual(user.full_name, expected)

    def test_full_name_on_real_user(self):
        """Test full_name on an actual saved user instance."""
        self.assertEqual(self.user.full_name, "Іван Петренко")

    def test_str_representation(self):
        """Test __str__ method returns email."""
        self.assertEqual(str(self.user), "ivan@example.com")

    def test_username_field_is_email(self):
        """Verify USERNAME_FIELD is set to email for authentication."""
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_user_creation_with_factory(self):
        """Test user creation using factory."""
        user = UserFactory()
        self.assertIsNotNone(user.id)
        self.assertTrue(user.email)
        self.assertTrue(user.check_password('defaultPassword123!'))

    def test_user_active_by_default(self):
        """Test that users are active by default."""
        user = UserFactory()
        self.assertTrue(user.is_active)

