from django.conf import settings
from rest_framework.pagination import LimitOffsetPagination


class StrictLimitOffsetPagination(LimitOffsetPagination):
    max_limit = settings.MAX_PAGE_SIZE
