__all__ = ()

from io import BytesIO

from django.contrib import auth
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image

import tasks.models
import tasks.tests.views.base.checks
import tasks.tests.views.base.tasks

User = auth.get_user_model()


def create_dummy_image():
    output = BytesIO()
    img = Image.new("RGB", (50, 50), color="red")
    img.save(output, format="JPEG")
    output.seek(0)
    return SimpleUploadedFile("test.jpg", output.read(), "image/jpeg")


class TestImageMyTasksList(tasks.tests.views.base.tasks.BaseMyTasksListTest):
    model = tasks.models.ImageTask
    view_url = reverse("tasks:my-image-tasks")
    template_name = "tasks/image/my_image_tasks.html"

    def create_task(self, client, title="Task"):
        return self.model.objects.create(
            client=client,
            title=title,
            image=create_dummy_image(),
        )


class TestImageTaskCreate(tasks.tests.views.base.tasks.BaseTaskCreateViewTest):
    model = tasks.models.ImageTask
    view_url = reverse("tasks:image-task-create")
    success_url_name = "tasks:image-task-detail"
    template_name = "tasks/task_create.html"

    def get_valid_data(self):
        data = super().get_valid_data()
        data[self.model.image.field.name] = create_dummy_image()
        return data


class TestImageTaskDetail(tasks.tests.views.base.tasks.BaseTaskDetailViewTest):
    model = tasks.models.ImageTask
    view_url_name = "tasks:image-task-detail"
    template_name = "tasks/image/image_task_detail.html"

    def create_task(self, client):
        return self.model.objects.create(
            client=client,
            title="Img Detail",
            image=create_dummy_image(),
        )


class TestImageMyChecksListtasks(
    tasks.tests.views.base.checks.BaseMyChecksListTest,
):
    model = tasks.models.ImageTaskCheck
    task_model = tasks.models.ImageTask
    view_url = reverse("tasks:my-image-checks")
    template_name = "tasks/image/my_image_checks.html"

    def create_task(self, client, title="Task"):
        return self.task_model.objects.create(
            client=client,
            title=title,
            image=create_dummy_image(),
        )


class TestImageCheckPerform(
    tasks.tests.views.base.checks.BaseCheckPerformViewTest,
):
    model = tasks.models.ImageTaskCheck
    task_model = tasks.models.ImageTask
    view_url_name = "tasks:image-check-perform"
    success_url_name = "tasks:image-check-detail"
    template_name = "tasks/image/image_check_perform.html"

    def create_task(self):
        return self.task_model.objects.create(
            client=self.customer,
            title="Img Task",
            image=create_dummy_image(),
        )


class TestImageCheckDetail(tasks.tests.views.base.checks.BaseCheckDetailTest):
    model = tasks.models.ImageTaskCheck
    task_model = tasks.models.ImageTask
    view_url_name = "tasks:image-check-detail"
    template_name = "tasks/image/check_detail.html"

    def create_task(self, client):
        return self.task_model.objects.create(
            client=client,
            title="Image Detail",
            image=create_dummy_image(),
        )
