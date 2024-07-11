import django_filters

from apps.specifications.enums import SpecificationPhase
from apps.specifications.models import Specification


class SpecificationFilterSet(django_filters.FilterSet):
    group_code = django_filters.CharFilter(
        field_name="group__code",
        lookup_expr="exact",
        help_text="Filter by `group` code",
    )
    cloned_from = django_filters.NumberFilter(
        field_name="cloned_from_id",
        lookup_expr="exact",
        help_text="Filter by `cloned_from` ID",
    )
    phase = django_filters.MultipleChoiceFilter(choices=SpecificationPhase.choices)

    class Meta:
        model = Specification
        fields = ("group_code", "cloned_from", "phase")
