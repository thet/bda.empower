# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from bda.empower.testing import BDA_EMPOWER_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestSetup(unittest.TestCase):
    """Test that bda.empower is properly installed."""

    layer = BDA_EMPOWER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if bda.empower is installed."""
        self.assertTrue(self.installer.isProductInstalled("bda.empower"))

    def test_browserlayer(self):
        """Test that IBdaEmpowerLayer is registered."""
        from bda.empower.interfaces import IBdaEmpowerLayer
        from plone.browserlayer import utils

        self.assertIn(IBdaEmpowerLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = BDA_EMPOWER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstallProducts(["bda.empower"])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if bda.empower is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled("bda.empower"))

    def test_browserlayer_removed(self):
        """Test that IBdaEmpowerLayer is removed."""
        from bda.empower.interfaces import IBdaEmpowerLayer
        from plone.browserlayer import utils

        self.assertNotIn(IBdaEmpowerLayer, utils.registered_layers())
