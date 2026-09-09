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

    def test_signup_view_creates_user_and_member_profile(self):
        response = self.client.post('/accounts/signup/', {
            'username': 'newmember',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newmember@example.com',
            'phone': '1234567890',
            'role': User.Role.MEMBER,
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='newmember')
        self.assertIsNotNone(user)
        self.assertTrue(hasattr(user, 'member_profile'))
        self.assertEqual(user.member_profile.status, 'ACTIVE')

    def test_signup_view_creates_trainer_profile(self):
        response = self.client.post('/accounts/signup/', {
            'username': 'newtrainer',
            'first_name': 'Trainer',
            'last_name': 'One',
            'email': 'newtrainer@example.com',
            'phone': '9876543210',
            'role': User.Role.TRAINER,
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='newtrainer')
        self.assertIsNotNone(user)
        self.assertTrue(hasattr(user, 'trainer_profile'))

