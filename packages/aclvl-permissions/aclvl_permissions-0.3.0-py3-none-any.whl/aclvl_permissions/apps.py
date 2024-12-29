from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AclvlPermissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aclvl_permissions'
    verbose_name = _("Access Control and Permissions")