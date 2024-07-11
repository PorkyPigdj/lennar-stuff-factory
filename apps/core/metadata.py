from collections import OrderedDict

from django.utils.encoding import force_str
from rest_framework import serializers
from rest_framework.metadata import SimpleMetadata
from rest_framework.request import clone_request


class CustomMetadata(SimpleMetadata):
    # Fulfill OPTIONS method response all each ViewSet/Generic/APIViews, based on the properties

    def determine_metadata(self, request, view) -> OrderedDict:
        metadata: OrderedDict = super().determine_metadata(request, view)
        if hasattr(view, "search_fields"):
            metadata["search_fields"] = view.search_fields
        if hasattr(view, "ordering_fields"):
            metadata["ordering_fields"] = view.ordering_fields

        return metadata

    def determine_actions(self, request, view):
        actions = {}
        for method in {"PUT", "POST", "GET", "PATCH", "DELETE"} & set(
            view.allowed_methods,
        ):
            view.request = clone_request(request, method)

            if method == "DELETE":
                serializer_info = None
            else:
                serializer = view.get_serializer()
                serializer_info = self.get_serializer_info(serializer)

            actions[method] = serializer_info
            view.request = request
        return actions

    def get_field_info(self, field):
        field_info = OrderedDict()
        field_info["type"] = self.label_lookup[field]
        field_info["required"] = getattr(field, "required", False)

        attrs = [
            "read_only",
            "label",
            "help_text",
            "min_length",
            "max_length",
            "min_value",
            "max_value",
        ]

        for attr in attrs:
            value = getattr(field, attr, None)
            if value:
                field_info[attr] = force_str(value, strings_only=True)

        if getattr(field, "child", None):
            field_info["child"] = self.get_field_info(field.child)
        elif getattr(field, "fields", None):
            field_info["children"] = self.get_serializer_info(field)

        if not isinstance(
            field,
            serializers.RelatedField | serializers.ManyRelatedField,
        ) and hasattr(field, "choices"):
            field_info["choices"] = [
                {
                    "value": choice_value,
                    "display_name": force_str(choice_name, strings_only=True),
                }
                for choice_value, choice_name in field.choices.items()
            ]

        return field_info
