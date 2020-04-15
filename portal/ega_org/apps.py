from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class EgaOrgConfig(AppConfig):
    name = 'ega_org'
    label = 'ega_org'
    verbose_name = _("ega_org")

    def ready(self):
        try:
            import portal.ega_org.signals  # noqa F401
        except ImportError:
            pass
