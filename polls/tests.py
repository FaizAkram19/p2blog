from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
import datetime
from .models import Question

# Create your tests here.

def create_question(question_text, days):
    return Question.objects.create(timezone.now()+datetime.timedelta(days=days))

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
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])