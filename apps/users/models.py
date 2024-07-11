from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.validators import CustomUsernameValidator
from apps.users.enums import UserRole
from apps.users.managers import CustomUserManager


class User(AbstractUser):
    username_validator = CustomUsernameValidator()

    email = models.EmailField(
        verbose_name=_("Email"),
        unique=True,
        error_messages={
            "unique": _("A user with this email already exists."),
        },
    )
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and ./-/_ only.",
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with this username already exists."),
        },
    )

    role = models.PositiveSmallIntegerField(
        choices=UserRole.choices,
        null=True,
        blank=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # TODO no auth implemented yet
    # FIXME must restrict `DEFAULT_AUTHENTICATION_CLASSES` and `DEFAULT_PERMISSION_CLASSES` in
    #  `settings.REST_FRAMEWORK` after Auth implementation
