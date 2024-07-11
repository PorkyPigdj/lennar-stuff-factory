import django_filters

from apps.components.models import Component


class ComponentFilterSet(django_filters.FilterSet):
    specification = django_filters.CharFilter(
        field_name="specification_id",
        lookup_expr="exact",
        help_text="Filter by `specification` ID",
    )

    class Meta:
        model = Component
        fields = ("specification",)
