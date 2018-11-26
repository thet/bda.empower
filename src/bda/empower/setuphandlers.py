# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from .testuser import install_test_users
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return ["bda.empower:uninstall"]


REMOVE_INITIAL = ["news", "front-page", "events"]


def post_install(context):
    """Post install script"""

    # install test users if TESTUSER environ variable exists.
    install_test_users()

    portal = api.portal.get()
    # remove existing
    for cid in REMOVE_INITIAL:
        if cid in portal.contentIds():
            api.content.delete(portal[cid])

    if "cases" not in portal.contentIds():
        api.content.create(
            type="Cases", id="cases", title=u"Fälle", container=portal
        )


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
