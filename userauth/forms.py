from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EditProfileForm(forms.ModelForm):
    image= forms.ImageField(required=True)
    first_name= forms.CharField(widget= forms.TextInput(attrs= {'class': 'input'}), required=True)
    bio= forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'image', 'location', 'bio', 'url')

class UserRegistrationForm(UserCreationForm):
    first_name= forms.CharField(widget= forms.TextInput(attrs= {'class': 'input', 'placeholder': 'First Name'}))
    last_name= forms.CharField(widget= forms.TextInput(attrs= {'class': 'input', 'placeholder': 'Last Name'}), required=False)
    username= forms.CharField(widget= forms.TextInput(attrs= {'class': 'input', 'placeholder': 'Username'}))
    email= forms.EmailField(widget= forms.TextInput(attrs= {'class': 'input', 'placeholder': 'Email'}))
    password1= forms.CharField(widget= forms.PasswordInput(attrs= {'class': 'input', 'placeholder': 'Password'}))
    password2= forms.CharField(widget= forms.PasswordInput(attrs= {'class': 'input', 'placeholder': 'Confirm Password'}))
    class Meta:
        model= User
        fields= ('first_name', 'last_name', 'username','email', 'password1', 'password2')

