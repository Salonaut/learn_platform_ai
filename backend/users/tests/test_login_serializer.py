from unittest.mock import MagicMock, patch

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from users.models import User
from users.serializers import UserLoginSerializer
from users.tests.factories import UserFactory


class TestUserLoginSerializer(TestCase):
    """Test UserLoginSerializer with proper mocking and error assertions."""

    @classmethod
    def setUpTestData(cls):
        """Create shared test data."""
        cls.user = UserFactory(
            email="test@example.com",
            password="ValidPassword123!",
            is_active=True
        )

    def setUp(self):
        """Set up test context for each test."""
        self.request = MagicMock()
        self.context = {'request': self.request}

    @patch('users.serializers.authenticate')
    def test_login_success(self, mock_authenticate):
        """Test successful login returns user in validated_data."""
        mock_authenticate.return_value = self.user

        data = {
            "email": "test@example.com",
            "password": "ValidPassword123!"
        }

        serializer = UserLoginSerializer(data=data, context=self.context)

        self.assertTrue(serializer.is_valid())
        mock_authenticate.assert_called_once_with(
            request=self.request,
            username="test@example.com",
            password="ValidPassword123!"
        )
        self.assertEqual(serializer.validated_data['user'], self.user)

    @patch('users.serializers.authenticate')
    def test_login_user_not_found(self, mock_authenticate):
        """Test login fails when authentication returns None."""
        mock_authenticate.return_value = None

        data = {
            "email": "wrong@example.com",
            "password": "WrongPassword"
        }

        serializer = UserLoginSerializer(data=data, context=self.context)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        # Assert on error key/structure, not exact message
        errors = context.exception.detail
        self.assertIn('non_field_errors', errors)
        # Check message contains expected keyword
        error_message = str(errors['non_field_errors'][0])
        self.assertIn('not found', error_message.lower())

    @patch('users.serializers.authenticate')
    def test_login_user_inactive(self, mock_authenticate):
        """Test login fails for inactive users."""
        inactive_user = UserFactory(is_active=False)
        mock_authenticate.return_value = inactive_user

        data = {
            "email": "inactive@example.com",
            "password": "ValidPassword123!"
        }

        serializer = UserLoginSerializer(data=data, context=self.context)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        errors = context.exception.detail
        self.assertIn('non_field_errors', errors)
        error_message = str(errors['non_field_errors'][0])
        self.assertIn('disabled', error_message.lower())

    def test_login_missing_email(self):
        """Test validation error when email is missing."""
        data = {"password": "ValidPassword123!"}

        serializer = UserLoginSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_login_missing_password(self):
        """Test validation error when password is missing."""
        data = {"email": "test@example.com"}

        serializer = UserLoginSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_login_both_fields_missing(self):
        """Test validation error when both fields are missing."""
        data = {}

        serializer = UserLoginSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertIn('password', serializer.errors)

    def test_login_invalid_email_format(self):
        """Test validation error for invalid email format."""
        data = {
            "email": "not-an-email",
            "password": "ValidPassword123!"
        }

        serializer = UserLoginSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_login_empty_email(self):
        """Test validation error for empty email."""
        data = {
            "email": "",
            "password": "ValidPassword123!"
        }

        serializer = UserLoginSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_login_empty_password(self):
        """Test validation error for empty password."""
        data = {
            "email": "test@example.com",
            "password": ""
        }

        serializer = UserLoginSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_password_is_write_only(self):
        """Verify password field is write-only and not exposed."""
        serializer = UserLoginSerializer()

        password_field = serializer.fields['password']
        self.assertTrue(password_field.write_only)

    @patch('users.serializers.authenticate')
    def test_authenticate_called_with_correct_params(self, mock_authenticate):
        """Verify authenticate is called with email as username."""
        mock_authenticate.return_value = self.user

        data = {
            "email": "test@example.com",
            "password": "ValidPassword123!"
        }

        serializer = UserLoginSerializer(data=data, context=self.context)
        serializer.is_valid()

        # Verify authenticate is called with email as username parameter
        call_kwargs = mock_authenticate.call_args.kwargs
        self.assertEqual(call_kwargs['username'], "test@example.com")
        self.assertEqual(call_kwargs['password'], "ValidPassword123!")
        self.assertEqual(call_kwargs['request'], self.request)
