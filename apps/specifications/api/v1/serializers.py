from collections import OrderedDict

from django.db import transaction
from rest_framework import serializers

from apps.components.models import Component
from apps.specifications.enums import SpecificationPhase
from apps.specifications.models import Specification, SpecificationGroup


class SpecificationComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ["id", "name", "description", "selected_part"]
        extra_kwargs = {
            "id": {"read_only": True},
            "selected_part": {"allow_blank": True, "allow_null": True},
        }


class SpecificationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationGroup
        fields = ["id", "name", "code"]
        extra_kwargs = {"id": {"read_only": True}}


class ParentSpecificationSerializer(serializers.ModelSerializer):
    group = SpecificationGroupSerializer(many=False)
    components = SpecificationComponentSerializer(many=True)

    class Meta:
        model = Specification
        fields = ["id", "name", "code", "phase", "group", "components"]


class UpdateSpecificationSerializer(serializers.ModelSerializer):
    group = SpecificationGroupSerializer(many=False, read_only=True)
    components = SpecificationComponentSerializer(many=True, read_only=True)
    cloned_from = ParentSpecificationSerializer(many=False, read_only=True)

    class Meta(ParentSpecificationSerializer.Meta):
        model = Specification
        fields = ["id", "name", "code", "phase", "group", "cloned_from", "components"]
        extra_kwargs = {"id": {"read_only": True}}


class SpecificationSerializer(serializers.ModelSerializer):
    group_id = serializers.IntegerField(
        write_only=True, allow_null=True, required=True, min_value=1
    )

    group = SpecificationGroupSerializer(many=False, read_only=True)
    components = SpecificationComponentSerializer(many=True)
    cloned_from = ParentSpecificationSerializer(many=False, read_only=True)

    class Meta:
        model = Specification
        fields = [
            "id",
            "name",
            "code",
            "phase",
            "group",
            "group_id",
            "cloned_from",
            "components",
        ]
        extra_kwargs = {"id": {"read_only": True}, "phase": {"read_only": True}}

    def create(self, validated_data) -> Specification:
        components_data: list[OrderedDict] = validated_data.pop("components")

        with transaction.atomic():
            specification: Specification = Specification.objects.create(
                **validated_data,
                phase=SpecificationPhase.PLANNING,
            )

            Component.objects.bulk_create(
                objs=[
                    Component(specification_id=specification.pk, **component_data)
                    for component_data in components_data
                ],
                batch_size=100,
            )

        return specification
