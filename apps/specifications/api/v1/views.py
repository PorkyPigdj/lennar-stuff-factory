from django.db import transaction
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiParameter,
)
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.components.models import Component
from apps.core.views import AllowedOptionsMixin
from apps.specifications.api.v1.filters import SpecificationFilterSet
from apps.specifications.api.v1.serializers import (
    SpecificationSerializer,
    UpdateSpecificationSerializer,
    SpecificationGroupSerializer,
)
from apps.specifications.enums import SpecificationPhase
from apps.specifications.models import Specification, SpecificationGroup


@extend_schema(tags=["Specification Group"])
@extend_schema_view(
    list=extend_schema(summary="List of Specification Groups"),
    retrieve=extend_schema(summary="Retrieve a Specification Group"),
    update=extend_schema(summary="Update a Specification Group"),
    partial_update=extend_schema(summary="Update (partial) a Specification Group"),
    create=extend_schema(summary="Create a new Specification Group"),
    destroy=extend_schema(summary="Delete a Specification Group"),
)
class SpecificationGroupViewSet(AllowedOptionsMixin, viewsets.ModelViewSet):
    queryset = SpecificationGroup.objects.all()
    serializer_class = SpecificationGroupSerializer

    authentication_classes = ()
    # TODO after specifying access levels, `permission_classes` and `authentication_classes` must be overridden

    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    search_fields = ["name"]
    ordering_fields = ["created_at", "updated_at"]
    filterset_fields = ("code",)

    lookup_field = "id"
    lookup_url_kwarg = "spec_group_id"

    throttle_scope = "specification_group_crud"

    http_method_names = ("post", "get", "put", "patch", "delete", "options")


@extend_schema(tags=["Specification"])
@extend_schema_view(
    list=extend_schema(summary="List of Specifications"),
    retrieve=extend_schema(summary="Retrieve a Specification"),
    update=extend_schema(summary="Update a Specification"),
    partial_update=extend_schema(summary="Update (partial) a Specification"),
    create=extend_schema(summary="Create a new Specification"),
    destroy=extend_schema(summary="Delete a Specification"),
)
class SpecificationViewSet(AllowedOptionsMixin, viewsets.ModelViewSet):
    queryset = Specification.objects.select_related(
        "group", "cloned_from"
    ).prefetch_related("components")

    authentication_classes = ()
    # TODO after specifying access levels, `permission_classes` and `authentication_classes` must be overridden

    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    search_fields = ["name", "group__name", "cloned_from__name"]
    ordering_fields = ["created_at", "updated_at"]
    filterset_class = SpecificationFilterSet

    lookup_field = "id"
    lookup_url_kwarg = "spec_id"

    throttle_scope = "specification_crud"

    http_method_names = ("post", "get", "put", "patch", "delete", "options")

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return UpdateSpecificationSerializer

        return SpecificationSerializer

    def get_permissions(self):
        # TODO only Architect can create Specification
        # if self.action == "create":
        #     return [IsAuthenticated(), IsArchitect()]

        return super().get_permissions()

    @extend_schema(
        summary="Clone a Specification",
        request=None,
        responses={
            status.HTTP_201_CREATED: SpecificationSerializer,
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="Specification is still in the planning phase."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Specification not found."
            ),
        },
        parameters=[
            OpenApiParameter(
                name="clone_selected_part",
                description="Clone `selected_part`s of Components of Specification",
                type=bool,
            ),
        ],
    )
    @action(
        detail=True,
        methods=["post"],
        url_path="clone",
        url_name="specification-clone",
    )
    def clone_specification(self, request, *args, **kwargs):
        clone_selected_part: bool = request.query_params.get(
            "clone_selected_part", "false"
        ).lower() in ("true", "yes", "1")

        try:
            specification: dict = (
                Specification.objects.filter(pk=kwargs[self.lookup_url_kwarg])
                .values("id", "name", "code", "phase")
                .get()
            )
        except Specification.DoesNotExist:
            return Response(
                data={"detail": "Specification not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if specification["phase"] == SpecificationPhase.PLANNING:
            return Response(
                data={
                    "detail": "Specification is still in the planning phase, and cannot be cloned"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        components: QuerySet[Component] = Component.objects.filter(
            specification_id=specification["id"]
        )
        if clone_selected_part:
            components: dict = components.values("name", "description", "selected_part")
        else:
            components: dict = components.values("name", "description")

        with transaction.atomic():
            cloned_specification: Specification = Specification.objects.create(
                name=specification["name"],
                code=specification["code"],
                phase=(
                    SpecificationPhase.DESIGN
                    if clone_selected_part
                    else SpecificationPhase.PLANNING
                ),
                cloned_from_id=specification["id"],
            )

            Component.objects.bulk_create(
                objs=[
                    Component(
                        specification_id=cloned_specification.pk, **component_data
                    )
                    for component_data in components
                ],
                batch_size=100,
            )

        serializer: SpecificationSerializer = self.get_serializer(
            instance=cloned_specification
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
