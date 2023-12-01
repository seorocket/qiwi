"""djangoproject URL Configuration

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
from django.urls import path, include

from core.routers import router
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include((router.urls, 'core'))),
    path('create/', TaskCreateView.as_view(), name='create-task'),
    path('tasks/', task_list, name='task-list'),
    path('tasks/<int:pk>/', task_detail, name='task-detail'),
    path('tasks/<int:pk>/stop/', TaskViewSet.as_view({'post': 'stop_task'}), name='task-stop'),
    path('tasks/<int:pk>/start/', TaskViewSet.as_view({'post': 'start_task'}), name='task-start'),
    path('tasks-delete/<int:pk>/', task_delete, name='task-delete'),
    path('', home, name='home'),
]
