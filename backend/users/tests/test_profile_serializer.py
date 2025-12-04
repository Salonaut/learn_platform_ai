from django.test import TestCase
from parameterized import parameterized

from users.models import User
from users.serializers import UserProfileSerializer
from users.tests.factories import UserFactory


class TestUserProfileSerializer(TestCase):
    """Test UserProfileSerializer with real User instances and edge cases."""

    @classmethod
    def setUpTestData(cls):
        """Create shared test data."""
        cls.user = UserFactory(
            first_name="Тест",
            last_name="Юзер",
            email="test@example.com",
            bio="Test bio",
            progress="in_progress"
        )

    def test_profile_serialization(self):
        """Test basic profile serialization with real user."""
        serializer = UserProfileSerializer(instance=self.user)
        data = serializer.data

        self.assertEqual(data['full_name'], "Тест Юзер")
        self.assertEqual(data['progress_status'], "In progress")
        self.assertEqual(data['email'], "test@example.com")
        self.assertEqual(data['bio'], "Test bio")

    @parameterized.expand([
        (None, "Not started"),
        ("completed", "Completed"),
        ("in_progress", "In progress"),
        ("unknown_status", "unknown_status"),
        ("", "Not started"),
    ])
    def test_progress_status_logic(self, progress_value, expected_status):
        """Test progress_status method with various progress values."""
        user = User(progress=progress_value)
        serializer = UserProfileSerializer()

        result = serializer.get_progress_status(user)
        self.assertEqual(result, expected_status)

    def test_full_name_is_read_only(self):
        """Verify full_name field is read-only."""
        serializer = UserProfileSerializer()
        full_name_field = serializer.fields['full_name']

        self.assertTrue(full_name_field.read_only)

    def test_progress_status_is_read_only(self):
        """Verify progress_status field is read-only."""
        serializer = UserProfileSerializer()
        progress_status_field = serializer.fields['progress_status']

        self.assertTrue(progress_status_field.read_only)

    def test_all_expected_fields_present(self):
        """Verify all expected fields are in serialized output."""
        serializer = UserProfileSerializer(instance=self.user)
        data = serializer.data

        expected_fields = {
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'avatar', 'bio', 'created_at', 'updated_at',
            'progress', 'progress_status'
        }

        self.assertEqual(set(data.keys()), expected_fields)

    def test_password_not_in_output(self):
        """Verify password is not exposed in serialized output."""
        serializer = UserProfileSerializer(instance=self.user)
        data = serializer.data

        self.assertNotIn('password', data)

    def test_serialization_with_minimal_user(self):
        """Test serialization works with minimal user data."""
        minimal_user = UserFactory(
            first_name="",
            last_name="",
            bio="",
            progress=None
        )

        serializer = UserProfileSerializer(instance=minimal_user)
        data = serializer.data

        self.assertEqual(data['full_name'], "")
        self.assertEqual(data['progress_status'], "Not started")
        self.assertEqual(data['bio'], "")

    def test_serialization_with_avatar(self):
        """Test serialization includes avatar field."""
        serializer = UserProfileSerializer(instance=self.user)
        data = serializer.data

        self.assertIn('avatar', data)

    def test_created_and_updated_timestamps(self):
        """Verify timestamps are included in serialized output."""
        serializer = UserProfileSerializer(instance=self.user)
        data = serializer.data

        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
        self.assertIsNotNone(data['created_at'])
        self.assertIsNotNone(data['updated_at'])

    def test_serializer_cannot_update_read_only_fields(self):
        """Verify read-only fields are not updated even if provided."""
        data = {
            'full_name': 'This Should Be Ignored',
            'progress_status': 'This Should Also Be Ignored',
            'bio': 'New bio'
        }

        serializer = UserProfileSerializer(
            instance=self.user,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        # full_name is computed from first_name and last_name
        self.assertEqual(updated_user.full_name, "Тест Юзер")
        # bio should be updated
        self.assertEqual(updated_user.bio, "New bio")

    def test_many_users_serialization(self):
        """Test serializing multiple users."""
        users = [
            UserFactory(progress="completed"),
            UserFactory(progress="in_progress"),
            UserFactory(progress=None),
        ]

        serializer = UserProfileSerializer(users, many=True)
        data = serializer.data

        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['progress_status'], "Completed")
        self.assertEqual(data[1]['progress_status'], "In progress")
        self.assertEqual(data[2]['progress_status'], "Not started")
