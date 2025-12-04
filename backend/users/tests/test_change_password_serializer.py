from unittest.mock import MagicMock

from django.test import TestCase
from parameterized import parameterized
from rest_framework.exceptions import ValidationError

from users.serializers import UserChangePasswordSerializer
from users.tests.factories import UserFactory


class TestUserChangePasswordSerializer(TestCase):
    """Test UserChangePasswordSerializer with proper validation and edge cases."""

    def setUp(self):
        """Set up test data for each test."""
        self.user = UserFactory(password="OldPassword123!")
        self.request = MagicMock()
        self.request.user = self.user
        self.context = {'request': self.request}

    def test_change_password_success(self):
        """Test successful password change."""
        data = {
            "old_password": "OldPassword123!",
            "new_password": "NewStrongPassword456!",
            "new_password_confirm": "NewStrongPassword456!"
        }

        serializer = UserChangePasswordSerializer(data=data, context=self.context)

        self.assertTrue(serializer.is_valid(raise_exception=True))
        returned_user = serializer.save()

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewStrongPassword456!"))
        self.assertFalse(self.user.check_password("OldPassword123!"))
        self.assertEqual(returned_user.id, self.user.id)

    def test_change_password_wrong_old_password(self):
        """Test validation error for incorrect old password."""
        data = {
            "old_password": "WrongOldPassword",
            "new_password": "NewStrongPassword456!",
            "new_password_confirm": "NewStrongPassword456!"
        }

        serializer = UserChangePasswordSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn("old_password", serializer.errors)

        # Verify error message contains expected keyword
        error_message = str(serializer.errors['old_password'][0])
        self.assertIn('incorrect', error_message.lower())

    def test_change_password_new_passwords_mismatch(self):
        """Test validation error when new passwords don't match."""
        data = {
            "old_password": "OldPassword123!",
            "new_password": "NewPassword1!",
            "new_password_confirm": "NewPassword2!"
        }

        serializer = UserChangePasswordSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn("new_password", serializer.errors)

        # Check error contains keyword about mismatch
        error_message = str(serializer.errors['new_password'][0])
        self.assertIn('match', error_message.lower())

    @parameterized.expand([
        ("short",),
        ("12345678",),
        ("onlylowercase",),
        ("ONLYUPPERCASE",),
        ("NoNumbers!",),
    ])
    def test_change_password_weak_new_password(self, weak_password):
        """Test validation error for weak new passwords."""
        data = {
            "old_password": "OldPassword123!",
            "new_password": weak_password,
            "new_password_confirm": weak_password
        }

        serializer = UserChangePasswordSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn("new_password", serializer.errors)

    def test_change_password_missing_old_password(self):
        """Test validation error when old_password is missing."""
        data = {
            "new_password": "NewStrongPassword456!",
            "new_password_confirm": "NewStrongPassword456!"
        }

        serializer = UserChangePasswordSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn("old_password", serializer.errors)

    def test_change_password_missing_new_password(self):
        """Test validation error when new_password is missing."""
        data = {
            "old_password": "OldPassword123!",
            "new_password_confirm": "NewStrongPassword456!"
        }

        serializer = UserChangePasswordSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn("new_password", serializer.errors)

    def test_change_password_missing_new_password_confirm(self):
        """Test validation error when new_password_confirm is missing."""
        data = {
            "old_password": "OldPassword123!",
            "new_password": "NewStrongPassword456!"
        }

        serializer = UserChangePasswordSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn("new_password_confirm", serializer.errors)

    def test_change_password_empty_old_password(self):
        """Test validation error for empty old_password."""
        data = {
            "old_password": "",
            "new_password": "NewStrongPassword456!",
            "new_password_confirm": "NewStrongPassword456!"
        }

        serializer = UserChangePasswordSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn("old_password", serializer.errors)

    def test_change_password_empty_new_password(self):
        """Test validation error for empty new_password."""
        data = {
            "old_password": "OldPassword123!",
            "new_password": "",
            "new_password_confirm": ""
        }

        serializer = UserChangePasswordSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn("new_password", serializer.errors)

    def test_all_fields_are_required(self):
        """Test validation error when all fields are missing."""
        data = {}

        serializer = UserChangePasswordSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn("old_password", serializer.errors)
        self.assertIn("new_password", serializer.errors)
        self.assertIn("new_password_confirm", serializer.errors)

    def test_password_is_actually_changed_in_database(self):
        """Verify password is actually changed and saved in database."""
        data = {
            "old_password": "OldPassword123!",
            "new_password": "SuperNewPassword789!",
            "new_password_confirm": "SuperNewPassword789!"
        }

        serializer = UserChangePasswordSerializer(data=data, context=self.context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Create a fresh instance from database to verify persistence
        fresh_user = UserFactory._meta.model.objects.get(id=self.user.id)
        self.assertTrue(fresh_user.check_password("SuperNewPassword789!"))
        self.assertFalse(fresh_user.check_password("OldPassword123!"))

    def test_password_fields_are_write_only(self):
        """Verify all password fields are write-only."""
        serializer = UserChangePasswordSerializer()

        for field_name in ['old_password', 'new_password', 'new_password_confirm']:
            with self.subTest(field=field_name):
                field = serializer.fields[field_name]
                self.assertTrue(field.write_only)

    def test_same_old_and_new_password(self):
        """Test that using the same password as new password is allowed."""
        # This is typically a business rule - some apps disallow it, others allow
        # Testing current behavior
        data = {
            "old_password": "OldPassword123!",
            "new_password": "OldPassword123!",
            "new_password_confirm": "OldPassword123!"
        }

        serializer = UserChangePasswordSerializer(data=data, context=self.context)

        # Current implementation allows this; if you want to prevent it,
        # you would add validation and update this test
        self.assertTrue(serializer.is_valid())

    def test_password_validators_are_applied(self):
        """Test that Django's password validators are applied to new password."""
        data = {
            "old_password": "OldPassword123!",
            "new_password": "123",  # Too short
            "new_password_confirm": "123"
        }

        serializer = UserChangePasswordSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        # Either new_password or new_password_confirm should have errors
        has_password_error = (
            'new_password' in serializer.errors or
            'new_password_confirm' in serializer.errors
        )
        self.assertTrue(has_password_error)

    def test_old_password_validation_before_new_password_validation(self):
        """Test that old_password is validated first."""
        data = {
            "old_password": "WrongPassword",
            "new_password": "NewPassword1",
            "new_password_confirm": "NewPassword2"  # Mismatch
        }

        serializer = UserChangePasswordSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        # old_password error should be present
        self.assertIn("old_password", serializer.errors)
