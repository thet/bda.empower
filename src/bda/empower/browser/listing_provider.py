# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from bda.empower import discourse
from plone import api
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.contentprovider.provider import ContentProviderBase


class ListingProvider(ContentProviderBase):

    template = ViewPageTemplateFile("listing_provider.pt")

    @property
    def current_def(self):
        return self.__parent__.current_def

    def update(self):

        self.workspace_roots = []
        for brain in discourse.get_all_workspace_roots(
            self.context, self.current_def[0]
        ):
            record = {}
            self.workspace_roots.append(record)
            record["current"] = brain.getObject()
            record["previous"] = aq_parent(record["current"])
            record["following"] = []
            for brain in discourse.get_next_workspaces(record["current"]):
                record["following"].append(brain.getObject())

    def render(self):
        return self.template()

    def workspace_url(self, node):
        url = "{0}/ws/{1}/{2}".format(
            self.context.absolute_url(),
            node.workspace,
            api.content.get_uuid(discourse.get_root_of_workspace(node)),
        )
        if not discourse.is_workspace_root(node):
            url = "{0}#{1}".format(url, node.getId())
        return url
