from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.utils import timezone
from members.models import Member
from trainers.models import Trainer
from .forms import CustomLoginForm, UserProfileForm, UserManagementForm, CustomSignUpForm

User = get_user_model()

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            # Auto-create profile based on role
            if user.role == User.Role.MEMBER:
                Member.objects.get_or_create(
                    user=user,
                    defaults={
                        'phone': user.phone or '',
                        'email': user.email or '',
                        'joining_date': timezone.now().date(),
                        'status': 'ACTIVE',
                    }
                )
            elif user.role == User.Role.TRAINER:
                Trainer.objects.get_or_create(
                    user=user,
                    defaults={
                        'phone': user.phone or '',
                        'email': user.email or '',
                        'specialization': 'Fitness & Conditioning',
                        'experience': 1,
                        'qualification': 'Certified Trainer',
                        'salary': 0.00,
                        'joining_date': timezone.now().date(),
                    }
                )

            login(request, user)
            messages.success(request, f"Welcome to the Gym, {user.get_full_name_or_username()}! Your account has been created successfully.")
            return redirect('dashboard:index')
        else:
            messages.error(request, "Please correct the registration errors below.")
    else:
        form = CustomSignUpForm()

    return render(request, 'authentication/signup.html', {'form': form})

def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name_or_username()}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard:index')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('accounts:login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'authentication/profile.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was updated successfully!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'authentication/change_password.html', {'form': form})

@login_required
def user_list_view(request):
    if not (request.user.is_admin or request.user.is_staff_user):
        messages.error(request, "Access denied. Only Admins/Staff can manage users.")
        return redirect('dashboard:index')
    
    users = User.objects.all().order_by('-date_joined')
    role_filter = request.GET.get('role', '')
    search_query = request.GET.get('q', '')

    if role_filter:
        users = users.filter(role=role_filter)
    if search_query:
        users = users.filter(username__icontains=search_query) | users.filter(email__icontains=search_query) | users.filter(first_name__icontains=search_query)

    paginator = Paginator(users, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'authentication/user_list.html', {
        'page_obj': page_obj,
        'role_filter': role_filter,
        'search_query': search_query,
        'roles': User.Role.choices,
    })

@login_required
def user_create_view(request):
    if not request.user.is_admin:
        messages.error(request, "Access denied. Only Admin can create system users.")
        return redirect('accounts:user_list')

    if request.method == 'POST':
        form = UserManagementForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            else:
                user.set_password('default123')
            user.save()
            messages.success(request, f"User {user.username} created successfully!")
            return redirect('accounts:user_list')
    else:
        form = UserManagementForm()

    return render(request, 'authentication/user_form.html', {'form': form, 'title': 'Create New User'})

@login_required
def user_edit_view(request, pk):
    if not request.user.is_admin:
        messages.error(request, "Access denied. Only Admin can edit users.")
        return redirect('accounts:user_list')

    target_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserManagementForm(request.POST, instance=target_user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            messages.success(request, f"User {user.username} updated successfully!")
            return redirect('accounts:user_list')
    else:
        form = UserManagementForm(instance=target_user)

    return render(request, 'authentication/user_form.html', {'form': form, 'title': f"Edit User: {target_user.username}", 'target_user': target_user})
