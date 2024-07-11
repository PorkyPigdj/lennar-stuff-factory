import logging
from typing import TYPE_CHECKING

from django.conf import settings
from django.db import connection
from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.core.constants import LOGGER_NAME
from apps.core.utils import get_view_action

if TYPE_CHECKING:
    from rest_framework.viewsets import GenericViewSet

logger = logging.getLogger(LOGGER_NAME)


class AllowedOptionsMixin:
    # Open OPTIONS method in Swagger for ViewSets/Generics/APIViews that inherit

    def get_authenticators(self):
        self: GenericViewSet | AllowedOptionsMixin

        action = get_view_action(self)
        if action == "metadata":
            return ()
        return super().get_authenticators()

    def get_permissions(self):
        self: GenericViewSet | AllowedOptionsMixin

        action = get_view_action(self)
        if action == "metadata":
            return (AllowAny(),)
        return super().get_permissions()

    @action(detail=False, methods=["OPTIONS"])
    def metadata(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)


@api_view(["GET"])
@permission_classes((AllowAny,))
def perform_healthcheck(request):
    status_code = 200
    is_sqlite_working = True
    # is_redis_working = True

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
    except Exception as exc:
        logger.exception(
            {
                "message": "SQLite is not working",
                "db_config": settings.DATABASES.get("default", {}),
            },
            exc_info=exc,
        )
        is_sqlite_working = False
        status_code = 400

    # try:
    #     redis_conn = Redis(
    #         host=settings.REDIS_HOST,
    #         port=settings.REDIS_PORT_NUMBER,
    #         username=settings.REDIS_USER,
    #         password=settings.REDIS_PASSWORD,
    #         socket_connect_timeout=1,
    #     )
    #     redis_conn.ping()
    # except Exception as exc:
    #     logger.exception(
    #         {
    #             "message": "Redis is not working",
    #             "redis_config": settings.CACHES.get("default", {}),
    #         },
    #         exc_info=exc,
    #     )
    #     is_redis_working = False
    #     status_code = 400

    return Response(
        data={
            "healthcheck": "Running",
            "is_sqlite_working": is_sqlite_working,
            # "is_redis_working": is_redis_working,
        },
        status=status_code,
    )


@api_view(["GET"])
@permission_classes((AllowAny,))
def backend_home_page(request):
    return HttpResponse(
        content=f"""
        <html>
            <head>
                <title>Home Page - Stuff Factory</title>
            </head>
            <body>
                <h1>Home Page - Stuff Factory</h1>
                <ul>
                    <li><a href="{reverse('admin:index')}">Admin Panel</a></li>
                    <li><a href="{reverse('swagger-ui-v1')}">Swagger</a></li>
                </ul>
            </body>
        </html>
        """,
        content_type="text/html",
        status=status.HTTP_200_OK,
    )
