from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control rounded px-4 py-2 shadow-sm',
        'placeholder': 'Enter Email',
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded px-4 py-2 shadow-sm',
        'placeholder': 'Enter Username',
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded px-4 py-2 shadow-sm',
        'placeholder': 'Enter Password',
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded px-4 py-2 shadow-sm',
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded px-4 py-2 shadow-sm',
        'placeholder': 'Update Username',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control rounded px-4 py-2 shadow-sm',
        'placeholder': 'Update Email',
    }))

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded px-4 py-2 shadow-sm',
        'placeholder': 'Your Address',
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded px-4 py-2 shadow-sm',
        'placeholder': 'Your Phone Number',
    }))
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control-file',
    }))

    class Meta:
        model = Profile
        fields = ['address', 'phone', 'image']




# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from .models import Profile

# class CreateUserForm(UserCreationForm):
#     email = forms.EmailField()
    
#     class Meta:
#         model = User
#         fields = ['username','email','password1','password2']

# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['username','email']

# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model=Profile
#         fields=['address','phone','image']