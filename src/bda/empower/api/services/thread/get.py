# -*- coding: utf-8 -*-
from bda.empower import discourse
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class Thread(object):

    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self, expand=False):
        """Reply to REST/JSON requests.
        """
        result = {
            'thread': {
                '@id': '{}/@thread'.format(
                    self.context.absolute_url(),
                ),
            },
        }
        if not expand:
            return result

        workspace = self.request.form.get('workspace', None);
        tree = discourse.get_tree(self.context, workspace)
        result['thread']['items'] = tree

        self.request.response.setHeader('Content-Type', 'application/json')
        return result


class ThreadGet(Service):

    def reply(self):
        service_factory = Thread(self.context, self.request)
        return service_factory(expand=True)['thread']
