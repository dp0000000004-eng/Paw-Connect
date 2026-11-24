from unittest.mock import Mock, patch

from django.core import signing
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase, override_settings
from django.urls import reverse

from .middleware import COOKIE_NAME, COOKIE_SALT, FirstRequestMiddleware, verify_human


@override_settings(
    ALLOWED_HOSTS=["testserver"],
    TURNSTILE_SITE_KEY="site-key",
    TURNSTILE_SECRET_KEY="secret-key",
    TURNSTILE_ALLOWED_HOSTNAMES=["example.test"],
)
class TurnstileTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_unverified_request_redirects_to_challenge_with_return_url(self):
        request = self.factory.get("/ai/?topic=math")
        middleware = FirstRequestMiddleware(lambda req: HttpResponse("ok"))

        response = middleware(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"],
            f'{reverse("verify_human")}?next=%2Fai%2F%3Ftopic%3Dmath',
        )

    def test_verified_cookie_allows_request_through(self):
        request = self.factory.get("/")
        request.COOKIES[COOKIE_NAME] = signing.dumps(
            {"verified": True},
            salt=COOKIE_SALT,
        )
        middleware = FirstRequestMiddleware(lambda req: HttpResponse("ok"))

        response = middleware(request)

        self.assertEqual(response.content, b"ok")

    @patch("Campus_Connect.middleware.requests.post")
    def test_successful_turnstile_check_sets_signed_cookie(self, post):
        verification_response = Mock()
        verification_response.json.return_value = {
            "success": True,
            "hostname": "example.test",
        }
        post.return_value = verification_response
        request = self.factory.post(
            "/is-human/?next=%2Fai%2F",
            {"cf-turnstile-response": "one-time-token"},
        )

        response = verify_human(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/ai/")
        self.assertTrue(response.cookies[COOKIE_NAME]["httponly"])
        self.assertTrue(response.cookies[COOKIE_NAME]["secure"])
        self.assertEqual(
            signing.loads(response.cookies[COOKIE_NAME].value, salt=COOKIE_SALT),
            {"verified": True},
        )
        post.assert_called_once()

    @patch("Campus_Connect.middleware.requests.post")
    def test_unexpected_hostname_does_not_set_verified_cookie(self, post):
        verification_response = Mock()
        verification_response.json.return_value = {
            "success": True,
            "hostname": "attacker.test",
        }
        post.return_value = verification_response
        request = self.factory.post(
            "/is-human/",
            {"cf-turnstile-response": "one-time-token"},
        )

        response = verify_human(request)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(COOKIE_NAME, response.cookies)
