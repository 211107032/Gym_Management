from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Member
from .forms import MemberForm

User = get_user_model()

@login_required
def member_list_view(request):
    members = Member.objects.select_related('user').all().order_by('-joining_date')

    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '')

    if status_filter:
        members = members.filter(status=status_filter)

    if search_query:
        members = members.filter(
            Q(member_id__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    paginator = Paginator(members, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'members/member_list.html', {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
        'statuses': Member.StatusChoices.choices,
    })

@login_required
def member_detail_view(request, pk):
    member = get_object_or_404(Member.objects.select_related('user'), pk=pk)
    
    # Check permissions
    if request.user.is_member and hasattr(request.user, 'member_profile') and request.user.member_profile.id != member.id:
        messages.error(request, "Access denied. You can only view your own profile.")
        return redirect('dashboard:index')

    subscriptions = member.subscriptions.select_related('membership_plan').all().order_by('-created_at')
    payments = member.payments.all().order_by('-payment_date')
    attendances = member.attendances.all().order_by('-date')[:10]
    assigned_trainer = member.assigned_trainers.select_related('trainer__user').first()
    workout_plans = member.workout_plans.all().order_by('-created_at')
    progress_records = member.progress_records.all().order_by('date')

    return render(request, 'members/member_detail.html', {
        'member': member,
        'subscriptions': subscriptions,
        'payments': payments,
        'attendances': attendances,
        'assigned_trainer': assigned_trainer,
        'workout_plans': workout_plans,
        'progress_records': progress_records,
    })

@login_required
def member_create_view(request):
    if request.user.is_member:
        messages.error(request, "Access denied.")
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password'] or 'member123'
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose another.")
                return render(request, 'members/member_form.html', {'form': form, 'title': 'Register New Member'})

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=User.Role.MEMBER,
                phone=form.cleaned_data['phone']
            )

            member = form.save(commit=False)
            member.user = user
            member.save()

            messages.success(request, f"Member {member.full_name} ({member.member_id}) registered successfully!")
            return redirect('members:detail', pk=member.pk)
    else:
        form = MemberForm()

    return render(request, 'members/member_form.html', {'form': form, 'title': 'Register New Member'})

@login_required
def member_edit_view(request, pk):
    member = get_object_or_404(Member, pk=pk)

    if request.user.is_member and hasattr(request.user, 'member_profile') and request.user.member_profile.id != member.id:
        messages.error(request, "Access denied.")
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            user = member.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()

            form.save()
            messages.success(request, f"Member {member.member_id} updated successfully!")
            return redirect('members:detail', pk=member.pk)
    else:
        initial_data = {
            'first_name': member.user.first_name,
            'last_name': member.user.last_name,
            'username': member.user.username,
        }
        form = MemberForm(instance=member, initial=initial_data)

    return render(request, 'members/member_form.html', {'form': form, 'title': f"Edit Member: {member.member_id}", 'member': member})

@login_required
def member_delete_view(request, pk):
    if not request.user.is_admin:
        messages.error(request, "Access denied. Only Admin can delete members.")
        return redirect('members:list')

    member = get_object_or_404(Member, pk=pk)
    user = member.user
    if request.method == 'POST':
        member_id = member.member_id
        user.delete() # Cascades to member
        messages.success(request, f"Member {member_id} deleted successfully.")
        return redirect('members:list')

    return render(request, 'members/member_confirm_delete.html', {'member': member})
