# -*- coding: utf-8 -*-
from bda.empower.content.contribution import IContribution  # NOQA E501
from bda.empower.testing import BDA_EMPOWER_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class ContributionIntegrationTest(unittest.TestCase):

    layer = BDA_EMPOWER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_ct_contribution_schema(self):
        fti = queryUtility(IDexterityFTI, name='Contribution')
        schema = fti.lookupSchema()
        self.assertEqual(IContribution, schema)

    def test_ct_contribution_fti(self):
        fti = queryUtility(IDexterityFTI, name='Contribution')
        self.assertTrue(fti)

    def test_ct_contribution_factory(self):
        fti = queryUtility(IDexterityFTI, name='Contribution')
        factory = fti.factory
        obj = createObject(factory)


    def test_ct_contribution_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Contribution',
            id='contribution',
        )


    def test_ct_contribution_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Contribution')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_contribution_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Contribution')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'contribution_id',
            title='Contribution container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
