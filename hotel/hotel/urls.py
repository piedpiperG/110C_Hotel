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
    path('ws/', include(websocket_urlpatterns)),

    # 空调管理员
    path('init_submit/', init_submit),
    # path('monitor/', monitor),

    # 前台
    path('recp_submit/', reception),

    # 经理
    path('manager_month/', manager_month),
    path('manager_week/', manager_week),

    path('', start_all),
    path('all', start_all2)
]
