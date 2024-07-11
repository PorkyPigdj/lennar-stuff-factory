from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

User = get_user_model()


class EmailOrUsernameAuthBackend(ModelBackend):
    # For Session auth in Django Admin with Email or Username

    def authenticate(
        self,
        request,
        identifier=None,
        password=None,
        **kwargs,
    ) -> User | None:
        identifier = identifier or kwargs.get("username", kwargs.get("email"))
        if identifier is None:
            raise ValueError("Username or Email is required to login")

        try:
            try:
                validate_email(identifier)
                user = User.objects.get(email__iexact=identifier)
            except ValidationError:
                user = User.objects.get(username__iexact=identifier)
        except User.DoesNotExist:
            # To prevent Timing Attack
            #  Attacker should not know about existence of a user
            User().set_password(password)
        else:
            if user.check_password(password):
                return user
