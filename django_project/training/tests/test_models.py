__all__ = ()

import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import override_settings, TestCase
from django.utils import timezone
from parameterized import parameterized

from training.models import TrainingText, UserTrainingProgress

User = get_user_model()


class TrainingTextModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.text = TrainingText.objects.create(
            content='A' * 100,
            is_ai_generated=True,
            difficulty=TrainingText.Difficulty.MEDIUM,
        )

    def test_str_representation_truncates_content(self):
        expected_str = 'A' * 29 + '…'
        self.assertEqual(str(self.text), expected_str)

    def test_default_difficulty(self):
        text = TrainingText.objects.create(
            content='Short',
            is_ai_generated=False,
        )
        self.assertEqual(text.difficulty, TrainingText.Difficulty.MEDIUM)

    def test_ordering_by_difficulty(self):
        text1 = TrainingText.objects.create(
            content='1',
            is_ai_generated=True,
            difficulty='medium',
        )
        text2 = TrainingText.objects.create(
            content='2',
            is_ai_generated=True,
            difficulty='easy',
        )
        text3 = TrainingText.objects.create(
            content='3',
            is_ai_generated=True,
            difficulty='hard',
        )

        texts = list(TrainingText.objects.all())

        texts = [text for text in texts if text in [text1, text2, text3]]

        self.assertEqual(texts[0], text2)
        self.assertEqual(texts[1], text3)


class UserTrainingProgressPropertiesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser_props',
            email='testuser_props@email.com',
            password='pass',
        )

    def setUp(self):
        self.progress = UserTrainingProgress.objects.create(user=self.user)

    def test_str_representation(self):
        self.assertEqual(str(self.progress), self.user.username)

    def test_can_take_test_initial(self):
        self.assertIsNone(self.progress.last_fail_timestamp)
        self.assertTrue(self.progress.can_take_test)

    @parameterized.expand(
        [
            ('25_hours_ago', datetime.timedelta(hours=25), True),
            ('23_hours_ago', datetime.timedelta(hours=23), False),
            ('exact_24_hours', datetime.timedelta(hours=24), True),
        ],
    )
    def test_can_take_test_with_timestamp(self, name, time_delta, expected):
        self.progress.last_fail_timestamp = timezone.now() - time_delta
        self.progress.save()

        self.assertEqual(self.progress.can_take_test, expected)

    @parameterized.expand(
        [
            ('no_fail', None, 0),
            ('failed_just_now', datetime.timedelta(seconds=0), 24),
            ('failed_10_hours_ago', datetime.timedelta(hours=10), 14),
            ('failed_23_hours_ago', datetime.timedelta(hours=23), 1),
            ('failed_25_hours_ago', datetime.timedelta(hours=25), 0),
        ],
    )
    def test_remaining_hours(self, name, time_delta, expected_hours):
        if time_delta is not None:
            self.progress.last_fail_timestamp = timezone.now() - time_delta
            self.progress.save()

        self.assertEqual(self.progress.remaining_hours, expected_hours)


class UserTrainingProgressLogicTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser_logic',
            email='testuser_logic@email.com',
        )
        cls.text1 = TrainingText.objects.create(
            content='text1',
            is_ai_generated=True,
        )
        cls.text2 = TrainingText.objects.create(
            content='text2',
            is_ai_generated=False,
        )

    def setUp(self):
        UserTrainingProgress.objects.filter(user=self.user).delete()
        self.progress = UserTrainingProgress.objects.create(user=self.user)

    def test_get_available_texts_all_initially(self):
        available = self.progress.get_available_texts()
        self.assertEqual(available.count(), 2)
        self.assertIn(self.text1, available)

    def test_get_available_texts_excludes_completed(self):
        self.progress.completed_texts.add(self.text1)

        available = self.progress.get_available_texts()

        self.assertEqual(available.count(), 1)
        self.assertNotIn(self.text1, available)

    def test_add_completed_text_correct_increases_score(self):
        self.progress.add_completed_text(self.text1, is_correct=True)

        self.progress.refresh_from_db()
        self.assertEqual(self.progress.training_score, 1)

    def test_add_completed_text_correct_clears_fail_timestamp(self):
        self.progress.last_fail_timestamp = timezone.now()
        self.progress.save()

        self.progress.add_completed_text(self.text1, is_correct=True)

        self.progress.refresh_from_db()
        self.assertIsNone(self.progress.last_fail_timestamp)

    def test_add_completed_text_incorrect_decreases_score(self):
        self.progress.training_score = 5
        self.progress.save()

        self.progress.add_completed_text(self.text1, is_correct=False)

        self.progress.refresh_from_db()
        self.assertEqual(self.progress.training_score, 3)

    def test_add_completed_text_incorrect_score_not_negative(self):
        self.progress.training_score = 1
        self.progress.save()

        self.progress.add_completed_text(self.text1, is_correct=False)

        self.progress.refresh_from_db()
        self.assertEqual(self.progress.training_score, 0)

    def test_add_completed_text_incorrect_sets_timestamp(self):
        self.assertIsNone(self.progress.last_fail_timestamp)

        self.progress.add_completed_text(self.text1, is_correct=False)

        self.progress.refresh_from_db()
        self.assertIsNotNone(self.progress.last_fail_timestamp)

    def test_add_completed_text(self):
        self.progress.add_completed_text(self.text1, is_correct=False)

        self.assertTrue(
            self.progress.completed_texts.filter(id=self.text1.id).exists(),
        )


@override_settings(
    TRAINING_COMPLETIONS_FOR_PERFORMER=5,
    PERFORMER_GROUP_NAME=settings.PERFORMER_GROUP_NAME,
)
class UserPromotionTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser_promo',
            email='testuser_promo',
            password='pass',
        )
        cls.text = TrainingText.objects.create(
            content='Test',
            is_ai_generated=True,
        )

    def setUp(self):
        UserTrainingProgress.objects.filter(user=self.user).delete()
        self.progress = UserTrainingProgress.objects.create(user=self.user)
        self.user.groups.clear()
        self.user.role = User.Role.CUSTOMER
        self.user.save()

    def test_promotion_adds_to_group(self):
        self.progress.training_score = 4
        self.progress.save()

        self.progress.add_completed_text(self.text, is_correct=True)

        self.assertTrue(
            self.user.groups.filter(name='Performers').exists(),
        )

    def test_promotion_changes_role(self):
        self.progress.training_score = 4
        self.progress.save()

        self.progress.add_completed_text(self.text, is_correct=True)

        self.user.refresh_from_db()
        self.assertEqual(self.user.role, User.Role.PERFORMER)

    def test_no_promotion_if_score_low(self):
        self.progress.training_score = 2
        self.progress.save()

        self.progress.add_completed_text(self.text, is_correct=True)

        self.assertFalse(
            self.user.groups.filter(name='Performers').exists(),
        )
