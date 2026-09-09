from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import AuditLog

@login_required
def audit_log_list_view(request):
    if not request.user.is_admin:
        messages.error(request, "Access denied. Only Admin can view system audit logs.")
        return redirect('dashboard:index')

    logs = AuditLog.objects.select_related('user').all()
    action_filter = request.GET.get('action', '')
    if action_filter:
        logs = logs.filter(action__icontains=action_filter)

    paginator = Paginator(logs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'audit_logs/log_list.html', {'page_obj': page_obj, 'action_filter': action_filter})
