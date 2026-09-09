from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from .models import Payment
from .forms import PaymentForm
from members.models import Member
from memberships.models import MemberSubscription
from gym_settings.models import GymSetting

@login_required
def payment_list_view(request):
    payments = Payment.objects.select_related('member__user', 'subscription__membership_plan').all().order_by('-payment_date', '-created_at')

    if request.user.is_member and hasattr(request.user, 'member_profile'):
        payments = payments.filter(member=request.user.member_profile)

    method_filter = request.GET.get('method', '')
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '')

    if method_filter:
        payments = payments.filter(payment_method=method_filter)

    if status_filter:
        payments = payments.filter(status=status_filter)

    if search_query:
        payments = payments.filter(
            Q(payment_id__icontains=search_query) |
            Q(member__member_id__icontains=search_query) |
            Q(member__user__first_name__icontains=search_query) |
            Q(member__user__last_name__icontains=search_query) |
            Q(transaction_id__icontains=search_query)
        )

    total_collected = payments.filter(status='PAID').aggregate(Sum('amount'))['amount__sum'] or 0.00

    paginator = Paginator(payments, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'payments/payment_list.html', {
        'page_obj': page_obj,
        'method_filter': method_filter,
        'status_filter': status_filter,
        'search_query': search_query,
        'total_collected': total_collected,
        'methods': Payment.MethodChoices.choices,
        'statuses': Payment.StatusChoices.choices,
    })

@login_required
def payment_create_view(request):
    if request.user.is_member:
        messages.error(request, "Access denied.")
        return redirect('dashboard:index')

    member_id = request.GET.get('member_id')
    sub_id = request.GET.get('sub_id')
    initial_data = {}

    if member_id:
        member = get_object_or_404(Member, pk=member_id)
        initial_data['member'] = member
    if sub_id:
        sub = get_object_or_404(MemberSubscription, pk=sub_id)
        initial_data['subscription'] = sub
        initial_data['amount'] = sub.final_amount

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            messages.success(request, f"Payment {payment.payment_id} of ₹{payment.amount} recorded successfully!")
            return redirect('payments:receipt', pk=payment.pk)
    else:
        form = PaymentForm(initial=initial_data)

    return render(request, 'payments/payment_form.html', {'form': form, 'title': 'Record New Payment'})

@login_required
def payment_receipt_view(request, pk):
    payment = get_object_or_404(Payment.objects.select_related('member__user', 'subscription__membership_plan'), pk=pk)

    if request.user.is_member and hasattr(request.user, 'member_profile') and request.user.member_profile.id != payment.member.id:
        messages.error(request, "Access denied.")
        return redirect('dashboard:index')

    gym_info = GymSetting.get_settings()

    return render(request, 'payments/receipt.html', {
        'payment': payment,
        'gym_info': gym_info
    })
