from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.core.constants import API_PREFIX
from apps.core.views import backend_home_page, perform_healthcheck

v1_api_urlpatterns = [
    path(
        "schema/",
        SpectacularAPIView.as_view(),
        name="schema-v1",
    ),
    path(
        "schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema-v1"),
        name="swagger-ui-v1",
    ),
    path(
        "specifications/",
        include("apps.specifications.api.v1.urls", "specifications-api"),
    ),
    path(
        "components/",
        include("apps.components.api.v1.urls", "components-api"),
    ),
]

urlpatterns = [
    path("", backend_home_page, name="backend-home-page"),
    path("health-check/", perform_healthcheck, name="health-check"),
    path("admin/", admin.site.urls),
    re_path(
        route=r"^media/(?P<path>.*)$",
        view=serve,
        kwargs={"document_root": settings.MEDIA_ROOT},
    ),
    re_path(
        route=r"^static/(?P<path>.*)$",
        view=serve,
        kwargs={"document_root": settings.STATIC_ROOT},
    ),
    path(f"{API_PREFIX}/v1/", include(v1_api_urlpatterns)),
]
if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
