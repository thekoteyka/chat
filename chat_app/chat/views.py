from django.shortcuts import render
from .forms import ChatForm
from .models import ChatModel
from subscribers.models import SubscribeModel
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def index_view(request, *args, **kwargs):
    chatform = ChatForm(request.POST or None)
    filters = request.GET.get('filter', None)
    is_subscribers = request.GET.get('sub', False)
    # if is_subscribers and filters:
    #     subscribers = SubscribeModel.objects.filter(self_user=request.user)
    #     messages = ChatModel.objects.filter(user=filters)
    #     subs = []
    #     obj = []

    #     for i in subscribers:
    #         subs.append(i.other_user)
    
    #     for message in messages:
    #         if message.user in subs:
    #             obj.append(message)

    # elif filters:
    #     obj = ChatModel.objects.filter(user=filters)

    # elif is_subscribers:
    #     subscribers = SubscribeModel.objects.filter(self_user=request.user)
    #     messages = ChatModel.objects.all()
    #     subs = []
    #     obj = []

    #     for i in subscribers:
    #         subs.append(i.other_user)
    
    #     for message in messages:
    #         if message.user in subs:
    #             obj.append(message)

    # else:
    #     obj = ChatModel.objects.all()
    # print(filters)
    # print(obj)

    only_subs = SubscribeModel.objects.filter(self_user__id=request.user.pk)
    obj = ChatModel.objects.filter(user__id=filters) or ChatModel.objects.all()

    if is_subscribers:
        obj=obj.filter(user_id__in=[user.other_user.id for user in only_subs])


    return render(request, 'index.html', {'form': chatform, 'obj': obj})

@login_required(login_url='/login/')
def send_view(request, *args, **kwargs):
    chatform = ChatForm(request.POST)
    if chatform.is_valid():
        user = request.user
        text = chatform.cleaned_data.get('text')
        message = ChatModel(user=user, text=text)
        message.save()
    # return redirect('/')
    return HttpResponseRedirect(reverse('index'))
