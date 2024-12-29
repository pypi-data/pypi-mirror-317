from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    name = models.CharField(_("Role Name"), max_length=100)
    access_level = models.ManyToManyField('AccessLevel', blank=True, verbose_name=_("Access Levels"))
    role_key = models.CharField(_("Role Key"), max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

    def __str__(self):
        return self.name


class AccessLevel(models.Model):
    name = models.CharField(_("Access Level Name"), max_length=100)
    access_key = models.CharField(_("Access Level Key"), max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _("Access Level")
        verbose_name_plural = _("Access Levels")

    def __str__(self):
        return self.name
