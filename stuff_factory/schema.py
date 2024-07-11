from drf_spectacular.generators import EndpointEnumerator, SchemaGenerator
from drf_spectacular.openapi import AutoSchema

from apps.core.constants import SWAGGER_URL_PREFIX


def custom_preprocessing_hook(endpoints):
    filtered = []
    for path, path_regex, method, callback in endpoints:
        # Remove all but DRF API endpoints
        if path.lstrip("/").startswith(SWAGGER_URL_PREFIX) and "schema" not in path:
            filtered.append((path, path_regex, method, callback))
    return filtered


class CustomEndpointEnumerator(EndpointEnumerator):
    def get_allowed_methods(self, callback):
        if hasattr(callback, "actions"):
            actions = set(callback.actions)
            http_method_names = set(callback.cls.http_method_names)
            methods = [method.upper() for method in actions & http_method_names]
        else:
            methods = callback.cls().allowed_methods

        return [
            method for method in methods if method not in {"HEAD", "TRACE", "CONNECT"}
        ]


class CustomSchemaGenerator(SchemaGenerator):
    endpoint_inspector_cls = CustomEndpointEnumerator


class CustomSchema(AutoSchema):
    method_mapping = {
        "get": "retrieve",
        "post": "create",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
        "options": "metadata",
    }
