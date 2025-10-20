from django.test import TestCase, SimpleTestCase
from rest_framework.exceptions import ValidationError
from unittest.mock import MagicMock, patch


from users.models import User
from users.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    UserChangePasswordSerializer
)



class TestUserRegistrationSerializer(TestCase):

    def test_registration_success(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "StrongPassword123",
            "password_confirm": "StrongPassword123"
        }
        serializer = UserRegistrationSerializer(data=data)


        self.assertTrue(serializer.is_valid())


        user = serializer.save()


        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "Test")
        self.assertTrue(user.check_password("StrongPassword123"))

    def test_registration_password_mismatch(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPassword123",
            "password_confirm": "WrongPassword456"
        }
        serializer = UserRegistrationSerializer(data=data)


        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertEqual(User.objects.count(), 0)



class TestUserLoginSerializer(SimpleTestCase):

    @patch('users.serializers.authenticate')
    def test_login_success(self, mock_authenticate):
        user_mock = MagicMock(spec=User, is_active=True)
        mock_authenticate.return_value = user_mock

        data = {"email": "test@example.com", "password": "password123"}


        mock_request = MagicMock()
        serializer = UserLoginSerializer(
            data=data,
            context={'request': mock_request}
        )

        self.assertTrue(serializer.is_valid())
        mock_authenticate.assert_called_with(
            request=mock_request,
            username="test@example.com",
            password="password123"
        )
        self.assertEqual(serializer.validated_data['user'], user_mock)

    @patch('users.serializers.authenticate')
    def test_login_user_not_found(self, mock_authenticate):
        mock_authenticate.return_value = None  # Імітуємо невдалу автентифікацію
        data = {"email": "wrong@example.com", "password": "wrong"}

        serializer = UserLoginSerializer(
            data=data,
            context={'request': MagicMock()}
        )


        with self.assertRaises(ValidationError) as e:
            serializer.is_valid(raise_exception=True)


        self.assertEqual(
            str(e.exception.detail['non_field_errors'][0]),
            'User not found'
        )

    @patch('users.serializers.authenticate')
    def test_login_user_inactive(self, mock_authenticate):
        user_mock = MagicMock(spec=User, is_active=False)  # Неактивний юзер
        mock_authenticate.return_value = user_mock

        data = {"email": "test@example.com", "password": "password123"}
        serializer = UserLoginSerializer(
            data=data,
            context={'request': MagicMock()}
        )

        with self.assertRaises(ValidationError) as e:
            serializer.is_valid(raise_exception=True)


        self.assertEqual(
            str(e.exception.detail['non_field_errors'][0]),
            'User account is disabled.'
        )



class TestUserProfileSerializer(SimpleTestCase):

    def test_profile_serialization(self):
        user = User(
            first_name="Тест",
            last_name="Юзер",
            progress="in_progress"
        )

        serializer = UserProfileSerializer(instance=user)
        data = serializer.data

        self.assertEqual(data['full_name'], "Тест Юзер")
        self.assertEqual(data['progress_status'], "In progress")

    def test_progress_status_logic(self):
        serializer = UserProfileSerializer()


        user_not_started = User(progress=None)
        self.assertEqual(
            serializer.get_progress_status(user_not_started),
            "Not started"
        )


        user_completed = User(progress="completed")
        self.assertEqual(
            serializer.get_progress_status(user_completed),
            "Completed"
        )



class TestUserUpdateSerializer(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="updater",
            email="update@example.com",
            password="password123",
            bio="Original bio"
        )

    def test_user_update(self):
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
        serializer.save()


        self.user.refresh_from_db()

        self.assertEqual(self.user.first_name, "Оновлене")
        self.assertEqual(self.user.bio, "Нове біо")
        self.assertEqual(self.user.social_media, "http://linked.in")



class TestUserChangePasswordSerializer(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="pass_changer",
            email="pass@example.com",
            password="OldPassword123"
        )
        self.request = MagicMock()
        self.request.user = self.user
        self.context = {'request': self.request}

    def test_change_password_success(self):
        data = {
            "old_password": "OldPassword123",
            "new_password": "NewStrongPassword456",
            "new_password_confirm": "NewStrongPassword456"
        }
        serializer = UserChangePasswordSerializer(data=data, context=self.context)

        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()


        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewStrongPassword456"))
        self.assertFalse(self.user.check_password("OldPassword123"))

    def test_change_password_wrong_old_password(self):

        data = {
            "old_password": "WRONG_OLD_PASSWORD",
            "new_password": "NewStrongPassword456",
            "new_password_confirm": "NewStrongPassword456"
        }
        serializer = UserChangePasswordSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn("old_password", serializer.errors)

    def test_change_password_new_password_mismatch(self):
        data = {
            "old_password": "OldPassword123",
            "new_password": "NewPassword1",
            "new_password_confirm": "NewPassword2"
        }
        serializer = UserChangePasswordSerializer(data=data, context=self.context)

        self.assertFalse(serializer.is_valid())
        self.assertIn("new_password", serializer.errors)