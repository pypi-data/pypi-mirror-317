from django.contrib import admin
from rest_framework import serializers
from django_celery_results.models import TaskResult, TASK_STATE_CHOICES, GroupResult
from django_celery_results.admin import TaskResultAdmin


class TaskResultSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=TASK_STATE_CHOICES)

    class Meta:
        model = TaskResult
        fields = '__all__'
        read_only_fields = TaskResultAdmin(TaskResult, admin_site=admin.site).get_readonly_fields(None)


class TaskResultListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ['id', 'task_id', 'periodic_task_name', 'task_name', 'date_done', 'status', 'worker']


class GroupResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupResult
        fields = '__all__'
        read_only_fields = ['date_created', 'date_done', 'result']


class GroupResultListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupResult
        fields = ['id', 'group_id', 'date_done']
