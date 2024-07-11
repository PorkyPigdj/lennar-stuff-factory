from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from rest_framework import viewsets, filters

from apps.components.api.v1.filters import ComponentFilterSet
from apps.components.api.v1.serializers import (
    ComponentSerializer,
    UpdateComponentSerializer,
)
from apps.components.models import Component
from apps.core.views import AllowedOptionsMixin


@extend_schema(tags=["Component"])
@extend_schema_view(
    list=extend_schema(summary="List of Components"),
    retrieve=extend_schema(summary="Retrieve a Component"),
    update=extend_schema(summary="Update a Component"),
    partial_update=extend_schema(summary="Update (partial) a Component"),
    create=extend_schema(summary="Create a new Component"),
    destroy=extend_schema(summary="Delete a Component"),
)
class ComponentViewSet(AllowedOptionsMixin, viewsets.ModelViewSet):
    queryset = Component.objects.select_related("specification")

    authentication_classes = ()
    # TODO after specifying access levels, `permission_classes` and `authentication_classes` must be overridden

    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    search_fields = ["name", "description", "selected_part"]
    ordering_fields = ["created_at", "updated_at"]
    filterset_class = ComponentFilterSet

    lookup_field = "id"
    lookup_url_kwarg = "component_id"

    throttle_scope = "component_crud"

    http_method_names = ("post", "get", "put", "patch", "delete", "options")

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return UpdateComponentSerializer

        return ComponentSerializer

    def get_permissions(self):
        # TODO Designer can update Component
        # if self.action in ("update", "partial_update"):
        #     return [IsAuthenticated(), IsArchitect()]

        return super().get_permissions()
