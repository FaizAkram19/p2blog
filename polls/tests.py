from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
import datetime
from .models import Question

# Create your tests here.

def create_question(question_text, days):
    now=timezone.now()+datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date = now)

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        future_question=Question.objects.create(question_text="future question", pub_date=timezone.now()+datetime.timedelta(days=30))
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        old_question=Question.objects.create(question_text="old question", pub_date=timezone.now()-datetime.timedelta(days=1, seconds=1))
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently(self):
        recent_question=Question.objects.create(question_text="recent question", pub_date=timezone.now()-datetime.timedelta(hours=23, minutes=59, seconds=59))
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        response=self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls to show")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
    def test_past_question(self):
        past_question=create_question(question_text="Past question.", days=-30)
        response=self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [past_question],
        )
    def test_future_question(self):
        create_question(question_text="future question", days=30)
        response=self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls to show")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
    def test_future_and_past_question(self):
        create_question(question_text="future", days=30)
        past=create_question(question_text="past",days=-30)
        response=self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[past])
    def test_two_question(self):
        q1=create_question(question_text="1",days=-5)
        q2=create_question(question_text="2", days=-6)
        response=self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[q1, q2])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future=create_question(question_text="future", days=5)
        url=reverse("polls:detail", args=(future.id,))
        response=self.client.get(url)
        self.assertEqual(response.status_code, 404)
