from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from chat.models import ChatModel
from subscribers.models import SubscribeModel

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('/')

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user_name = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=user_name, password=password)
        if user:
            login(request, user)
        return redirect('/')
    return render(request, 'accounts/form.html', {'form': form, 'type': 'login'})

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user_name = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = User.objects.create_user(user_name, email, password, is_staff=False)
        user.save()
        user_profile = UserProfile(profile=user)
        user_profile.save()
        return redirect("/")
    return render(request, 'accounts/form.html', {'form': form, 'type': 'register'})

@login_required(login_url='/login/')
def profile_view(request):
   ############################################################### # print(request.GET.get('parameter1', 'default'))
    user = request.user
    messages = ChatModel.objects.filter(user=user)
    subscribers = SubscribeModel.objects.filter(self_user=user)
    return render(request, 'accounts/profile.html', {'profile': user, 'chat_data': messages, 'subscribers': subscribers})