__all__ = ()

from django.contrib import auth
from django.urls import reverse

import tasks.models
import tasks.tests.views.base.checks
import tasks.tests.views.base.tasks

User = auth.get_user_model()


class TestTextMyTasksList(tasks.tests.views.base.tasks.BaseMyTasksListTest):
    model = tasks.models.TextTask
    view_url = reverse('tasks:my-text-tasks')
    template_name = 'tasks/text/my_tasks.html'

    def create_task(self, client, title='Task'):
        return self.model.objects.create(
            client=client,
            title=title,
            content='Some text content',
        )


class TestTextTaskCreate(tasks.tests.views.base.tasks.BaseTaskCreateViewTest):
    model = tasks.models.TextTask
    view_url = reverse('tasks:text-task-create')
    success_url_name = 'tasks:text-task-detail'
    template_name = 'tasks/task_create.html'

    def get_valid_data(self):
        data = super().get_valid_data()
        data[self.model.content.field.name] = 'Some content'
        return data


class TestTextTaskDetail(tasks.tests.views.base.tasks.BaseTaskDetailViewTest):
    model = tasks.models.TextTask
    view_url_name = 'tasks:text-task-detail'
    template_name = 'tasks/text/task_detail.html'

    def create_task(self, client):
        return self.model.objects.create(
            client=client,
            title='Detail Task',
            content='Content',
        )


class TestTextMyChecksList(tasks.tests.views.base.checks.BaseMyChecksListTest):
    model = tasks.models.TextTaskCheck
    task_model = tasks.models.TextTask
    view_url = reverse('tasks:my-text-checks')
    template_name = 'tasks/text/my_checks.html'

    def create_task(self, client, title='Task'):
        return self.task_model.objects.create(
            client=client,
            title=title,
            content='Content for check',
        )


class TestTextCheckPerform(
    tasks.tests.views.base.checks.BaseCheckPerformViewTest,
):
    model = tasks.models.TextTaskCheck
    task_model = tasks.models.TextTask
    view_url_name = 'tasks:text-check-perform'
    success_url_name = 'tasks:text-check-detail'
    template_name = 'tasks/text/check_perform.html'

    def create_task(self):
        return self.task_model.objects.create(
            client=self.customer,
            title='Text Task',
            content='Original content',
        )

    def get_additional_post_data(self):
        return {
            'highlighted_content': ("Original <span class='haiv'>content</span>"),
        }

    def test_annotated_content_logic(self):
        raw_html = 'Clean <script>alert(1)</script> <b>html</b>'
        data = {
            self.model.ai_score.field.name: 10.0,
            'highlighted_content': raw_html,
            'action': 'save_draft',
        }
        self.client.post(self.url, data)

        check = self.model.objects.get(task=self.task)
        self.assertIn('Clean', check.annotated_content)
        self.assertNotIn('<script>', check.annotated_content)


class TestTextCheckDetail(tasks.tests.views.base.checks.BaseCheckDetailTest):
    model = tasks.models.TextTaskCheck
    task_model = tasks.models.TextTask
    view_url_name = 'tasks:text-check-detail'
    template_name = 'tasks/text/check_detail.html'

    def create_task(self, client):
        return self.task_model.objects.create(
            client=client,
            title='Detailed Task',
            content='Detail content',
        )
