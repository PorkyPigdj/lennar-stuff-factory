from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import DateTimeMixin


class Component(DateTimeMixin):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    description = models.CharField(
        verbose_name=_("Description"),
        max_length=500,
        null=True,
    )
    selected_part = models.CharField(
        verbose_name=_("Selected Part"),
        max_length=255,
        null=True,
    )

    specification = models.ForeignKey(
        verbose_name=_("Specification"),
        to="specifications.Specification",
        on_delete=models.CASCADE,
        related_name="components",
        related_query_name="component",
    )

    class Meta:
        app_label = "components"
        db_table = "stuff_factory_components"
        verbose_name = "Component"
        verbose_name_plural = "Components"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} | Spec: {self.specification!s}"

    def save(self, *args, **kwargs):
        if not self.selected_part:
            self.selected_part = None

        if not self.description:
            self.description = None

        super().save(*args, **kwargs)
