from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from members.models import Member
from memberships.models import MembershipPlan, MemberSubscription

User = get_user_model()

class SubscriptionTests(TestCase):
    def test_subscription_expiry_calculation(self):
        user = User.objects.create_user(username='sub_user', password='pass')
        member = Member.objects.create(user=user, phone='111', email='s@test.com')
        plan = MembershipPlan.objects.create(name='Monthly', duration_days=30, price=1000)

        sub = MemberSubscription.objects.create(
            member=member,
            membership_plan=plan,
            start_date=timezone.now().date()
        )
        self.assertEqual(sub.end_date, timezone.now().date() + timedelta(days=30))
        self.assertEqual(sub.status, 'ACTIVE')
        self.assertEqual(sub.remaining_days, 30)
