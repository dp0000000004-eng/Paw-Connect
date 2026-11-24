import logging
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.core import signing
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods


logger = logging.getLogger(__name__)

COOKIE_NAME = "human_verified"
COOKIE_SALT = "website.human.verification"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365
TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


def is_human_verified(request):
    signed_cookie = request.COOKIES.get(COOKIE_NAME)
    if not signed_cookie:
        return False

    try:
        data = signing.loads(signed_cookie, salt=COOKIE_SALT, max_age=COOKIE_MAX_AGE)
    except signing.BadSignature:
        return False

    return isinstance(data, dict) and data.get("verified") is True


class FirstRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path_info != reverse("verify_human") and not is_human_verified(request):
            verification_url = reverse("verify_human")
            query = urlencode({"next": request.get_full_path()})
            return redirect(f"{verification_url}?{query}")

        return self.get_response(request)


def _verification_page(request, error=None):
    return render(request, "verification.html", {
        "site_key": settings.TURNSTILE_SITE_KEY,
        "error": error,
    })


@require_http_methods(["GET", "POST"])
def verify_human(request):
    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = "/"

    if is_human_verified(request):
        return redirect(next_url)

    if (
        not settings.TURNSTILE_SITE_KEY
        or not settings.TURNSTILE_SECRET_KEY
        or not settings.TURNSTILE_ALLOWED_HOSTNAMES
    ):
        logger.error("Cloudflare Turnstile is not fully configured.")
        return _verification_page(
            request,
            "Verification is temporarily unavailable. Please try again later.",
        )

    if request.method == "GET":
        return _verification_page(request)

    token = request.POST.get("cf-turnstile-response")
    if not token:
        return _verification_page(
            request,
            "Cloudflare verification was not completed. Check the message above, then reload and try again.",
        )

    try:
        response = requests.post(
            TURNSTILE_VERIFY_URL,
            data={
                "secret": settings.TURNSTILE_SECRET_KEY,
                "response": token,
            },
            timeout=10,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException:
        logger.exception("Cloudflare Turnstile verification request failed.")
        return _verification_page(
            request,
            "Could not reach the verification service. Please try again.",
        )

    hostname = result.get("hostname") if isinstance(result, dict) else None
    if not (
        isinstance(result, dict)
        and result.get("success") is True
        and isinstance(hostname, str)
        and hostname.lower().rstrip(".") in settings.TURNSTILE_ALLOWED_HOSTNAMES
    ):
        return _verification_page(request, "Verification failed. Please try again.")

    response = redirect(next_url)
    response.set_cookie(
        COOKIE_NAME,
        signing.dumps({"verified": True}, salt=COOKIE_SALT),
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        secure=True,
        samesite="Lax",
    )
    return response
