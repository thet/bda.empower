# -*- coding: utf-8 -*-
from bda.empower import discourse
from Products.Five.browser import BrowserView


class RedirectCaseToFirstWorkspaceView(BrowserView):
    """redirector, if someone tries to access the case directly,
    redirect to its initial workspace view
    """

    def __call__(self):
        workspace_root = discourse.get_initial_root(self.context)
        initial_workspace = list(discourse.get_workspace_definitions().keys())[0]  # noqa
        url = "{0}/ws/{1}".format(
            workspace_root.absolute_url(), initial_workspace
        )
        self.request.response.redirect(url)
        return "... redirecting to {0}".format(url)


class RedirectToCurrentWorkspaceRootView(BrowserView):
    """redirector, if someone tries to access the contribution directly
    """

    def __call__(self):
        workspace_root = discourse.get_initial_root(self.context)
        url = "{0}/ws/{1}#{2}".format(
            workspace_root.absolute_url(),
            self.context.workspace,
            self.context.getId(),
        )
        self.request.response.redirect(url)
        return "... redirecting to {0}".format(url)
