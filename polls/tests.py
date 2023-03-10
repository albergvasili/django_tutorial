import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose
        pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_questions(self):
        """
        was_published_recently() returns False for questions whose
        pub_date is older than 1 day
        """

        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose
        pub_date is within the last day
        """

        time = timezone.now() - datetime.timedelta(
                hours=23, minutes=59, seconds=59
                )
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(
            question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        res = self.client.get(reverse('polls:index'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'No polls are available')
        self.assertQuerysetEqual(res.context['latest_questions_list'], [])

    def test_past_questions(self):
        question = create_question(question_text='Past question', days=-30)
        res = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(res.context['latest_questions_list'],
                                 [question])

    def test_future_questions(self):
        create_question(question_text='Future question', days=30)
        res = self.client.get(reverse('polls:index'))
        self.assertContains(res, 'No polls are available')
        self.assertQuerysetEqual(res.context['latest_questions_list'], [])

    def test_future_question_and_past_question(self):
        question = create_question(question_text='Past question', days=-30)
        create_question(question_text='Future question', days=30)
        res = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(res.context['latest_questions_list'],
                                 [question])
