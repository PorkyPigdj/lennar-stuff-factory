from django.urls import path

from apps.specifications.api.v1.views import (
    SpecificationViewSet,
    SpecificationGroupViewSet,
)

app_name = "specifications-api"

urlpatterns = [
    path(
        "",
        SpecificationViewSet.as_view(
            {"post": "create", "get": "list", "options": "metadata"}
        ),
        name="specification-create-list-api",
    ),
    path(
        "<int:spec_id>/",
        SpecificationViewSet.as_view(
            {
                "delete": "destroy",
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "options": "metadata",
            }
        ),
        name="specification-destroy-update-retrieve-api",
    ),
    path(
        "<int:spec_id>/clone/",
        SpecificationViewSet.as_view(
            {
                "post": "clone_specification",
                "options": "metadata",
            }
        ),
        name="specification-clone-api",
    ),
    path(
        "groups/",
        SpecificationGroupViewSet.as_view(
            {"post": "create", "get": "list", "options": "metadata"}
        ),
        name="specification-group-create-list-api",
    ),
    path(
        "groups/<int:spec_group_id>/",
        SpecificationGroupViewSet.as_view(
            {
                "delete": "destroy",
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "options": "metadata",
            }
        ),
        name="specification-group-destroy-update-retrieve-api",
    ),
]
