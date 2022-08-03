import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Violations
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя:',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(label='Пароль:',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UsrRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя:',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(label='имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))

    password1 = forms.CharField(label='Пароль:',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля:',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


# class NewsForm(forms.ModelForm):
#     class Meta:
#         model = News
#         fields = ['title', 'content', 'is_published', 'category']
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
#             'category': forms.Select(attrs={'class': 'form-control'}),
#         }
#
#     def clean_title(self):
#         title = self.cleaned_data['title']
#         if re.match(r'\d', title):
#             raise ValidationError('Название не может начинаться с цифры')
#         return title
