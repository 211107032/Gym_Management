from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta, datetime
from members.models import Member
from memberships.models import MembershipPlan, MemberSubscription
from attendance.models import Attendance
from payments.models import Payment
from trainers.models import Trainer, TrainerAssignment
from workouts.models import WorkoutPlan, MemberProgress

@login_required
def index_view(request):
    user = request.user
    today = timezone.now().date()
    month_start = today.replace(day=1)

    # Automatically check/update expired memberships
    MemberSubscription.objects.filter(end_date__lt=today, status='ACTIVE').update(status='EXPIRED')

    if user.is_admin:
        total_members = Member.objects.count()
        active_members = Member.objects.filter(status='ACTIVE').count()
        expired_members = Member.objects.filter(status='EXPIRED').count()
        total_trainers = Trainer.objects.count()

        today_attendance_count = Attendance.objects.filter(date=today).count()
        monthly_revenue = Payment.objects.filter(status='PAID', payment_date__gte=month_start).aggregate(Sum('amount'))['amount__sum'] or 0.00
        pending_payments = Payment.objects.filter(status='PENDING').aggregate(Sum('amount'))['amount__sum'] or 0.00

        expiring_soon_count = MemberSubscription.objects.filter(
            status='ACTIVE',
            end_date__range=[today, today + timedelta(days=7)]
        ).count()

        recent_members = Member.objects.select_related('user').order_by('-joining_date')[:5]
        recent_payments = Payment.objects.select_related('member__user').order_by('-payment_date')[:5]
        top_plans = MembershipPlan.objects.annotate(subs_count=Count('subscriptions')).order_by('-subs_count')[:4]

        context = {
            'total_members': total_members,
            'active_members': active_members,
            'expired_members': expired_members,
            'total_trainers': total_trainers,
            'today_attendance_count': today_attendance_count,
            'monthly_revenue': monthly_revenue,
            'pending_payments': pending_payments,
            'expiring_soon_count': expiring_soon_count,
            'recent_members': recent_members,
            'recent_payments': recent_payments,
            'top_plans': top_plans,
            'role_template': 'dashboard/admin_dashboard.html'
        }

    elif user.is_staff_user:
        total_members = Member.objects.count()
        today_attendance = Attendance.objects.filter(date=today).count()
        active_memberships = MemberSubscription.objects.filter(status='ACTIVE').count()
        expiring_memberships = MemberSubscription.objects.filter(status='ACTIVE', end_date__range=[today, today + timedelta(days=7)]).count()

        recent_payments = Payment.objects.select_related('member__user').order_by('-payment_date')[:5]
        recent_checkins = Attendance.objects.select_related('member__user').filter(date=today).order_by('-check_in_time')[:5]

        context = {
            'total_members': total_members,
            'today_attendance': today_attendance,
            'active_memberships': active_memberships,
            'expiring_memberships': expiring_memberships,
            'recent_payments': recent_payments,
            'recent_checkins': recent_checkins,
            'role_template': 'dashboard/staff_dashboard.html'
        }

    elif user.is_trainer:
        trainer = getattr(user, 'trainer_profile', None)
        assigned_memberships = []
        workout_plans = []
        if trainer:
            assigned_memberships = TrainerAssignment.objects.filter(trainer=trainer).select_related('member__user')
            workout_plans = WorkoutPlan.objects.filter(trainer=trainer).select_related('member__user')

        context = {
            'trainer': trainer,
            'assigned_memberships': assigned_memberships,
            'workout_plans': workout_plans,
            'role_template': 'dashboard/trainer_dashboard.html'
        }

    else: # MEMBER
        member = getattr(user, 'member_profile', None)
        sub = member.active_subscription if member else None
        trainer_assign = member.assigned_trainers.select_related('trainer__user').first() if member else None
        workout_plan = member.workout_plans.order_by('-created_at').first() if member else None
        payments = member.payments.order_by('-payment_date')[:5] if member else []

        total_days = Attendance.objects.filter(member=member).count() if member else 0
        present_days = Attendance.objects.filter(member=member, status='PRESENT').count() if member else 0
        attendance_pct = round((present_days / total_days * 100), 1) if total_days > 0 else 100.0

        context = {
            'member': member,
            'subscription': sub,
            'trainer_assign': trainer_assign,
            'workout_plan': workout_plan,
            'payments': payments,
            'attendance_pct': attendance_pct,
            'role_template': 'dashboard/member_dashboard.html'
        }

    return render(request, 'dashboard/index.html', context)

@login_required
def chart_analytics_api(request):
    today = timezone.now().date()

    # 1. Member Growth (Last 6 Months)
    growth_labels = []
    growth_data = []
    for i in range(5, -1, -1):
        m_date = today - timedelta(days=i*30)
        m_start = m_date.replace(day=1)
        if m_start.month == 12:
            m_end = m_start.replace(year=m_start.year+1, month=1, day=1) - timedelta(days=1)
        else:
            m_end = m_start.replace(month=m_start.month+1, day=1) - timedelta(days=1)

        count = Member.objects.filter(joining_date__range=[m_start, m_end]).count()
        growth_labels.append(m_start.strftime('%b %Y'))
        growth_data.append(count)

    # 2. Revenue Trend (Last 6 Months)
    revenue_data = []
    for i in range(5, -1, -1):
        m_date = today - timedelta(days=i*30)
        m_start = m_date.replace(day=1)
        if m_start.month == 12:
            m_end = m_start.replace(year=m_start.year+1, month=1, day=1) - timedelta(days=1)
        else:
            m_end = m_start.replace(month=m_start.month+1, day=1) - timedelta(days=1)

        rev = Payment.objects.filter(status='PAID', payment_date__range=[m_start, m_end]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        revenue_data.append(float(rev))

    # 3. Attendance Breakdown (Current Month)
    month_start = today.replace(day=1)
    present_cnt = Attendance.objects.filter(date__gte=month_start, status='PRESENT').count()
    late_cnt = Attendance.objects.filter(date__gte=month_start, status='LATE').count()
    absent_cnt = Attendance.objects.filter(date__gte=month_start, status='ABSENT').count()

    # 4. Membership Distribution
    plans = MembershipPlan.objects.annotate(s_count=Count('subscriptions'))
    plan_labels = [p.name for p in plans]
    plan_counts = [p.s_count for p in plans]

    return JsonResponse({
        'growth': {
            'labels': growth_labels,
            'data': growth_data
        },
        'revenue': {
            'labels': growth_labels,
            'data': revenue_data
        },
        'attendance': {
            'labels': ['Present', 'Late', 'Absent'],
            'data': [present_cnt, late_cnt, absent_cnt]
        },
        'membership': {
            'labels': plan_labels,
            'data': plan_counts
        }
    })
