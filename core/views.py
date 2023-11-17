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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        formatted_data = []
        for task_data in serializer.data:
            formatted_data.append({
                "wallet_number": task_data['qiwi_wallet'],
                "password": task_data['qiwi_pass'],
                "amount": task_data['amount'],
                "phones": task_data['phones'].split(','),
            })

        return Response(formatted_data)

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

            # Возвращаем ответ с данными созданной задачи
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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
