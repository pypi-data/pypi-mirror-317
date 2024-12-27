from django.utils.translation import gettext_lazy as _


class AccessToUnpublishedConfigIsForbidden(RuntimeError):
    def __init__(self, *args, **kwargs):
        args = args or [403, _("Access to unpublished config is forbidden...")]
        super().__init__(*args, **kwargs)
