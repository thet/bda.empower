# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from bda.empower import discourse
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.contentprovider.interfaces import ITALNamespaceData
from zope.contentprovider.provider import ContentProviderBase
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider

import zope.schema


@provider(ITALNamespaceData)
class ITALThreadValue(Interface):

    thread_id = zope.schema.Bytes(title=u"id of thread")


@implementer(ITALThreadValue)
class ThreadProvider(ContentProviderBase):

    template = ViewPageTemplateFile("thread_provider.pt")

    def render(self):
        return self.template()

    def update(self):
        if self.thread_id is None:
            self.thread_id = self.context.getId()
        self._tree = None
        if self.tree is None:
            items = discourse.get_current_workspace_tree(
                self.__parent__.thread_root
            )
            self._tree = discourse.build_tree(items)

    @property
    def _parent_path(self):
        if not isinstance(self.__parent__, self.__class__):
            return "/".join(
                aq_parent(self.__parent__.thread_root).getPhysicalPath()
            )
        return "{0}/{1}".format(
            self.__parent__._parent_path, self.thread_id
        )

    @property
    def tree(self):
        return getattr(self.__parent__, "tree", self._tree)

    @property
    def contributions(self):
        if not isinstance(self.__parent__, self.__class__):
            # initial call
            return [self.__parent__.thread_root]
        return self.tree.get(self._parent_path, [])

    @property
    def level(self):
        return getattr(self.__parent__, "level", -1) + 1
