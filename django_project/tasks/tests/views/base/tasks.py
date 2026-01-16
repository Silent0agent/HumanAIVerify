__all__ = ()

from http import HTTPStatus

from django.contrib import auth
from django.urls import reverse

from tasks.tests.views.base.base import BaseViewTest

User = auth.get_user_model()


class BaseMyTasksListTest(BaseViewTest):
    view_url = None
    template_name = None

    def create_task(self, client, title='Task title'):
        raise NotImplementedError

    def setUp(self):
        self.client.force_login(self.customer)

    def test_get_status_code_ok(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_template_used(self):
        response = self.client.get(self.view_url)
        self.assertTemplateUsed(response, self.template_name)

    def test_context_object_name(self):
        response = self.client.get(self.view_url)
        self.assertIn('tasks', response.context)

    def test_list_contains_my_tasks(self):
        task1 = self.create_task(self.customer, title='My Task 1')
        task2 = self.create_task(self.customer, title='My Task 2')

        response = self.client.get(self.view_url)

        self.assertIn(task1, response.context['tasks'])
        self.assertIn(task2, response.context['tasks'])

    def test_list_does_not_contain_others_tasks(self):
        other_user = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='pass',
        )
        other_task = self.create_task(other_user, title='Other Task')
        response = self.client.get(self.view_url)

        self.assertNotIn(other_task, response.context['tasks'])

    def test_anonymous_access_redirects(self):
        self.client.logout()
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_performer_access_redirects(self):
        self.client.logout()
        self.client.force_login(self.performer)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


class BaseTaskCreateViewTest(BaseViewTest):
    model = None
    view_url = None
    success_url_name = None
    template_name = None

    def setUp(self):
        self.client.force_login(self.customer)

    def get_valid_data(self):
        self.task_title = 'Test Task'
        self.task_description = 'Description'
        return {
            self.model.title.field.name: self.task_title,
            self.model.description.field.name: self.task_description,
        }

    def test_get_status_code_ok(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_template_used(self):
        response = self.client.get(self.view_url)
        self.assertTemplateUsed(response, self.template_name)

    def test_form_in_context(self):
        response = self.client.get(self.view_url)
        self.assertIn('form', response.context)

    def test_post_valid_status_code_ok(self):
        data = self.get_valid_data()
        response = self.client.post(self.view_url, data, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_valid_creates_object(self):
        data = self.get_valid_data()
        self.client.post(self.view_url, data, follow=True)
        self.assertTrue(
            self.model.objects.filter(title=self.task_title).exists(),
        )

        task = self.model.objects.get(title=self.task_title)
        self.assertEqual(task.client, self.customer)

    def test_post_valid_redirects_to_detail_view(self):
        data = self.get_valid_data()
        response = self.client.post(self.view_url, data, follow=True)
        task = self.model.objects.get(title=self.task_title)

        self.assertRedirects(
            response,
            reverse(self.success_url_name, kwargs={'task_id': task.pk}),
        )

    def test_post_invalid_status_code_ok(self):
        data = self.get_valid_data()
        del data[self.model.title.field.name]

        response = self.client.post(self.view_url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_invalid_does_not_create_object(self):
        initial_objects_count = self.model.objects.count()
        data = self.get_valid_data()
        del data[self.model.title.field.name]

        self.client.post(self.view_url, data)
        self.assertEqual(initial_objects_count, self.model.objects.count())

    def test_anonymous_access_denied(self):
        self.client.logout()

        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_performer_access_denied(self):
        self.client.logout()
        self.client.force_login(self.performer)

        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


class BaseTaskDetailViewTest(BaseViewTest):
    view_url_name = None
    template_name = None

    def create_task(self, client):
        raise NotImplementedError

    def setUp(self):
        super().setUp()
        self.task = self.create_task(self.customer)
        self.url = reverse(
            self.view_url_name,
            kwargs={'task_id': self.task.pk},
        )
        self.client.force_login(self.customer)

    def test_get_status_code_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.template_name)

    def test_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['task'], self.task)

    def test_other_user_cannot_see_detail(self):
        self.client.logout()
        other_user = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='pass',
        )
        self.client.force_login(other_user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
