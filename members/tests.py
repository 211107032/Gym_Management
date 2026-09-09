from django.test import TestCase
from django.contrib.auth import get_user_model
from members.models import Member

User = get_user_model()

class MemberModelTests(TestCase):
    def test_member_auto_id_formatting(self):
        user = User.objects.create_user(username='john_doe', password='pass', email='john@test.com')
        member = Member.objects.create(
            user=user,
            phone='1234567890',
            email='john@test.com'
        )
        self.assertEqual(member.member_id, 'MEM-0001')
        self.assertEqual(member.full_name, 'john_doe')
