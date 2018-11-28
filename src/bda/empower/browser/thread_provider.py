# -*- coding: utf-8 -*-
from bda.empower import discourse
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.contentprovider.provider import ContentProviderBase


BOTTOMLEVEL = 6


class ThreadProvider(ContentProviderBase):

    template = ViewPageTemplateFile("thread_provider.pt")
    recurse = ViewPageTemplateFile("thread_recurse.pt")
    bottomlevel = BOTTOMLEVEL

    def update(self):
        items = discourse.get_current_workspace_tree(
            self.__parent__.thread_root
        )
        tree = discourse.build_tree(items)
        self.itemtree = tree

    def render(self):
        return self.template()

    @property
    def start_path(self):
        start_path = None
        root = discourse.get_root_of_workspace(self.__parent__.thread_root)
        if root:
            # start a level above the start context.
            # itemtree structure works that way.
            start_path = "/".join(root.getPhysicalPath()[:-1])
        return start_path
