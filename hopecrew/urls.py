import django.contrib.auth

from chat import views
"""hopecrew URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('contact', views.contact, name="contact"),
    path('accounts/register', views.register, name="register"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('success', views.thanks, name="thanks"),
    #path('profile', views.profile, name="profile"),
    #path('profile/edit', views.profile_edit, name="profile_edit"),
    path('chat', views.chat, name="chat"),
    path('chat/api/log', views.chat, name="chat_api_log"),
    path('chat/api/new', views.api_new, name="chat_api_new"),
    path('chat/api/edit', views.api_edit, name="chat_api_edit"),
]
