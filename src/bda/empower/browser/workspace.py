# -*- coding: utf-8 -*-
from bda.empower import discourse
from plone import api
from Products.Five.browser import BrowserView
from zExceptions import Redirect
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class WorkspaceView(BrowserView):
    def __init__(self, context, request):
        super(WorkspaceView, self).__init__(context, request)
        self.subpath = []
        self.current_def = None
        # if a thread root is set, show thread, otherwise show overview
        self.thread_root = None

    def publishTraverse(self, request, name):
        self.subpath.append(name)
        return self

    def update(self):
        wdefs = discourse.get_workspace_definitions()
        first_workspace = list(wdefs.keys())[0]
        initial_def = first_workspace, wdefs[first_workspace]

        # are we on intital view?
        if not self.subpath:
            self.current_def = initial_def
            self.thread_root = self.context
            return

        # first subpath is the workspace requested
        workspace = self.subpath[0]
        if workspace not in wdefs:
            raise Redirect(self.workspace_url())
        self.current_def = workspace, wdefs[workspace]

        # second subpath, if given, is the root of the current thread
        if len(self.subpath) > 1:
            # second part, if given, is the uid of the root of the thread
            try:
                obj = api.content.get(UID=self.subpath[1])  # may be ValueError
                self.thread_root = discourse.get_root_of_workspace(obj)
                if self.thread_root is None:
                    raise ValueError("not a thread")
            except ValueError:
                raise Redirect(self.workspace_url())

        # initial?
        if self.thread_root is None and workspace == first_workspace:
            self.thread_root = self.context

        if len(self.subpath) > 2:
            # this is wrong
            raise Redirect(self.workspace_url())

    def workspaces_defs(self):
        return list(discourse.get_workspace_definitions().items())

    def workspace_url(self, workspace_def=None, obj=None):
        w_def = workspace_def or self.current_def
        url = "{0}/ws/{1}".format(self.context.absolute_url(), w_def[0])
        if obj:
            url = "{0}/{1}".format(url, api.content.get_uuid(obj=obj))
        return url
