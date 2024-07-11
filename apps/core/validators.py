import re
from string import punctuation as punctuation_characters

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from apps.core.constants import (
    PASSWORD_MINIMUM_LENGTH,
    PASSWORD_NUMERIC_REQUIRED,
    PASSWORD_SPECIAL_CHAR_REQUIRED,
    PASSWORD_UPPER_AND_LOWER_REQUIRED,
)


class CustomUsernameValidator(UnicodeUsernameValidator):
    regex = r"^[\w.-]+\Z"
    message = _(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and ./-/_ characters."
    )

class CustomPasswordValidator:
    def validate(self, password, user=None, **kwargs):
        if len(password) < PASSWORD_MINIMUM_LENGTH:
            raise ValidationError(
                _(
                    "Password is too short. "
                    "It must be at least {min_length} characters.",
                ).format(min_length=PASSWORD_MINIMUM_LENGTH),
                code="password_too_short",
            )

        if PASSWORD_UPPER_AND_LOWER_REQUIRED is True and (
            password == password.lower() or password == password.upper()
        ):
            raise ValidationError(
                _("Password must contain both uppercase and lowercase letters."),
                code="password_upper_and_lower_required",
            )

        if PASSWORD_NUMERIC_REQUIRED is True:
            regex = re.compile(r"\d")
            if not regex.search(password):
                raise ValidationError(
                    _("Password must contain digits."),
                    code="password_numeric_required",
                )

        if PASSWORD_SPECIAL_CHAR_REQUIRED is True and (
            not any(char in set(punctuation_characters) for char in password)
        ):
            raise ValidationError(
                _("Password must contain special characters."),
                code="password_special_char_required",
            )

    def get_help_text(self):
        return _("Your password must contain at least {min_length} character.").format(
            min_length=PASSWORD_MINIMUM_LENGTH,
        )
