import django_filters
from django_filters import rest_framework as filters
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .forms import TaskForm


class UserFilter(filters.FilterSet):
    username = django_filters.CharFilter(field_name="username")

    class Meta:
        model = User
        fields = ['username']

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_class = UserFilter

    def get_queryset(self):
        return User.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return redirect('task-list')

    @action(detail=True, methods=['post'])
    def start_task(self, request, pk=None):
        task = self.get_object()
        task.status = 4
        task.save()
        return redirect('task-list')

    @action(detail=True, methods=['post'])
    def stop_task(self, request, pk=None):
        task = self.get_object()
        task.status = 0
        task.save()
        return redirect('task-list')

    @action(detail=False, methods=['get'], url_path='get-and-start-task')
    def get_and_start_task(self, request, *args, **kwargs):
        task_instance = Task.objects.filter(status=4).order_by('id').first()
        if task_instance:
            serializer = self.get_serializer(task_instance)
            task_instance.status = 2
            task_instance.save()
            return Response(serializer.data)
        else:
            return Response({'detail': 'No task with status 4 found.'}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=False, methods=['get'], url_path='get-and-update-task')
    def get_and_update_task(self, request, *args, **kwargs):
        task_instance = Task.objects.filter(status=1).order_by('id').first()
        if task_instance:
            serializer = self.get_serializer(task_instance)
            task_instance.status = 2
            task_instance.save()
            return Response(serializer.data)
        else:
            return Response({'detail': 'No task with status 0 found.'}, status=status.HTTP_404_NOT_FOUND)

def task_delete(request, pk):
    item = get_object_or_404(Task, id=pk)
    item.delete()
    return redirect('task-list')


class TaskCreateView(APIView):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, 'task_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.data)
        if form.is_valid():
            # Создаем новый объект Task
            task = Task.objects.create(
                qiwi_wallet=form.cleaned_data['qiwi_wallet'],
                qiwi_pass=form.cleaned_data['qiwi_pass'],
                phones=form.cleaned_data['phones'],
                amount=form.cleaned_data['amount']
            )

            # После сохранения задачи, выполните редирект на task_list
            return redirect('task-list')  # Замените 'task-list' на ваш фактический URL-путь

        return render(request, 'task_create.html', {'form': form})


def task_list(request):
    tasks = Task.objects.all()

    # Добавляем пагинацию
    paginator = Paginator(tasks, 100)
    page = request.GET.get('page')

    try:
        tasks_page = paginator.page(page)
    except PageNotAnInteger:
        tasks_page = paginator.page(1)
    except EmptyPage:
        tasks_page = paginator.page(paginator.num_pages)

    return render(request, 'task_list.html', {'tasks': tasks_page})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    logs = TaskLog.objects.filter(task=task)
    return render(request, 'task_detail.html', {'task': task, 'logs': logs})

def home(request):
    return render(request, 'home.html')

class TaskLogViewSet(viewsets.ModelViewSet):
    queryset = TaskLog.objects.all()
    serializer_class = TaskLogSerializer