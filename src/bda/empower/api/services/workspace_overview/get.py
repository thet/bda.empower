# -*- coding: utf-8 -*-
from bda.empower import discourse
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class WorkspaceOverview(object):

    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self, expand=False):
        """Reply to REST/JSON requests.
        """
        result = {
            'workspace_overview': {
                '@id': '{}/@workspace_overview'.format(
                    self.context.absolute_url(),
                ),
            },
        }
        if not expand:
            return result

        workspace = self.request.form.get('workspace', None);
        items = discourse.get_all_workspace_roots(self.context, workspace)
        result['workspace_overview']['items'] = [
            discourse.make_item_overview(it) for it in items
        ]

        self.request.response.setHeader('Content-Type', 'application/json')

        return result


class WorkspaceOverviewGet(Service):

    def reply(self):
        service_factory = WorkspaceOverview(self.context, self.request)
        return service_factory(expand=True)['workspace_overview']
