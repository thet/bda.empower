# -*- coding: utf-8 -*-
from .setupdevusers import create_dev_users
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return ["bda.empower:example_content"]


REMOVE_INITIAL = ["news", "front-page", "events"]


def post_install(context):
    """Post install script"""

    # install test users if TESTUSER environ variable exists.
    create_dev_users()

    portal = api.portal.get()
    # remove existing
    for cid in REMOVE_INITIAL:
        if cid in portal.contentIds():
            api.content.delete(portal[cid])

    if "cases" not in portal.contentIds():
        api.content.create(
            type="Cases", id="cases", title=u"Fälle", container=portal
        )
