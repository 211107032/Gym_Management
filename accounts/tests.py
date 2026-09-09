from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTests(TestCase):
    def test_create_custom_user(self):
        user = User.objects.create_user(
            username='testmember',
            password='password123',
            email='test@example.com',
            role=User.Role.MEMBER
        )
        self.assertEqual(user.username, 'testmember')
        self.assertTrue(user.is_member)
        self.assertFalse(user.is_admin)

    def test_admin_role_permissions(self):
        admin = User.objects.create_superuser(
            username='adminuser',
            password='password123',
            email='admin@example.com'
        )
        self.assertTrue(admin.is_admin)
        self.assertTrue(admin.is_staff_user)
