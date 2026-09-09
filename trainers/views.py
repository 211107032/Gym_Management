from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Trainer, TrainerAssignment
from .forms import TrainerForm, AssignMemberForm
from members.models import Member

User = get_user_model()

@login_required
def trainer_list_view(request):
    trainers = Trainer.objects.select_related('user').all().order_by('-joining_date')
    search_query = request.GET.get('q', '')

    if search_query:
        trainers = trainers.filter(
            Q(trainer_id__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(specialization__icontains=search_query)
        )

    paginator = Paginator(trainers, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'trainers/trainer_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
    })

@login_required
def trainer_detail_view(request, pk):
    trainer = get_object_or_404(Trainer.objects.select_related('user'), pk=pk)
    assigned_memberships = trainer.assigned_members.select_related('member__user').all()

    return render(request, 'trainers/trainer_detail.html', {
        'trainer': trainer,
        'assigned_memberships': assigned_memberships
    })

@login_required
def trainer_create_view(request):
    if not request.user.is_admin:
        messages.error(request, "Access denied. Only Admin can add trainers.")
        return redirect('trainers:list')

    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password'] or 'trainer123'
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return render(request, 'trainers/trainer_form.html', {'form': form, 'title': 'Add New Trainer'})

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=User.Role.TRAINER,
                phone=form.cleaned_data['phone']
            )

            trainer = form.save(commit=False)
            trainer.user = user
            trainer.save()

            messages.success(request, f"Trainer {trainer.full_name} ({trainer.trainer_id}) added successfully!")
            return redirect('trainers:detail', pk=trainer.pk)
    else:
        form = TrainerForm()

    return render(request, 'trainers/trainer_form.html', {'form': form, 'title': 'Add New Trainer'})

@login_required
def trainer_edit_view(request, pk):
    if not request.user.is_admin:
        messages.error(request, "Access denied.")
        return redirect('trainers:list')

    trainer = get_object_or_404(Trainer, pk=pk)
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            user = trainer.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()

            form.save()
            messages.success(request, f"Trainer {trainer.trainer_id} updated successfully!")
            return redirect('trainers:detail', pk=trainer.pk)
    else:
        initial_data = {
            'first_name': trainer.user.first_name,
            'last_name': trainer.user.last_name,
            'username': trainer.user.username,
        }
        form = TrainerForm(instance=trainer, initial=initial_data)

    return render(request, 'trainers/trainer_form.html', {'form': form, 'title': f"Edit Trainer: {trainer.trainer_id}", 'trainer': trainer})

@login_required
def assign_member_view(request):
    if request.user.is_member:
        messages.error(request, "Access denied.")
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = AssignMemberForm(request.POST)
        if form.is_valid():
            assignment, created = TrainerAssignment.objects.get_or_create(
                trainer=form.cleaned_data['trainer'],
                member=form.cleaned_data['member']
            )
            if created:
                messages.success(request, f"Assigned {assignment.member.full_name} to {assignment.trainer.full_name}.")
            else:
                messages.info(request, f"Member {assignment.member.full_name} is already assigned to {assignment.trainer.full_name}.")
            return redirect('trainers:detail', pk=assignment.trainer.pk)
    else:
        form = AssignMemberForm()

    return render(request, 'trainers/assign_form.html', {'form': form})
