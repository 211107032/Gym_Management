import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from members.models import Member
from memberships.models import MembershipPlan, MemberSubscription
from payments.models import Payment
from attendance.models import Attendance

@login_required
def report_index_view(request):
    if not (request.user.is_admin or request.user.is_staff_user):
        messages.error(request, "Access denied.")
        return redirect('dashboard:index')

    total_members = Member.objects.count()
    active_members = Member.objects.filter(status='ACTIVE').count()
    expired_members = Member.objects.filter(status='EXPIRED').count()
    
    total_revenue = Payment.objects.filter(status='PAID').aggregate(Sum('amount'))['amount__sum'] or 0.00
    month_start = timezone.now().date().replace(day=1)
    monthly_revenue = Payment.objects.filter(status='PAID', payment_date__gte=month_start).aggregate(Sum('amount'))['amount__sum'] or 0.00

    plan_stats = MembershipPlan.objects.annotate(sub_count=Count('subscriptions')).order_by('-sub_count')

    return render(request, 'reports/report_index.html', {
        'total_members': total_members,
        'active_members': active_members,
        'expired_members': expired_members,
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'plan_stats': plan_stats
    })

@login_required
def export_csv_view(request, report_type):
    if not (request.user.is_admin or request.user.is_staff_user):
        messages.error(request, "Access denied.")
        return redirect('dashboard:index')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{report_type}_report_{timezone.now().strftime("%Y%m%d")}.csv"'
    writer = csv.writer(response)

    if report_type == 'members':
        writer.writerow(['Member ID', 'Full Name', 'Username', 'Email', 'Phone', 'Joining Date', 'Status', 'Height', 'Weight'])
        members = Member.objects.select_related('user').all()
        for m in members:
            writer.writerow([m.member_id, m.full_name, m.user.username, m.email, m.phone, m.joining_date, m.status, m.height, m.weight])

    elif report_type == 'payments':
        writer.writerow(['Payment ID', 'Member ID', 'Member Name', 'Plan', 'Amount', 'Method', 'Payment Date', 'Status', 'Transaction ID'])
        payments = Payment.objects.select_related('member__user', 'subscription__membership_plan').all()
        for p in payments:
            plan_name = p.subscription.membership_plan.name if p.subscription else 'N/A'
            writer.writerow([p.payment_id, p.member.member_id, p.member.full_name, plan_name, p.amount, p.get_payment_method_display(), p.payment_date, p.status, p.transaction_id])

    elif report_type == 'attendance':
        writer.writerow(['Date', 'Member ID', 'Member Name', 'Check-In Time', 'Check-Out Time', 'Status'])
        attendances = Attendance.objects.select_related('member__user').all()
        for a in attendances:
            cin = a.check_in_time.strftime('%I:%M %p') if a.check_in_time else ''
            cout = a.check_out_time.strftime('%I:%M %p') if a.check_out_time else ''
            writer.writerow([a.date, a.member.member_id, a.member.full_name, cin, cout, a.get_status_display()])

    elif report_type == 'subscriptions':
        writer.writerow(['Member ID', 'Member Name', 'Plan Name', 'Start Date', 'End Date', 'Price', 'Discount', 'Final Amount', 'Status'])
        subscriptions = MemberSubscription.objects.select_related('member__user', 'membership_plan').all()
        for s in subscriptions:
            writer.writerow([s.member.member_id, s.member.full_name, s.membership_plan.name, s.start_date, s.end_date, s.price, s.discount, s.final_amount, s.status])

    return response
