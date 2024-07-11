from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.specifications.models import SpecificationGroup, Specification


@admin.register(SpecificationGroup)
class SpecificationGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code")
    list_display_links = ("id", "name", "code")
    search_fields = ("id", "name", "code")

    date_hierarchy = "created_at"


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "get_phase_display",
        "group_display",
        "cloned_from_display",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "name", "code")
    search_fields = ("id", "name", "code")
    list_filter = ("phase",)

    date_hierarchy = "created_at"

    raw_id_fields = ("cloned_from", "group")

    @admin.display(description="Group")
    def group_display(self, obj: Specification):
        if obj.group:
            url = reverse(
                "admin:specifications_specificationgroup_change", args=[obj.group_id]
            )
            return mark_safe(f'<a href="{url}">{obj.group!s}</a>')

    @admin.display(description="Cloned From")
    def cloned_from_display(self, obj: Specification):
        if obj.cloned_from:
            url = reverse(
                "admin:specifications_specification_change", args=[obj.cloned_from_id]
            )
            return mark_safe(f'<b><a href="{url}">{obj.cloned_from_id}</a></b>')
