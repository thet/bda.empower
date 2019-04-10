# -*- coding: utf-8 -*-
from bda.empower import discourse
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class CasesOverview(object):

    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self, expand=False):
        """Reply to REST/JSON requests.
        """
        result = {
            'cases_overview': {
                '@id': '{}/@cases_overview'.format(
                    self.context.absolute_url(),
                ),
            },
        }
        if not expand:
            return result

        items = discourse.get_cases()
        result['cases_overview']['items'] = [
            discourse.make_item_overview(it) for it in items
        ]

        self.request.response.setHeader('Content-Type', 'application/json')

        return result


class CasesOverviewGet(Service):

    def reply(self):
        service_factory = CasesOverview(self.context, self.request)
        return service_factory(expand=True)['cases_overview']
