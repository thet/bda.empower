# -*- coding: utf-8 -*-
from bda.empower.testing import BDA_EMPOWER_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class DiscourseAPIIntegrationTest(unittest.TestCase):

    layer = BDA_EMPOWER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.case = api.content.create(
            container=self.portal["cases"],
            id="case",
            type="Case",
            workspace="analysis",
        )
        self.case.reindexObject()

    def _create(self, container, cid, ws):
        contrib = api.content.create(
            container=container, id=cid, type="Contribution", workspace=ws
        )
        contrib.reindexObject()
        return contrib

    def test_is_root(self):
        from bda.empower.discourse import is_initial_root

        self.assertTrue(is_initial_root(self.case))
        contrib = self._create(self.case, "a1", "analysis")
        self.assertFalse(is_initial_root(contrib))

    def test_ws_path_root_only(self):
        contrib = self._create(self.case, "a1", "analysis")
        from bda.empower.discourse import get_root_of_workspace

        self.assertEqual(get_root_of_workspace(contrib), self.case)

    def test_ws_path_same_ws(self):
        a1 = self._create(self.case, "a1", "analysis")
        a2 = self._create(a1, "a2", "analysis")
        a3 = self._create(a2, "a3", "analysis")
        from bda.empower.discourse import get_root_of_workspace

        self.assertEqual(get_root_of_workspace(a3), self.case)

    def test_ws_path_several_ws(self):
        a1 = self._create(self.case, "a1", "analysis")
        a2 = self._create(a1, "a2", "analysis")
        s1 = self._create(a2, "s1", "strategy")
        s2 = self._create(s1, "s2", "strategy")
        from bda.empower.discourse import get_root_of_workspace

        self.assertEqual(get_root_of_workspace(a2), self.case)
        self.assertEqual(get_root_of_workspace(s1), s1)
        self.assertEqual(get_root_of_workspace(s2), s1)

    def test_get_workspace_path(self):
        a1 = self._create(self.case, "a1", "analysis")
        a2 = self._create(a1, "a2", "analysis")
        s1 = self._create(a2, "s1", "strategy")
        s2 = self._create(s1, "s2", "strategy")
        c1 = self._create(s2, "c1", "action")
        c2 = self._create(c1, "c2", "action")
        c3 = self._create(c2, "c3", "action")
        from bda.empower.discourse import get_workspace_path

        path = get_workspace_path(c3)
        self.assertEqual(len(path), 4)
        self.assertEqual(path[0], "BASE")
        self.assertEqual(path[1], api.content.get_uuid(self.case))
        self.assertEqual(path[2], api.content.get_uuid(s1))
        self.assertEqual(path[3], api.content.get_uuid(c1))

    def test_get_next_workspace_nodes(self):
        a1 = self._create(self.case, "a1", "analysis")
        a2 = self._create(a1, "a2", "analysis")
        s11 = self._create(a2, "s12", "strategy")
        s12 = self._create(s11, "s12", "strategy")
        s21 = self._create(a2, "s21", "strategy")
        s22 = self._create(s21, "s22", "strategy")
        c1 = self._create(s11, "c1", "action")
        c2 = self._create(s12, "c2", "action")
        c3 = self._create(s21, "c3", "action")
        from bda.empower.discourse import get_next_workspace_nodes

        nodes = get_next_workspace_nodes(self.case)
