"""apps."""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
