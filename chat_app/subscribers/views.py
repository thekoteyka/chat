from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import SubscribeModel
from django.contrib.auth.decorators import login_required

# Create your views here.

# def subscribe_view(request, pk):
#     self_user = request.user
#     # other_user = get_object_or_404(User, pk=pk)
#     other_user = User.objects.get(id=pk)
#     if self_user == other_user:
#         return redirect('/')
#     if SubscribeModel.objects.filter(other_user=other_user):
#         return redirect('/')

#     m = SubscribeModel(self_user=self_user, other_user=other_user)
#     m.save()
#     return redirect('/')
@login_required(login_url='/login/')
def subscribe_view(request, *args, **kwargs): 
    if request.method == 'POST':
        self_user = request.user
        other_user = get_object_or_404(User, pk=kwargs['pk'])
        if self_user != other_user and not SubscribeModel.objects.filter(
        self_user=self_user, other_user=other_user).exists():
            s_model = SubscribeModel(self_user=self_user, other_user=other_user)
            s_model.save()
    return redirect('/')