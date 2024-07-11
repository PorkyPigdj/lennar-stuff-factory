from django.db import models


class UserRole(models.IntegerChoices):
    ARCHITECT = 1, "Architect"
    DESIGNER = 2, "Designer"
    BUILDER = 3, "Builder"
