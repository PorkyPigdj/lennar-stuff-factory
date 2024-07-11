from django.urls import path

from apps.components.api.v1.views import ComponentViewSet

app_name = "components-api"

urlpatterns = [
    path(
        "",
        ComponentViewSet.as_view(
            {"post": "create", "get": "list", "options": "metadata"}
        ),
        name="component-create-list-api",
    ),
    path(
        "<int:component_id>/",
        ComponentViewSet.as_view(
            {
                "delete": "destroy",
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "options": "metadata",
            }
        ),
        name="component-destroy-update-retrieve-api",
    ),
]
