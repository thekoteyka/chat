from django import forms
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

User = get_user_model()

class RegisterForm(forms.Form):
    def clean_username(self):
        profile = self.cleaned_data.get('username')
        queryset = User.objects.filter(username__iexact=profile)

        if queryset.exists():
            raise forms.ValidationError("Имя пользователя уже существует")

        return profile

    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form__password'
            }
        )
    )

class LoginForm(forms.Form):
    def clean_username(self):
        profile = self.cleaned_data.get('username')
        queryset = User.objects.filter(username__iexact=profile)

        if not queryset.exists():
            # raise forms.ValidationError('Неправильное имя пользователя или пароль')
            return redirect('/')

        return profile

    username = forms.CharField(label='Your name:')
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form__password'
            }
        )
    )