from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .widgets import CustomWYSIWYGWidget

class CustomWYSIWYGField(models.TextField):
    """
    Unchained Editor WYSIWYG Field that integrates a custom WYSIWYG editor widget.
    """
    description = _("Custom WYSIWYG Field")

    def __init__(self, *args, license_key=None, **kwargs):
        kwargs['blank'] = True  # Allow blank by default
        super().__init__(*args, **kwargs)
        self._license_key = license_key

    def formfield(self, **kwargs):
        license_key = self._license_key or getattr(settings, 'UNCHAINED_EDITOR_LICENSE_KEY', None)
        defaults = {
            'widget': CustomWYSIWYGWidget(),
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)