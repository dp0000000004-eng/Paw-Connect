from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Chat


class ChatModelTests(TestCase):
    def test_chat_str(self):
        user = User.objects.create_user(username="aiuser", password="pass12345")
        chat = Chat.objects.create(
            user=user,
            prompt="What is DBMS?",
            response="A database management system stores and retrieves data.",
        )
        self.assertEqual(str(chat), "What is DBMS?")


class ChatViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="aiuser", password="pass12345")
        Chat.objects.create(
            user=self.user,
            prompt="Explain OOP",
            response="Object oriented programming uses classes and objects.",
        )

    def test_chat_requires_login(self):
        response = self.client.get(reverse("ai:ai_view"))
        self.assertEqual(response.status_code, 302)

    def test_chat_page_when_logged_in(self):
        self.client.login(username="aiuser", password="pass12345")
        response = self.client.get(reverse("ai:ai_view"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Explain OOP")
        self.assertContains(response, "Paw AI")
