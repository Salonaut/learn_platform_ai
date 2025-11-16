from django.core.exceptions import ValidationError as DjangoValidationError
from django.test import TestCase
from parameterized import parameterized
from rest_framework.exceptions import ValidationError

from users.models import User
from users.serializers import UserRegistrationSerializer
from users.tests.factories import UserFactory


class TestUserRegistrationSerializer(TestCase):
    """Test UserRegistrationSerializer with real User instances and edge cases."""

    @classmethod
    def setUpTestData(cls):
        """Create shared test data."""
        cls.valid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "StrongPassword123!",
            "password_confirm": "StrongPassword123!"
        }

    def test_registration_success(self):
        """Test successful user registration."""
        serializer = UserRegistrationSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertTrue(user.check_password("StrongPassword123!"))

    def test_registration_password_mismatch(self):
        """Test validation error when passwords don't match."""
        data = self.valid_data.copy()
        data["password_confirm"] = "DifferentPassword456"

        serializer = UserRegistrationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertEqual(User.objects.count(), 0)

    @parameterized.expand([
        ("invalid-email",),
        ("missing@domain",),
        ("@nodomain.com",),
        ("",),
    ])
    def test_registration_invalid_email(self, invalid_email):
        """Test validation error for invalid email formats."""
        data = self.valid_data.copy()
        data["email"] = invalid_email

        serializer = UserRegistrationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_registration_duplicate_email(self):
        """Test validation error when email already exists."""
        UserFactory(email="duplicate@example.com")

        data = self.valid_data.copy()
        data["email"] = "duplicate@example.com"
        data["username"] = "different_username"

        serializer = UserRegistrationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_registration_duplicate_username(self):
        """Test validation error when username already exists."""
        UserFactory(username="existinguser")

        data = self.valid_data.copy()
        data["username"] = "existinguser"

        serializer = UserRegistrationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    @parameterized.expand([
        ("short",),
        ("12345678",),
        ("onlylowercase",),
        ("ONLYUPPERCASE",),
        ("NoNumbers!",),
    ])
    def test_registration_weak_password(self, weak_password):
        """Test validation error for weak passwords."""
        data = self.valid_data.copy()
        data["password"] = weak_password
        data["password_confirm"] = weak_password

        serializer = UserRegistrationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_registration_missing_required_fields(self):
        """Test validation error when required fields are missing."""
        data = {
            "email": "test@example.com",
            "password": "StrongPassword123!",
            "password_confirm": "StrongPassword123!"
        }

        serializer = UserRegistrationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_registration_password_not_stored_in_plain_text(self):
        """Ensure password is hashed and not stored as plain text."""
        serializer = UserRegistrationSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        # Password should not match the raw password
        self.assertNotEqual(user.password, "StrongPassword123!")
        # But check_password should work
        self.assertTrue(user.check_password("StrongPassword123!"))

    def test_password_confirm_not_saved(self):
        """Verify password_confirm is not saved to the database."""
        serializer = UserRegistrationSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        # Verify password_confirm field doesn't exist on the user model
        self.assertFalse(hasattr(user, 'password_confirm'))

    def test_registration_with_whitespace_in_names(self):
        """Test registration handles whitespace in names correctly."""
        data = self.valid_data.copy()
        data["first_name"] = "  John  "
        data["last_name"] = "  Doe  "

        serializer = UserRegistrationSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        # Django strips whitespace by default for CharField
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_registration_optional_names(self):
        """Test registration works without first_name and last_name."""
        data = {
            "username": "minimal_user",
            "email": "minimal@example.com",
            "password": "StrongPassword123!",
            "password_confirm": "StrongPassword123!"
        }

        serializer = UserRegistrationSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")
        self.assertEqual(user.full_name, "")

    def test_write_only_password_fields(self):
        """Verify password fields are write-only and not exposed in output."""
        serializer = UserRegistrationSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        # Create a serializer for the saved user
        output_serializer = UserRegistrationSerializer(instance=user)

        # Password fields should not be in serialized output
        self.assertNotIn('password', output_serializer.data)
        self.assertNotIn('password_confirm', output_serializer.data)
