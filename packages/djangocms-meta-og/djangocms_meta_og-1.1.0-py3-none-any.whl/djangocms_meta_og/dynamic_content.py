from urllib.parse import quote

from django.http import HttpRequest


def get_current_page_url(request: HttpRequest) -> str:
    """Get current page url."""
    return quote(request.build_absolute_uri(request.current_page.get_absolute_url()), "&?")


def get_current_page_title(request: HttpRequest) -> str:
    """Get current page title."""
    return request.current_page.get_page_title()


def get_current_page_description(request: HttpRequest) -> str:
    """Get current page description."""
    return request.current_page.get_meta_description()
