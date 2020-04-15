from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class CvRegistrationConfig(AppConfig):
    name = 'cv_registration'
    label = 'cv_registration'
    verbose_name = _("cv_registration")

    def ready(self):
        try:
            import portal.cv_registration.signals  # noqa F401
        except ImportError:
            pass
