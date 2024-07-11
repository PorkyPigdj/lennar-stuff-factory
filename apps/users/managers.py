from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Q


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
        self,
        email,
        username,
        password: str | None = None,
        **extra_fields,
    ):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db, force_insert=True)

        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("first_name", "Admin")
        extra_fields.setdefault("last_name", "Admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            email,
            username,
            password,
            **extra_fields,
        )

    def get_by_natural_key(self, username):
        return self.get(Q(username__iexact=username) | Q(email__iexact=username))
