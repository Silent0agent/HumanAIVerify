__all__ = ()

from django.test import SimpleTestCase
from django.urls import resolve, reverse

import training.views


class TrainingRoutesTest(SimpleTestCase):
    def test_start(self):
        url = reverse('training:start')
        self.assertEqual(url, '/training/start/')

        resolver = resolve(url)
        self.assertEqual(
            resolver.func.view_class,
            training.views.TrainingStartView,
        )

    def test_take_test(self):
        url = reverse('training:take-test', kwargs={'text_id': 1})
        self.assertEqual(url, '/training/take-test/1/')

        resolver = resolve(url)
        self.assertEqual(
            resolver.func.view_class,
            training.views.TrainingTakeTestView,
        )

    def test_results(self):
        url = reverse('training:results')
        self.assertEqual(url, '/training/results/')

        resolver = resolve(url)
        self.assertEqual(
            resolver.func.view_class,
            training.views.TrainingResultsView,
        )
