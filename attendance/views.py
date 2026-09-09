from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from .models import Attendance
from .forms import AttendanceForm, QuickCheckInForm
from members.models import Member

@login_required
def attendance_list_view(request):
    selected_date_str = request.GET.get('date', timezone.now().strftime('%Y-%m-%d'))
    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = timezone.now().date()

    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    attendances = Attendance.objects.select_related('member__user').filter(date=selected_date)

    if status_filter:
        attendances = attendances.filter(status=status_filter)

    if search_query:
        attendances = attendances.filter(
            Q(member__member_id__icontains=search_query) |
            Q(member__user__first_name__icontains=search_query) |
            Q(member__user__last_name__icontains=search_query) |
            Q(member__phone__icontains=search_query)
        )

    # Calculate stats for the selected date
    total_members = Member.objects.filter(status='ACTIVE').count()
    today_attendances = Attendance.objects.filter(date=selected_date)
    present_count = today_attendances.filter(status='PRESENT').count()
    late_count = today_attendances.filter(status='LATE').count()
    absent_count = max(0, total_members - (present_count + late_count))

    paginator = Paginator(attendances, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    check_in_form = QuickCheckInForm()

    return render(request, 'attendance/attendance_list.html', {
        'page_obj': page_obj,
        'selected_date': selected_date.strftime('%Y-%m-%d'),
        'search_query': search_query,
        'status_filter': status_filter,
        'present_count': present_count,
        'late_count': late_count,
        'absent_count': absent_count,
        'total_members': total_members,
        'check_in_form': check_in_form,
        'statuses': Attendance.StatusChoices.choices,
    })

@login_required
def check_in_view(request):
    if request.user.is_member:
        messages.error(request, "Access denied.")
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = QuickCheckInForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['member_identifier'].strip()
            member = Member.objects.filter(
                Q(member_id__iexact=identifier) |
                Q(phone__iexact=identifier) |
                Q(user__username__iexact=identifier)
            ).first()

            if not member:
                messages.error(request, f"No active member found matching '{identifier}'.")
                return redirect('attendance:list')

            today = timezone.now().date()
            current_time = timezone.now().time()

            existing = Attendance.objects.filter(member=member, date=today).first()
            if existing:
                messages.warning(request, f"Member {member.full_name} ({member.member_id}) is already checked in for today at {existing.check_in_time.strftime('%I:%M %p')}.")
            else:
                Gym_opening = timezone.now().replace(hour=8, minute=0, second=0).time()
                status = Attendance.StatusChoices.LATE if current_time > Gym_opening else Attendance.StatusChoices.PRESENT

                Attendance.objects.create(
                    member=member,
                    date=today,
                    check_in_time=current_time,
                    status=status
                )
                messages.success(request, f"Checked in {member.full_name} ({member.member_id}) successfully at {current_time.strftime('%I:%M %p')}!")

    return redirect('attendance:list')

@login_required
def check_out_view(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    attendance.check_out_time = timezone.now().time()
    attendance.save()
    messages.success(request, f"Checked out {attendance.member.full_name} at {attendance.check_out_time.strftime('%I:%M %p')}.")
    return redirect('attendance:list')
