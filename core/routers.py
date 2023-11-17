from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'tasklogs', TaskLogViewSet, basename='tasklog')

urlpatterns = [
    path('', include(router.urls)),
    # Добавь другие маршруты, если необходимо
]