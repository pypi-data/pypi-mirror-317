from django_filters import (
    rest_framework as filters,
)

from edu_async_tasks.core.models import (
    RunningTask,
)


class RunningTasksFilter(filters.FilterSet):

    queued_at = filters.DateFilter(lookup_expr='date')
    started_at = filters.DateFilter(lookup_expr='date')
    finished_at = filters.DateFilter(lookup_expr='date')

    ordering = filters.OrderingFilter(
        fields=(
            ('inverted_queued_at', 'queued_at'),
            ('inverted_started_at', 'started_at'),
            ('name', 'name'),
            ('description', 'description'),
            ('status__title', 'status'),
            ('execution_time', 'execution_time'),
        )
    )

    class Meta:
        model = RunningTask
        fields = (
            'queued_at',
            'started_at',
            'finished_at',
            'name',
            'status',
        )
