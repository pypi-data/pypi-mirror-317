from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from django_celery_results.models import TaskResult, GroupResult

from .serializers import (
    TaskResultSerializer, TaskResultListSerializer, GroupResultSerializer, GroupResultListSerializer
)
from .filters import TaskResultFilter, GroupResultFilter


class TaskResultViewSet(viewsets.ModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = TaskResultFilter
    ordering_fields = ['id']

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskResultListSerializer
        else:
            return TaskResultSerializer


class GroupResultViewSet(viewsets.ModelViewSet):
    queryset = GroupResult.objects.all()
    serializer_class = GroupResultSerializer
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = GroupResultFilter
    ordering_fields = ['id']

    def get_serializer_class(self):
        if self.action == 'list':
            return GroupResultListSerializer
        else:
            return GroupResultSerializer
