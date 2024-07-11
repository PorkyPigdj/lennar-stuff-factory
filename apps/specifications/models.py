from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import DateTimeMixin
from apps.specifications.enums import SpecificationPhase


class SpecificationGroup(DateTimeMixin):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    code = models.CharField(verbose_name=_("Code"), max_length=100)

    class Meta:
        app_label = "specifications"
        db_table = "stuff_factory_specification_groups"
        verbose_name = "Specification Group"
        verbose_name_plural = "Specification Groups"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} -> {self.code}"


class Specification(DateTimeMixin):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    code = models.CharField(verbose_name=_("Code"), max_length=100)

    phase = models.IntegerField(
        verbose_name=_("Phase"),
        choices=SpecificationPhase.choices,
        default=SpecificationPhase.PLANNING,
    )

    group = models.OneToOneField(
        verbose_name=_("Group"),
        to="specifications.SpecificationGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="specification",
        related_query_name="specification",
    )
    cloned_from = models.ForeignKey(
        verbose_name=_("Cloned From"),
        to="self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clones",
        related_query_name="clone",
    )

    class Meta:
        app_label = "specifications"
        db_table = "stuff_factory_specifications"
        verbose_name = "Specification"
        verbose_name_plural = "Specifications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} -> {self.code} | Group: {self.group!s}"
