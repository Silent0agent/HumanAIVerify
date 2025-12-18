__all__ = ()

from http import HTTPStatus

from django.contrib import auth
from django.urls import reverse

from tasks.tests.views.base.base import BaseViewTest

User = auth.get_user_model()


class BaseMyChecksListTest(BaseViewTest):
    model = None
    view_url = None
    template_name = None

    def create_task(self, client, title="Task"):
        raise NotImplementedError

    def create_check(self, task, performer, status):
        return self.model.objects.create(
            task=task,
            performer=performer,
            status=status,
            ai_score=50.0,
        )

    def setUp(self):
        self.client.force_login(self.performer)

    def test_get_status_code_ok(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_template_used(self):
        response = self.client.get(self.view_url)
        self.assertTemplateUsed(response, self.template_name)

    def test_context_data_structure(self):
        response = self.client.get(self.view_url)
        self.assertIn("checks", response.context)
        self.assertIn("available_tasks", response.context)

    def test_list_contains_my_checks(self):
        task = self.create_task(self.customer, "Checked Task")
        check = self.create_check(
            task,
            self.performer,
            self.model.Status.PUBLISHED,
        )
        response = self.client.get(self.view_url)

        checks_ids = [check.id for check in response.context["checks"]]
        self.assertIn(check.id, checks_ids)

    def test_list_does_not_contain_others_checks(self):
        other_performer = User.objects.create_user(
            username="performer2",
            email="performer2@email.com",
            password="pass",
            role=User.Role.PERFORMER,
        )
        task = self.create_task(self.customer, "Other Checked Task")
        check = self.create_check(
            task,
            other_performer,
            self.model.Status.PUBLISHED,
        )

        response = self.client.get(self.view_url)

        checks_ids = [check.id for check in response.context["checks"]]
        self.assertNotIn(check.id, checks_ids)

    def test_available_tasks_logic(self):
        checked_task = self.create_task(self.customer, title="Done")
        self.create_check(
            checked_task,
            self.performer,
            self.model.Status.PUBLISHED,
        )
        available_task = self.create_task(self.customer, title="Available")
        response = self.client.get(self.view_url)

        available_ids = [
            task.id for task in response.context["available_tasks"]
        ]
        self.assertIn(available_task.id, available_ids)
        self.assertNotIn(checked_task.id, available_ids)

    def test_anonymous_access_redirects(self):
        self.client.logout()
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_customer_access_redirects(self):
        self.client.logout()
        self.client.force_login(self.customer)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


class BaseCheckPerformViewTest(BaseViewTest):
    model = None
    view_url_name = None
    template_name = None

    def create_task(self):
        raise NotImplementedError

    def setUp(self):
        self.customer.refresh_from_db()
        self.task = self.create_task()
        self.url = reverse(
            self.view_url_name,
            kwargs={"task_id": self.task.pk},
        )
        self.client.force_login(self.performer)

    def get_additional_post_data(self):
        return {}

    def test_get_status_code_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.template_name)

    def test_task_in_context(self):
        response = self.client.get(self.url)

        self.assertIn("task", response.context)
        self.assertEqual(response.context["task"], self.task)

    def test_post_draft_status_code_ok(self):
        data = {
            self.model.ai_score.field.name: 50.0,
            "action": "save_draft",
        }
        data.update(self.get_additional_post_data())
        response = self.client.post(self.url, data, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_draft_object_saved(self):
        check_comment = "Draft comment"
        data = {
            self.model.ai_score.field.name: 75.0,
            self.model.comment.field.name: check_comment,
            "action": "save_draft",
        }
        data.update(self.get_additional_post_data())
        self.client.post(self.url, data, follow=True)

        check = self.model.objects.get(
            task=self.task,
            performer=self.performer,
        )
        self.assertEqual(check.status, self.model.Status.DRAFT)
        self.assertEqual(check.ai_score, 75.0)
        self.assertEqual(check.comment, check_comment)

    def test_post_publish_status_code_ok(self):
        data = {
            self.model.ai_score.field.name: 80.0,
            "action": "publish",
        }
        data.update(self.get_additional_post_data())
        response = self.client.post(self.url, data, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_publish_object_saved(self):
        check_comment = "Publish comment"
        data = {
            self.model.ai_score.field.name: 20.0,
            self.model.comment.field.name: check_comment,
            "action": "publish",
        }
        data.update(self.get_additional_post_data())
        self.client.post(self.url, data, follow=True)

        check = self.model.objects.get(
            task=self.task,
            performer=self.performer,
        )
        self.assertEqual(check.ai_score, 20.0)
        self.assertEqual(check.status, self.model.Status.PUBLISHED)
        self.assertEqual(check.comment, check_comment)

    def test_post_valid_redirects_to_detail_view(self):
        data = {
            self.model.ai_score.field.name: 20.0,
            "action": "publish",
        }
        data.update(self.get_additional_post_data())
        response = self.client.post(self.url, data, follow=True)

        check = self.model.objects.get(
            task=self.task,
            performer=self.performer,
        )
        self.assertRedirects(
            response,
            reverse(self.success_url_name, kwargs={"check_id": check.id}),
        )

    def test_user_cant_check_his_task(self):
        self.client.logout()
        user_performer = User.objects.create_user(
            username="temp_perf",
            email="new_performer@email.com",
            password="pwd",
            role=User.Role.PERFORMER,
        )
        self.task.client = user_performer
        self.task.save()

        self.client.force_login(user_performer)

        data = {
            self.model.ai_score.field.name: 20.0,
            "action": "publish",
        }
        data.update(self.get_additional_post_data())

        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class BaseCheckDetailTest(BaseViewTest):
    model = None
    view_url_name = None
    template_name = None

    def create_task(self, client):
        raise NotImplementedError

    def create_check(self, task, performer):
        return self.model.objects.create(
            task=task,
            performer=performer,
            status=self.model.Status.PUBLISHED,
            ai_score=88.0,
            comment="Good job",
        )

    def setUp(self):
        self.task = self.create_task(self.customer)
        self.check = self.create_check(self.task, self.performer)
        self.url = reverse(
            self.view_url_name,
            kwargs={"check_id": self.check.id},
        )

    def test_customer_can_view_his_task_check(self):
        self.client.force_login(self.customer)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["check"], self.check)

    def test_performer_can_view_his_own_check(self):
        self.client.force_login(self.performer)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["check"], self.check)

    def test_anonymous_access_redirects(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_other_customer_cannot_view(self):
        other_customer = User.objects.create_user(
            username="customer2",
            email="customer2@email.com",
            password="pass",
            role=User.Role.CUSTOMER,
        )
        self.client.force_login(other_customer)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_other_performer_cannot_view(self):
        other_perf = User.objects.create_user(
            username="performer2",
            email="performer2@email.com",
            role=User.Role.PERFORMER,
            password="pass",
        )
        self.client.force_login(other_perf)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_template_used(self):
        self.client.force_login(self.customer)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.template_name)
