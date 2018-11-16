# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return ["bda.empower:uninstall"]


def post_install(context):
    """Post install script"""
    portal = api.portal.get()
    if 'cases' not in portal.contentIds():
        api.content.create(
            type="Cases", id="cases", title=u"Fälle", container=portal
        )


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
