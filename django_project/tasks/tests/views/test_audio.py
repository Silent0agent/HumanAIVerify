__all__ = ()

from django.contrib import auth
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

import tasks.models
import tasks.tests.views.base.checks
import tasks.tests.views.base.tasks

User = auth.get_user_model()


def create_dummy_audio():
    return SimpleUploadedFile("test.mp3", b"\x00\x00\x00", "audio/mpeg")


class TestAudioMyTasksList(tasks.tests.views.base.tasks.BaseMyTasksListTest):
    model = tasks.models.AudioTask
    view_url = reverse("tasks:my-audio-tasks")
    template_name = "tasks/audio/my_audio_tasks.html"

    def create_task(self, client, title="Task"):
        return self.model.objects.create(
            client=client,
            title=title,
            audio=create_dummy_audio(),
        )


class TestAudioTaskCreate(tasks.tests.views.base.tasks.BaseTaskCreateViewTest):
    model = tasks.models.AudioTask
    view_url = reverse("tasks:audio-task-create")
    success_url_name = "tasks:audio-task-detail"
    template_name = "tasks/task_create.html"

    def get_valid_data(self):
        data = super().get_valid_data()
        data[self.model.audio.field.name] = create_dummy_audio()
        return data


class TestAudioTaskDetail(tasks.tests.views.base.tasks.BaseTaskDetailViewTest):
    model = tasks.models.AudioTask
    view_url_name = "tasks:audio-task-detail"
    template_name = "tasks/audio/audio_task_detail.html"

    def create_task(self, client):
        return self.model.objects.create(
            client=client,
            title="Audio Detail",
            audio=create_dummy_audio(),
        )


class TestAudioMyChecksList(
    tasks.tests.views.base.checks.BaseMyChecksListTest,
):
    model = tasks.models.AudioTaskCheck
    task_model = tasks.models.AudioTask
    view_url = reverse("tasks:my-audio-checks")
    template_name = "tasks/audio/my_audio_checks.html"

    def create_task(self, client, title="Task"):
        return self.task_model.objects.create(
            client=client,
            title=title,
            audio=create_dummy_audio(),
        )


class TestAudioCheckPerform(
    tasks.tests.views.base.checks.BaseCheckPerformViewTest,
):
    model = tasks.models.AudioTaskCheck
    task_model = tasks.models.AudioTask
    view_url_name = "tasks:audio-check-perform"
    success_url_name = "tasks:audio-check-detail"
    template_name = "tasks/audio/audio_check_perform.html"

    def create_task(self):
        return self.task_model.objects.create(
            client=self.customer,
            title="Audio Task",
            audio=create_dummy_audio(),
        )


class TestAudioCheckDetail(tasks.tests.views.base.checks.BaseCheckDetailTest):
    model = tasks.models.AudioTaskCheck
    task_model = tasks.models.AudioTask
    view_url_name = "tasks:audio-check-detail"
    template_name = "tasks/audio/check_detail.html"

    def create_task(self, client):
        return self.task_model.objects.create(
            client=client,
            title="Audio Detail",
            audio=create_dummy_audio(),
        )
