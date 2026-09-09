from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from .models import MembershipPlan, MemberSubscription
from .forms import MembershipPlanForm, MemberSubscriptionForm
from members.models import Member

@login_required
def plan_list_view(request):
    plans = MembershipPlan.objects.all().order_by('price')
    return render(request, 'memberships/plan_list.html', {'plans': plans})

@login_required
def plan_create_view(request):
    if not request.user.is_admin:
        messages.error(request, "Access denied. Only Admin can create membership plans.")
        return redirect('memberships:plan_list')

    if request.method == 'POST':
        form = MembershipPlanForm(request.POST)
        if form.is_valid():
            plan = form.save()
            messages.success(request, f"Membership Plan '{plan.name}' created successfully!")
            return redirect('memberships:plan_list')
    else:
        form = MembershipPlanForm()

    return render(request, 'memberships/plan_form.html', {'form': form, 'title': 'Create Membership Plan'})

@login_required
def plan_edit_view(request, pk):
    if not request.user.is_admin:
        messages.error(request, "Access denied.")
        return redirect('memberships:plan_list')

    plan = get_object_or_404(MembershipPlan, pk=pk)
    if request.method == 'POST':
        form = MembershipPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, f"Plan '{plan.name}' updated successfully!")
            return redirect('memberships:plan_list')
    else:
        form = MembershipPlanForm(instance=plan)

    return render(request, 'memberships/plan_form.html', {'form': form, 'title': f"Edit Plan: {plan.name}", 'plan': plan})

@login_required
def subscription_list_view(request):
    subscriptions = MemberSubscription.objects.select_related('member', 'membership_plan').all().order_by('-created_at')

    status_filter = request.GET.get('status', '')
    if status_filter:
        subscriptions = subscriptions.filter(status=status_filter)

    paginator = Paginator(subscriptions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'memberships/subscription_list.html', {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'statuses': MemberSubscription.StatusChoices.choices,
    })

@login_required
def subscription_create_view(request):
    if request.user.is_member:
        messages.error(request, "Access denied.")
        return redirect('dashboard:index')

    member_id = request.GET.get('member_id')
    initial_data = {}
    if member_id:
        member = get_object_or_404(Member, pk=member_id)
        initial_data['member'] = member

    if request.method == 'POST':
        form = MemberSubscriptionForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            plan = sub.membership_plan
            sub.price = plan.price
            sub.end_date = sub.start_date + timedelta(days=plan.duration_days)
            sub.save()

            messages.success(request, f"Subscription assigned to {sub.member.full_name} successfully!")
            return redirect('memberships:subscription_list')
    else:
        form = MemberSubscriptionForm(initial=initial_data)

    return render(request, 'memberships/subscription_form.html', {'form': form, 'title': 'Assign Membership Plan'})
