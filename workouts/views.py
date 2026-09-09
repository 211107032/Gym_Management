from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import WorkoutPlan, WorkoutExercise, MemberProgress
from .forms import WorkoutPlanForm, WorkoutExerciseForm, MemberProgressForm
from members.models import Member

@login_required
def workout_list_view(request):
    plans = WorkoutPlan.objects.select_related('member__user', 'trainer__user').all().order_by('-created_at')

    if request.user.is_member and hasattr(request.user, 'member_profile'):
        plans = plans.filter(member=request.user.member_profile)
    elif request.user.is_trainer and hasattr(request.user, 'trainer_profile'):
        plans = plans.filter(trainer=request.user.trainer_profile)

    paginator = Paginator(plans, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'workouts/workout_list.html', {'page_obj': page_obj})

@login_required
def workout_detail_view(request, pk):
    plan = get_object_or_404(WorkoutPlan.objects.select_related('member__user', 'trainer__user'), pk=pk)

    if request.user.is_member and hasattr(request.user, 'member_profile') and request.user.member_profile.id != plan.member.id:
        messages.error(request, "Access denied.")
        return redirect('dashboard:index')

    exercises = plan.exercises.all()
    exercise_form = WorkoutExerciseForm()

    if request.method == 'POST':
        if request.user.is_member:
            messages.error(request, "Members cannot add exercises.")
            return redirect('workouts:detail', pk=pk)

        exercise_form = WorkoutExerciseForm(request.POST)
        if exercise_form.is_valid():
            ex = exercise_form.save(commit=False)
            ex.workout_plan = plan
            ex.save()
            messages.success(request, f"Exercise '{ex.exercise_name}' added to plan successfully!")
            return redirect('workouts:detail', pk=pk)

    return render(request, 'workouts/workout_detail.html', {
        'plan': plan,
        'exercises': exercises,
        'exercise_form': exercise_form
    })

@login_required
def workout_create_view(request):
    if request.user.is_member:
        messages.error(request, "Access denied.")
        return redirect('dashboard:index')

    initial_data = {}
    member_id = request.GET.get('member_id')
    if member_id:
        member = get_object_or_404(Member, pk=member_id)
        initial_data['member'] = member

    if request.user.is_trainer and hasattr(request.user, 'trainer_profile'):
        initial_data['trainer'] = request.user.trainer_profile

    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            plan = form.save()
            messages.success(request, f"Workout Plan '{plan.name}' created for {plan.member.full_name}!")
            return redirect('workouts:detail', pk=plan.pk)
    else:
        form = WorkoutPlanForm(initial=initial_data)

    return render(request, 'workouts/workout_form.html', {'form': form, 'title': 'Create Workout Plan'})

@login_required
def progress_list_view(request):
    member_id = request.GET.get('member_id')
    if request.user.is_member and hasattr(request.user, 'member_profile'):
        member = request.user.member_profile
    elif member_id:
        member = get_object_or_404(Member, pk=member_id)
    else:
        member = Member.objects.filter(status='ACTIVE').first()

    progress_records = []
    if member:
        progress_records = MemberProgress.objects.filter(member=member).order_by('date')

    if request.method == 'POST':
        form = MemberProgressForm(request.POST)
        if form.is_valid():
            rec = form.save()
            messages.success(request, f"Progress logged for {rec.member.full_name} ({rec.weight}kg, BMI {rec.bmi})!")
            return redirect(f"{request.path}?member_id={rec.member.id}")
    else:
        initial_data = {'member': member} if member else {}
        if member:
            initial_data['weight'] = member.weight
            initial_data['height'] = member.height
        form = MemberProgressForm(initial=initial_data)

    members_list = Member.objects.all().select_related('user')

    return render(request, 'workouts/progress_list.html', {
        'member': member,
        'progress_records': progress_records,
        'form': form,
        'members_list': members_list
    })

@login_required
def progress_chart_data(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    records = MemberProgress.objects.filter(member=member).order_by('date')

    labels = [r.date.strftime('%b %d, %Y') for r in records]
    weights = [float(r.weight) for r in records]
    bmis = [float(r.bmi) if r.bmi else None for r in records]
    body_fats = [float(r.body_fat_percentage) if r.body_fat_percentage else None for r in records]

    return JsonResponse({
        'member_name': member.full_name,
        'labels': labels,
        'weights': weights,
        'bmis': bmis,
        'body_fats': body_fats
    })
