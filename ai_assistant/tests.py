from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Chat
from .serializers import ChatSerializer


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
        self.assertContains(response, "Explain OOP")


class ExtraChatViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="pawuser", password="pass12345")

    def test_chat_uses_ai_template(self):
        self.client.login(username="pawuser", password="pass12345")
        response = self.client.get(reverse("ai:ai_view"))
        self.assertTemplateUsed(response, "ai.html")

    def test_chat_login_redirect_target(self):
        response = self.client.get(reverse("ai:ai_view"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url.lower())


class ChatImportTests(TestCase):
    def test_models_serializers_views_urls_import(self):
        from ai_assistant import models as chat_models
        from ai_assistant import serializers as chat_serializers
        from ai_assistant import urls as chat_urls
        from ai_assistant import views as chat_views

        self.assertTrue(chat_models.Chat)
        self.assertTrue(chat_serializers.ChatSerializer)
        self.assertTrue(chat_views.chat)
        self.assertTrue(chat_urls.urlpatterns)


class ChatSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="serialai", password="pass12345")

    def test_chat_serializer_fields(self):
        chat = Chat.objects.create(
            user=self.user,
            prompt="What is DBMS?",
            response="A database management system.",
        )
        data = ChatSerializer(chat).data
        self.assertEqual(data["user"], self.user.id)
        self.assertEqual(data["prompt"], "What is DBMS?")
        self.assertEqual(data["response"], "A database management system.")

    def test_chat_serializer_strips_html_from_prompt(self):
        serializer = ChatSerializer()
        cleaned = serializer.validate_prompt("<script>alert(1)</script>Explain SQL")
        self.assertNotIn("<script>", cleaned)


class ChatRestApiViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="api-ai", password="pass12345")
        other = User.objects.create_user(username="other-ai", password="pass12345")
        Chat.objects.create(
            user=self.user,
            prompt="Explain OOP",
            response="Object oriented programming uses classes.",
        )
        Chat.objects.create(
            user=other,
            prompt="Secret prompt",
            response="Should not appear",
        )

    def test_chat_json_requires_login(self):
        response = self.client.get(reverse("ai:ai_view"), HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 302)

    def test_chat_json_lists_only_current_user_chats(self):
        self.client.login(username="api-ai", password="pass12345")
        response = self.client.get(reverse("ai:ai_view"), HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("chats", payload)
        self.assertIn("greets", payload)
        prompts = [item["prompt"] for item in payload["chats"]]
        self.assertEqual(prompts, ["Explain OOP"])
        self.assertNotIn("Secret prompt", prompts)

    def test_chat_xml_renders(self):
        self.client.login(username="api-ai", password="pass12345")
        response = self.client.get(reverse("ai:ai_view"), HTTP_ACCEPT="application/xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Explain OOP", response.content)

    @patch("ai_assistant.views.OpenAI")
    def test_chat_post_saves_ai_response(self, mock_openai):
        chunk = MagicMock()
        chunk.choices = [MagicMock()]
        chunk.choices[0].delta.content = "DBMS stores data."
        chunk.choices[0].delta.reasoning_content = None
        mock_openai.return_value.chat.completions.create.return_value = [chunk]

        self.client.login(username="api-ai", password="pass12345")
        response = self.client.post(
            reverse("ai:ai_view"),
            {"prompt": "What is a DBMS?"},
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.status_code, 200)
        chat = Chat.objects.get(prompt="What is a DBMS?")
        self.assertEqual(chat.user, self.user)
        self.assertIn("DBMS stores data.", chat.response)
        payload = response.json()
        prompts = [item["prompt"] for item in payload["chats"]]
        self.assertIn("What is a DBMS?", prompts)
