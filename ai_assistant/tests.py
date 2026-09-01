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
        self.assertContains(response, "Paw AI")
        self.assertContains(response, "aiuser")
        # Saved chats are not rendered while the NVIDIA API block is commented out
        self.assertNotContains(response, "Explain OOP")


class ExtraChatViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="pawuser", password="pass12345")

    def test_chat_uses_ai_template(self):
        self.client.login(username="pawuser", password="pass12345")
        response = self.client.get(reverse("ai:ai_view"))
        self.assertTemplateUsed(response, "ai.html")

    def test_chat_post_still_renders_page(self):
        self.client.login(username="pawuser", password="pass12345")
        response = self.client.post(
            reverse("ai:ai_view"),
            {"prompt": "What is a DBMS?"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Paw AI")

    def test_chat_post_does_not_save_while_api_disabled(self):
        self.client.login(username="pawuser", password="pass12345")
        self.client.post(
            reverse("ai:ai_view"),
            {"prompt": "What is a DBMS?"},
        )
        self.assertEqual(Chat.objects.count(), 0)

    def test_chat_login_redirect_target(self):
        response = self.client.get(reverse("ai:ai_view"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url.lower())
