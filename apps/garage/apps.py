from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GarageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.garage'

    def ready(self):
        import apps.garage.signals  # noqa
