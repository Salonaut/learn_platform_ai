from django.test import SimpleTestCase
from unittest.mock import MagicMock
from users.models import User

class TestUserModel(SimpleTestCase):

    def test_full_name_property(self):
        user_mock = MagicMock(spec=User)
        user_mock.first_name = "Іван"
        user_mock.last_name = "Петренко"

        full_name = User.full_name.fget(user_mock)

        self.assertEqual(full_name, "Іван Петренко")

    def test_full_name_property_only_first_name(self):
        user_mock = MagicMock(spec=User)
        user_mock.first_name = "Марія"
        user_mock.last_name = ""

        full_name = User.full_name.fget(user_mock)

        self.assertEqual(full_name, "Марія")

    def test_full_name_property_empty(self):
        user_mock = MagicMock(spec=User)
        user_mock.first_name = ""
        user_mock.last_name = ""

        full_name = User.full_name.fget(user_mock)

        self.assertEqual(full_name, "")

