import logging
from functools import cache
from urllib.error import URLError
from urllib.parse import ParseResult, urlparse

from django.apps import apps
from django.conf import settings

from apps.core.constants import LOGGER_NAME, SWAGGER_URL_PREFIX

logger = logging.getLogger(LOGGER_NAME)


def get_view_action(view):
    try:
        method = view.request.method.lower()
        assert method
    except (AttributeError, AssertionError):
        view_allowed_methods = getattr(view, "allowed_methods", None) or [""]
        method = view_allowed_methods[0].lower()

    try:
        action = view.action
        assert action
        assert action != "metadata" or method == "options"
    except (AttributeError, AssertionError):
        view_action_map = getattr(view, "action_map", None) or {}
        action = view_action_map.get(method)

    return action or ("metadata" if method == "options" else None)


def set_base_url_scheme(url: str) -> str:
    try:
        parsed_url = urlparse(url)
        parsed_url = parsed_url._replace(scheme=settings.BASE_URL_SCHEME)  # FIXME
        parsed_url = parsed_url._replace(netloc=settings.BASE_URL_NETLOC)  # FIXME
        return ParseResult(*parsed_url).geturl()

    except (URLError, LookupError, ValueError) as exc:
        logger.exception(
            "Failed in setting URL",
            extra={
                "url": url,
                "URL_PREFIX": SWAGGER_URL_PREFIX,
                "BASE_URL_SCHEME": settings.BASE_URL_SCHEME,  # FIXME
                "BASE_URL_NETLOC": settings.BASE_URL_NETLOC,  # FIXME
            },
        )
        raise ValueError("Failed in setting URL") from exc


@cache
def get_model(app_name: str, model_name: str):
    return apps.get_model(app_name, model_name)
