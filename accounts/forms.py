from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Enter username or email',
        'id': 'login_username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Enter password',
        'id': 'login_password'
    }))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class UserManagementForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'role', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CustomSignUpForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=User.Role.choices,
        initial=User.Role.MEMBER,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Create a password (min 6 characters)'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Choose a unique username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Phone number (optional)'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        if password and len(password) < 6:
            self.add_error('password', "Password must be at least 6 characters long.")
        return cleaned_data

