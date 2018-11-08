# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import bda.empower


class BdaEmpowerLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=bda.empower)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'bda.empower:default')


BDA_EMPOWER_FIXTURE = BdaEmpowerLayer()


BDA_EMPOWER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(BDA_EMPOWER_FIXTURE,),
    name='BdaEmpowerLayer:IntegrationTesting',
)


BDA_EMPOWER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(BDA_EMPOWER_FIXTURE,),
    name='BdaEmpowerLayer:FunctionalTesting',
)


BDA_EMPOWER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        BDA_EMPOWER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='BdaEmpowerLayer:AcceptanceTesting',
)
