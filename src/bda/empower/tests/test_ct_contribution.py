# -*- coding: utf-8 -*-
from bda.empower.testing import BDA_EMPOWER_INTEGRATION_TESTING
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility
from zope.container.interfaces import INameChooser

import unittest


class ContributionIntegrationTest(unittest.TestCase):

    layer = BDA_EMPOWER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.cases = self.portal["cases"]

    def test_ct_contribution_fti(self):
        fti = queryUtility(IDexterityFTI, name="Contribution")
        self.assertTrue(fti)

    def test_ct_contribution_not_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Contribution")
        self.assertFalse(
            fti.global_allow, u"{0} is globally addable!".format(fti.id)
        )

    def test_ct_contribution_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Contribution")
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.case,
            "contribution_id",
            title="Contribution container",
        )
        self.parent = self.case[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent, type="Document", title="My Content"
            )

    def test_ct_contribution_namechooser(self):
        case = api.content.create(
            container=self.cases, id="foobarbaz", type="Case"
        )
        chooser = INameChooser(self.cases)
        new_id = chooser.chooseName(None, case)
        self.assertTrue(len(new_id) == 3)

        contribution = api.content.create(
            container=self.cases["foobarbaaz"], id="foobarbaz", type="Case"
        )
        chooser = INameChooser(self.cases["foobarbaz"])
        new_id = chooser.chooseName(None, contribution)
        self.assertTrue(len(new_id) == 3)
