from django.test import TestCase
from parameterized import parameterized

from users.serializers import UserUpdateSerializer
from users.tests.factories import UserFactory


class TestUserUpdateSerializer(TestCase):
    """Test UserUpdateSerializer with factories and edge cases."""

    @classmethod
    def setUpTestData(cls):
        """Create shared test data."""
        cls.user = UserFactory(
            first_name="Original",
            last_name="Name",
            bio="Original bio",
            social_media="http://old.com"
        )

    def test_user_update_all_fields(self):
        """Test updating all allowed fields."""
        data = {
            "first_name": "Оновлене",
            "last_name": "Ім'я",
            "bio": "Нове біо",
            "social_media": "http://linked.in"
        }

        serializer = UserUpdateSerializer(
            instance=self.user,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.user.refresh_from_db()

        self.assertEqual(self.user.first_name, "Оновлене")
        self.assertEqual(self.user.last_name, "Ім'я")
        self.assertEqual(self.user.bio, "Нове біо")
        self.assertEqual(self.user.social_media, "http://linked.in")
        self.assertEqual(updated_user.id, self.user.id)

    def test_user_partial_update(self):
        """Test partial update only changes provided fields."""
        data = {"bio": "Only bio updated"}

        serializer = UserUpdateSerializer(
            instance=self.user,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.user.refresh_from_db()

        self.assertEqual(self.user.bio, "Only bio updated")
        self.assertEqual(self.user.first_name, "Original")
        self.assertEqual(self.user.last_name, "Name")

    def test_update_first_name_only(self):
        """Test updating only first name."""
        data = {"first_name": "NewFirst"}

        serializer = UserUpdateSerializer(
            instance=self.user,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "NewFirst")
        self.assertEqual(self.user.last_name, "Name")

    def test_update_clears_bio(self):
        """Test that bio can be cleared with empty string."""
        data = {"bio": ""}

        serializer = UserUpdateSerializer(
            instance=self.user,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, "")

    def test_update_returns_updated_instance(self):
        """Verify save() returns the updated user instance."""
        data = {"first_name": "Updated"}

        serializer = UserUpdateSerializer(
            instance=self.user,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid())
        returned_user = serializer.save()

        self.assertEqual(returned_user.id, self.user.id)
        self.assertEqual(returned_user.first_name, "Updated")

    def test_only_allowed_fields_in_serializer(self):
        """Verify only specific fields are allowed for update."""
        serializer = UserUpdateSerializer()

        expected_fields = {'first_name', 'last_name', 'avatar', 'bio', 'social_media'}
        actual_fields = set(serializer.fields.keys())

        self.assertEqual(actual_fields, expected_fields)

    def test_cannot_update_email_through_serializer(self):
        """Verify email cannot be updated through this serializer."""
        data = {
            "email": "newemail@example.com",
            "first_name": "Test"
        }

        serializer = UserUpdateSerializer(
            instance=self.user,
            data=data,
            partial=True
        )

        # Email should be ignored since it's not in the serializer fields
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.user.refresh_from_db()
        # Email should remain unchanged
        self.assertNotEqual(self.user.email, "newemail@example.com")
        # But first_name should be updated
        self.assertEqual(self.user.first_name, "Test")

    def test_cannot_update_username_through_serializer(self):
        """Verify username cannot be updated through this serializer."""
        original_username = self.user.username

        data = {
            "username": "newusername",
            "bio": "New bio"
        }

        serializer = UserUpdateSerializer(
            instance=self.user,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, original_username)
        self.assertEqual(self.user.bio, "New bio")

    @parameterized.expand([
        ("", "", "", ""),
        ("  ", "  ", "  ", "  "),
        ("Valid", "Name", "Valid bio", "http://social.com"),
    ])
    def test_update_with_various_values(self, first_name, last_name, bio, social_media):
        """Test update handles various input values."""
        user = UserFactory()
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "bio": bio,
            "social_media": social_media
        }

        serializer = UserUpdateSerializer(
            instance=user,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        user.refresh_from_db()
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.bio, bio)
        self.assertEqual(user.social_media, social_media)

    def test_update_with_empty_data(self):
        """Test update with empty data doesn't change anything."""
        original_first_name = self.user.first_name

        data = {}

        serializer = UserUpdateSerializer(
            instance=self.user,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, original_first_name)

    def test_update_with_none_values(self):
        """Test update handles None values for nullable fields."""
        data = {
            "social_media": None,
            "bio": "Bio remains"
        }

        serializer = UserUpdateSerializer(
            instance=self.user,
            data=data,
            partial=True
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.user.refresh_from_db()
        self.assertIsNone(self.user.social_media)
        self.assertEqual(self.user.bio, "Bio remains")
