__all__ = ()

from django.contrib import auth
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
from django.test import TestCase

from tasks.models import TaskCheck, TextTask

User = auth.get_user_model()


class TextTaskModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_user = User.objects.create_user(
            username="client",
            password="password",
            email="example1@email.com",
        )
        cls.performer_user = User.objects.create_user(
            username="performer",
            password="password",
            email="example2@email.com",
        )
        cls.task_title = "Test Task Title"

    def setUp(self):
        self.task = TextTask.objects.create(
            client=self.client_user,
            title=self.task_title,
            content="Some content",
        )

    def test_task_timestamps(self):
        self.assertIsNotNone(self.task.created_at)
        self.assertIsNotNone(self.task.updated_at)

    def test_task_str(self):
        self.assertEqual(str(self.task), self.task_title)

    def test_ai_score_none(self):
        self.assertIsNone(self.task.ai_score)

    def test_ai_score_calculation(self):
        TaskCheck.objects.create(
            task=self.task,
            performer=self.performer_user,
            ai_score=50.0,
        )
        performer_2 = User.objects.create_user(
            username="performer2",
            email="example3@email.com",
        )
        TaskCheck.objects.create(
            task=self.task,
            performer=performer_2,
            ai_score=100.0,
        )

        self.assertAlmostEqual(self.task.ai_score, 75.0)

    def test_ordering_by_created_at_field(self):
        task_2 = TextTask.objects.create(
            client=self.client_user,
            title="Newer Task",
            content="Content",
        )
        tasks = TextTask.objects.all()
        self.assertEqual(tasks[0], task_2)
        self.assertEqual(tasks[1], self.task)

    def test_on_delete_client_protect(self):
        client_user_2 = User.objects.create_user(
            username="client_2",
            password="password",
            email="example3@email.com",
        )
        TextTask.objects.create(
            client=client_user_2,
            title=self.task_title,
            content="Some content",
        )
        self.assertEqual(User.objects.count(), 3)
        with self.assertRaises(ProtectedError):
            client_user_2.delete()

        self.assertEqual(User.objects.count(), 3)


class TaskCheckModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_user = User.objects.create_user(
            username="client",
            password="password",
            email="example1@email.com",
        )
        cls.performer_user = User.objects.create_user(
            username="performer",
            password="password",
            email="example2@email.com",
        )
        cls.task = TextTask.objects.create(
            client=cls.client_user,
            title="Task",
            content="Content",
        )
        cls.check_ai_score = 85.5

    def setUp(self):
        self.check = TaskCheck.objects.create(
            task=self.task,
            performer=self.performer_user,
            ai_score=self.check_ai_score,
            comment="Looks like AI",
        )

    def test_task_timestamps(self):
        self.assertIsNotNone(self.task.created_at)
        self.assertIsNotNone(self.task.updated_at)

    def test_check_default_status_draft(self):
        self.assertEqual(self.check.status, TaskCheck.Status.DRAFT)

    def test_check_str(self):
        self.assertEqual(
            str(self.check),
            f"{self.task.title} | {self.performer_user.username} "
            f"({self.check_ai_score}%)",
        )

    def test_ai_score_validators_min(self):
        self.check.ai_score = -0.1
        with self.assertRaises(ValidationError):
            self.check.full_clean()

    def test_ai_score_validators_max(self):
        self.check.ai_score = 100.1
        with self.assertRaises(ValidationError):
            self.check.full_clean()

    def test_unique_constraint_task_and_performer(self):
        with self.assertRaises(IntegrityError):
            TaskCheck.objects.create(
                task=self.task,
                performer=self.performer_user,
                ai_score=10.0,
            )

    def test_switch_status_to_published(self):
        self.check.status = TaskCheck.Status.PUBLISHED
        self.check.full_clean()
        self.check.save()
        self.assertEqual(self.check.status, "published")

    def test_invalid_status(self):
        self.check.status = "invalid_status"
        with self.assertRaises(ValidationError):
            self.check.full_clean()

    def test_ordering_by_created_at_field(self):
        performer_user_2 = User.objects.create_user(
            username="performer_2",
            password="password",
            email="example3@email.com",
        )
        check_2 = TaskCheck.objects.create(
            task=self.task,
            performer=performer_user_2,
            ai_score=35.0,
            comment="Looks like human",
        )
        checks = TaskCheck.objects.all()
        self.assertEqual(checks[0], check_2)
        self.assertEqual(checks[1], self.check)

    def test_on_delete_task_cascade(self):
        task_2 = TextTask.objects.create(
            client=self.client_user,
            title="Task 2",
            content="Content 2",
        )
        TaskCheck.objects.create(
            task=task_2,
            performer=self.performer_user,
            ai_score=35.0,
            comment="Looks like human",
        )
        self.assertEqual(TaskCheck.objects.count(), 2)
        task_2.delete()
        self.assertEqual(TaskCheck.objects.count(), 1)

    def test_on_delete_performer_protect(self):
        performer_user_2 = User.objects.create_user(
            username="performer_2",
            password="password",
            email="example3@email.com",
        )
        TaskCheck.objects.create(
            task=self.task,
            performer=performer_user_2,
            ai_score=35.0,
            comment="Looks like human",
        )
        self.assertEqual(User.objects.count(), 3)
        with self.assertRaises(ProtectedError):
            performer_user_2.delete()

        self.assertEqual(User.objects.count(), 3)
