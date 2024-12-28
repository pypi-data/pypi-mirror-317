from datetime import (
    timedelta,
)
from itertools import (
    chain,
)
from operator import (
    attrgetter,
)
from uuid import (
    uuid4,
)

from django.urls.base import (
    reverse,
)
from django.utils import (
    timezone,
)
from rest_framework import (
    status,
)
from rest_framework.test import (
    APITestCase,
)

from edu_async_tasks.core.models import (
    AsyncTaskStatus,
    AsyncTaskType,
    RunningTask,
)


class RunningTaskViewsetTestCase(APITestCase):

    def setUp(self) -> None:
        self.list_url = reverse('async-tasks-list')

        self.task_types = AsyncTaskType.get_model_enum_values()
        self.task_statuses = sorted(AsyncTaskStatus.get_model_enum_values(), key=attrgetter('title'))

        time_now = timezone.now()

        # задачи для проверки сортировки по основным полям
        self.task_1 = RunningTask(
            id=uuid4(),
            name=f'edu_async_tasks.core.tasks.Foo00',
            task_type_id=self.task_types[0].key,
            queued_at=time_now,
            started_at=time_now - timedelta(seconds=9),
            finished_at=time_now - timedelta(seconds=5),
            status_id=AsyncTaskStatus.PENDING.key,
            description='АААААААААааааааааааААААААААААааааа',
        )
        self.task_2 = RunningTask(
            id=uuid4(),
            name=f'edu_async_tasks.core.tasks.Foo01',
            queued_at=time_now - timedelta(seconds=10),
            started_at=time_now + timedelta(seconds=11),
            task_type_id=self.task_types[1].key,
            finished_at=time_now + timedelta(seconds=5),
            status_id=AsyncTaskStatus.RECEIVED.key,
            description='В',
        )
        self.task_3 = RunningTask(
            id=uuid4(),
            name=f'edu_async_tasks.core.tasks.Foo02',
            task_type_id=self.task_types[2].key,
            queued_at=time_now + timedelta(seconds=10),
            started_at=time_now + timedelta(seconds=1),
            finished_at=time_now + timedelta(seconds=15),
            status_id=AsyncTaskStatus.STARTED.key,
            description='Б',
        )

        self.tasks = [
            self.task_1,
            self.task_2,
            self.task_3,
        ]

        # задачи для проверки сортировки по статусам
        self.other_day_tasks = []
        for idx, task_status in enumerate(self.task_statuses[3:], start=3):
            task = RunningTask(
                id=uuid4(),
                name=f'edu_async_tasks.core.tasks.Foo{idx:02d}',
                task_type_id=self.task_types[idx].key,
                description=f'Задача номер {idx:02d}',
                status_id=task_status.key,
                queued_at=timezone.now() + timedelta(days=1, seconds=idx),
                started_at=time_now + timedelta(days=1, seconds=idx + 1),
                options=None,
            )
            setattr(self, f'task_{idx + 1}', task)
            self.other_day_tasks.append(task)

        self.tasks = RunningTask.objects.bulk_create(chain(self.tasks, self.other_day_tasks))

    def test_list(self) -> None:
        response = self.client.get(self.list_url)
        task = self.tasks[0]

        expected_result = self.client.get(reverse('async-tasks-detail', args=[task.id])).json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for field in ('count', 'next', 'previous', 'results'):
            with self.subTest(field=field):
                self.assertIn(field, response.data)

        results = response.json()['results']

        self.assertEqual(len(results), len(self.tasks))

        # проверяем сортировку по-умолчанию
        self.assertEqual(
            tuple(str(i.id) for i in (*reversed(self.other_day_tasks), self.task_3, self.task_1, self.task_2)),
            tuple(t['id'] for t in results),
        )

        # Проверяем, что expected_result содержится в результатах
        self.assertIn(expected_result, results)

    def test_list_ordering(self):
        sub_tests = (
            ('queued_at', (*reversed(self.other_day_tasks), self.task_3, self.task_1, self.task_2)),
            ('started_at', (*reversed(self.other_day_tasks), self.task_2, self.task_3, self.task_1)),
            ('status', (self.task_1, self.task_2, self.task_3, *self.other_day_tasks)),
            ('description', (self.task_1, self.task_3, self.task_2, *self.other_day_tasks)),
        )
        for ordering_field, expected_asc_order in sub_tests:
            with self.subTest(ordering_field):
                response_asc = self.client.get(self.list_url, {'ordering': ordering_field})
                response_desc = self.client.get(self.list_url, {'ordering': f'-{ordering_field}'})

                self.assertEqual(response_asc.status_code, status.HTTP_200_OK)
                self.assertEqual(response_desc.status_code, status.HTTP_200_OK)

                results_asc = response_asc.json()['results']
                results_desc = response_desc.json()['results']

                # проверяем правильность сортировки
                self.assertEqual(
                    tuple(str(i.id) for i in expected_asc_order),
                    tuple(t['id'] for t in results_asc),
                )
                # проверяем что набор записей не отличается, отличается только порядок
                self.assertListEqual(results_asc, list(reversed(results_desc)))

    def test_list_filtering(self):
        subtests = (
            (
                'queued_at:  дата постановки в очередь задачи первого дня',
                {'queued_at': self.task_1.queued_at.date()},
                (self.task_3, self.task_1, self.task_2)
            ),
            (
                'queued_at: дата постановки в очередь задач второго дня',
                {'queued_at': self.other_day_tasks[0].queued_at.date()},
                tuple(reversed(self.other_day_tasks))
            ),
            ('name', {'name': self.task_1.name}, (self.task_1,)),
            ('status', {'status': self.task_1.status.key}, (self.task_1,)),
            ("search: description", {'search': 'ааааааа'}, (self.task_1,)),
            ("search: status title", {'search': 'выполн'}, (self.task_10, self.task_3)),
            ("search: status key", {'search': 'pend'}, (self.task_1,)),
            ("search: date", {'search': self.task_1.queued_at.date()}, (self.task_3, self.task_1, self.task_2)),
            ("search: name", {'search': 'Foo00'}, (self.task_1,)),
        )

        for name, filter_params, expected_tasks in subtests:
            with self.subTest(name=name):
                response = self.client.get(self.list_url, filter_params)
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                results = response.json()['results']

                # проверяем правильность фильтрации
                self.assertEqual(
                    tuple(str(i.id) for i in expected_tasks),
                    tuple(t['id'] for t in results),
                )
