# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView


class WorkspaceView(BrowserView):
    def workspace_title(self):
        return "".join(self.request["TraversalRequestNameStack"])
