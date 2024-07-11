from django.contrib import admin
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.components.models import Component


class ComponentAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].required = False
        self.fields["selected_part"].required = False


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    form = ComponentAdminForm

    list_display = (
        "id",
        "name",
        "description",
        "selected_part",
        "specification_display",
    )
    list_display_links = ("id", "name")
    search_fields = ("id", "name", "description", "selected_part")

    date_hierarchy = "created_at"

    raw_id_fields = ("specification",)

    @admin.display(description="Specification")
    def specification_display(self, obj: Component):
        if obj.specification:
            url = reverse(
                "admin:specifications_specification_change", args=[obj.specification_id]
            )
            return mark_safe(f'<a href="{url}">{obj.specification!s}</a>')
