"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import logout_view, register_view, login_view, profile_view
from chat.views import index_view, send_view
from subscribers.views import subscribe_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', logout_view, name="logout"),
    path('registration/', register_view, name='registration'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('send/', send_view, name='send-message'),
    path('', index_view, name='index'),
    path('subscribe/<int:pk>/', subscribe_view, name='subscribe')
]
