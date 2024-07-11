from rest_framework import serializers

from apps.components.models import Component
from apps.specifications.api.v1.serializers import SpecificationGroupSerializer
from apps.specifications.models import Specification


class ComponentSpecificationSerializer(serializers.ModelSerializer):
    group = SpecificationGroupSerializer(many=False)

    class Meta:
        model = Specification
        fields = ["id", "name", "code", "phase", "group"]


class UpdateComponentSerializer(serializers.ModelSerializer):
    specification = ComponentSpecificationSerializer(read_only=True, many=False)

    class Meta:
        model = Component
        fields = [
            "id",
            "name",
            "description",
            "selected_part",
            "specification",
        ]
        extra_kwargs = {"id": {"read_only": True}, "name": {"read_only": True}}


class ComponentSerializer(serializers.ModelSerializer):
    specification_id = serializers.IntegerField(
        write_only=True, allow_null=False, required=True, min_value=1
    )
    specification = ComponentSpecificationSerializer(read_only=True, many=False)

    class Meta:
        model = Component
        fields = [
            "id",
            "name",
            "description",
            "selected_part",
            "specification",
            "specification_id",
        ]
        extra_kwargs = {"id": {"read_only": True}}
