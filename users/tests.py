from django.test import TestCase

from .models import CustomUser


class UserTests(TestCase):
    def test_user_creation(self):
        UserTable = CustomUser
        user = UserTable.objects.create_user(
            username="test", email="test@test.com", password="test12345678"
        )

        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_superuser_creation(self):
        UserTable = CustomUser
        superuser = UserTable.objects.create_superuser(
            username="test", email="test@test.com", password="test12345678"
        )
        self.assertEqual(superuser.username, "test")
        self.assertEqual(superuser.email, "test@test.com")
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
