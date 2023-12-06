"""
URL configuration for djangoProject2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from Air_Condition.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('guest/', guest_init),
    path('', guest_init),
    path('2', guest2_init),
    path('3', guest3_init),
    path('4', guest4_init),
    path('5', guest5_init),

    path('increase_temperature/', increase_temperature),
    path('click_data/', click_data),
]
urlpatterns += staticfiles_urlpatterns()
