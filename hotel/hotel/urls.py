"""
URL configuration for hotel project.

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

from django.contrib import admin
from django.urls import include, path
from Air_Condition.views import *
from hotel.routing import application
from django.urls import re_path

from django.contrib import admin
from django.urls import path, include
from hotel.routing import websocket_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('socket/', websocket_view),  # 替换 'your_app' 为你的应用名
    path('ws/', include(websocket_urlpatterns)),
]
