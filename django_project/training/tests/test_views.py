__all__ = ()

from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import override_settings, TestCase
from django.urls import reverse
from django.utils import timezone

import training.forms
import training.models

User = get_user_model()


class TrainingStartViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse('training:start')

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='pass',
        )
        self.client.force_login(self.user)

    def test_start_view_loads_successfully(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'training/start.html')

    def test_start_view_creates_progress_if_missing(self):
        self.client.get(self.url)

        self.assertTrue(
            training.models.UserTrainingProgress.objects.filter(
                user=self.user,
            ).exists(),
        )

    def test_start_view_context_blocked_user(self):
        training.models.UserTrainingProgress.objects.create(
            user=self.user,
            last_fail_timestamp=timezone.now(),
        )

        response = self.client.get(self.url)
        self.assertFalse(response.context['can_start'])

    def test_start_view_redirects_to_test_if_allowed(self):
        training.models.UserTrainingProgress.objects.create(user=self.user)
        text = training.models.TrainingText.objects.create(
            content='Test',
            is_ai_generated=True,
        )

        response = self.client.get(self.url)

        target_url = reverse('training:take-test', kwargs={'text_id': text.id})
        self.assertRedirects(response, target_url)

    def test_start_view_message_when_no_texts_available(self):
        training.models.UserTrainingProgress.objects.create(user=self.user)

        response = self.client.get(self.url)
        all_messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(all_messages), 1)


class TrainingTakeTestViewGetTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form_field = training.models.TrainingText.is_ai_generated.field.name

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='password',
        )
        self.client.force_login(self.user)
        self.text = training.models.TrainingText.objects.create(
            content='Content',
            is_ai_generated=True,
        )
        self.progress = training.models.UserTrainingProgress.objects.create(
            user=self.user,
        )
        self.url = reverse(
            'training:take-test',
            kwargs={'text_id': self.text.id},
        )

    def test_take_test_view_loads_successfully(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'training/take_test.html')

    def test_take_test_view_context_has_form(self):
        response = self.client.get(self.url)

        self.assertIsInstance(
            response.context['form'],
            training.forms.TrainingTextForm,
        )

    def test_take_test_not_found_if_text_does_not_exist(self):
        bad_url = reverse('training:take-test', kwargs={'text_id': 99999})
        response = self.client.get(bad_url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_take_test_redirects_if_cooldown_active(self):
        self.progress.last_fail_timestamp = timezone.now()
        self.progress.save()

        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('training:start'))

    def test_take_test_redirects_if_already_completed(self):
        self.progress.completed_texts.add(self.text)

        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('training:start'))


@override_settings(TRAINING_COMPLETIONS_FOR_PERFORMER=10)
class TrainingTakeTestViewPostTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form_field = training.models.TrainingText.is_ai_generated.field.name

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='password',
        )
        self.client.force_login(self.user)
        self.text = training.models.TrainingText.objects.create(
            content='AI Text',
            is_ai_generated=True,
        )
        self.progress = training.models.UserTrainingProgress.objects.create(
            user=self.user,
            training_score=5,
        )
        self.url = reverse(
            'training:take-test',
            kwargs={'text_id': self.text.id},
        )

    def test_post_invalid_form_status_code(self):
        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'training/take_test.html')

    def test_post_invalid_form_shows_errors(self):
        response = self.client.post(self.url, {})

        self.assertTrue(response.context['form'].errors)

    def test_post_correct_answer_redirects_to_start(self):
        response = self.client.post(self.url, {self.form_field: 'True'})

        self.assertRedirects(response, reverse('training:start'))

    def test_post_correct_answer_increments_score(self):
        initial_score = self.progress.training_score

        self.client.post(self.url, {self.form_field: 'True'})

        self.progress.refresh_from_db()
        self.assertEqual(self.progress.training_score, initial_score + 1)

    def test_post_correct_answer_clears_fail_timestamp(self):
        self.progress.last_fail_timestamp = timezone.now()
        self.progress.save()

        self.client.post(self.url, {self.form_field: 'True'})

        self.progress.refresh_from_db()
        self.assertIsNone(self.progress.last_fail_timestamp)

    def test_post_wrong_answer_redirects_to_start(self):
        response = self.client.post(self.url, {self.form_field: 'False'})

        self.assertRedirects(response, reverse('training:start'))

    def test_post_wrong_answer_decrements_score(self):
        initial_score = self.progress.training_score

        self.client.post(self.url, {self.form_field: 'False'})

        self.progress.refresh_from_db()
        self.assertEqual(self.progress.training_score, initial_score - 2)

    def test_post_wrong_answer_sets_fail_timestamp(self):
        self.client.post(self.url, {self.form_field: 'False'})

        self.progress.refresh_from_db()
        self.assertIsNotNone(self.progress.last_fail_timestamp)


class TrainingPerformerPromotionTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form_field = training.models.TrainingText.is_ai_generated.field.name

    def setUp(self):
        self.user = User.objects.create_user(
            username='pro_user',
            email='testuser@email.com',
            password='password',
        )
        self.client.force_login(self.user)
        self.text = training.models.TrainingText.objects.create(
            content='Content',
            is_ai_generated=True,
        )
        self.url = reverse(
            'training:take-test',
            kwargs={'text_id': self.text.id},
        )

        self.threshold = settings.TRAINING_COMPLETIONS_FOR_PERFORMER
        self.progress = training.models.UserTrainingProgress.objects.create(
            user=self.user,
            training_score=self.threshold - 1,
        )

    def test_promotion_redirects_to_results(self):
        response = self.client.post(self.url, {self.form_field: 'True'})

        self.assertRedirects(response, reverse('training:results'))

    def test_promotion_adds_user_to_group(self):
        self.client.post(self.url, {self.form_field: 'True'})

        self.assertTrue(
            self.user.groups.filter(
                name=settings.PERFORMER_GROUP_NAME,
            ).exists(),
        )


class TrainingResultsViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse('training:results')

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='password',
        )
        self.client.force_login(self.user)

    def test_results_view_loads_successfully(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'training/results.html')

    def test_results_view_creates_progress_if_missing(self):
        self.client.get(self.url)

        self.assertTrue(
            training.models.UserTrainingProgress.objects.filter(
                user=self.user,
            ).exists(),
        )

    def test_results_view_context_counts(self):
        text1 = training.models.TrainingText.objects.create(
            content='1',
            is_ai_generated=True,
        )
        training.models.TrainingText.objects.create(
            content='2',
            is_ai_generated=False,
        )

        progress = training.models.UserTrainingProgress.objects.create(
            user=self.user,
        )
        progress.completed_texts.add(text1)

        response = self.client.get(self.url)

        self.assertEqual(response.context['completed_count'], 1)
        self.assertEqual(response.context['total_texts'], 2)
