from django_filters import rest_framework as filters
from django_celery_results.models import TaskResult, TASK_STATE_CHOICES, GroupResult


class TaskResultFilter(filters.FilterSet):
    periodic_task_name = filters.CharFilter(lookup_expr='icontains')
    task_name = filters.CharFilter(lookup_expr='icontains')
    task_args = filters.CharFilter(lookup_expr='icontains')
    task_kwargs = filters.CharFilter(lookup_expr='icontains')
    status = filters.ChoiceFilter(choices=TASK_STATE_CHOICES)
    worker = filters.CharFilter(lookup_expr='icontains')
    date_done = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = TaskResult
        fields = ['task_id']


class GroupResultFilter(filters.FilterSet):
    date_done = filters.DateTimeFromToRangeFilter()
    group_id = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = GroupResult
        fields = ['date_done', 'group_id']
