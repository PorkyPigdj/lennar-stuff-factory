import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Model, Q

from apps.core.utils import get_model

# Run this file using "python manage.py init_project" command


class Command(BaseCommand):
    help = "Create SuperUser (admin)"

    def handle(self, *args, **options):
        user_model: Model = get_user_model()

        superuser_email = os.getenv("DJANGO_ADMIN_EMAIL")
        superuser_username = os.getenv("DJANGO_ADMIN_USERNAME")
        superuser_password = os.getenv("DJANGO_ADMIN_PASSWORD")

        if superuser_email and superuser_username and superuser_password:
            try:
                superuser = user_model.objects.get(
                    Q(email__iexact=superuser_email)
                    | Q(username__iexact=superuser_username),
                )
            except user_model.DoesNotExist:
                superuser = user_model.objects.create_superuser(
                    email=superuser_email,
                    username=superuser_username,
                )
            else:
                superuser.email = superuser_email
                superuser.username = superuser_username

            superuser.first_name = "Admin"
            superuser.last_name = "User"
            superuser.is_staff = True
            superuser.is_superuser = True
            superuser.is_active = True

            superuser.set_password(superuser_password)
            superuser.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"SuperUser for {superuser_email} - {superuser_username} "
                    "is created successfully",
                ),
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("ENV Variables are not set to create SuperUser"),
            )

        try:
            site_id = settings.SITE_ID
            assert "django.contrib.sites" in settings.INSTALLED_APPS
        except (ValueError, AttributeError, AssertionError):
            pass
        else:
            if site_id:
                from django.contrib.sites.models import Site  # noqa: PLC0415

                default_site: Site = Site.objects.filter(pk=site_id).first()
                if default_site:
                    default_site.domain = (
                        f"{settings.BASE_URL_SCHEME}://{settings.BASE_URL_NETLOC}"
                    )
                    default_site.name = settings.PROJECT_NAME
                    default_site.save()
