# -*- coding: utf-8 -*-
from Acquisition import aq_base
from bda.empower import discourse
from plone import api
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

    def _make_item(self, item):
        ob = aq_base(item.getObject())
        ret = {
            "@id": item.getURL(),
            "@type": item.PortalType(),
            "uid": item.uuid(),
            "title": item.Title(),
            "review_state": item.review_state(),
            "creator": item.Creator(),
            "created": item.CreationDate(),
            "modified": item.ModificationDate(),
            "workspace": getattr(ob, 'workspace', None),
            "client": getattr(ob, 'client', None),
            "coordinators": getattr(ob, 'coordinators', None),
            "expert_pool": getattr(ob, 'expert_pool', None),
            "experts_assigned": getattr(ob, 'experts_assigned', None),
            "previous_workspace": None,
            "next_workspace": None,
        }

        text = getattr(ob, 'text', None)
        # TODO: check if output_relative_to(workspace) is better..?
        ret["text"] = text.output_relative_to(ob) if text else None

        return ret

    @property
    def itemtree(self):
        items = discourse.get_workspace_tree(self.context)
        tree = discourse.build_tree(items)

        roots = discourse.get_all_workspace_roots(self.context, getattr(self.context, 'workspace', None)  # TODO: fix. needs other way to get current workspace name - context might be case.  # noqa
        nexts = []
        for root in roots:
            nexts.append(list(
                discourse.get_next_workspaces(root.getObject())
            ))

        def _make_roots(item):

            return {
                'url': None,
                'title': None
            }

        roots = map(_make_roots, roots)

        for key, items in tree.items():
            tree[key] = map(self._make_item, items)
        return tree

    @property
    def start_path(self):
        root = discourse.get_root_of_workspace(self.context)
        start_path = None
        if root:
            start_path = "/".join(root.getPhysicalPath()[:-1])  # start a level above the start context. itemtree structure works that way.  # noqa
        return start_path

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
        #if not expand:
        #    return result

        # === Your custom code comes here ===

        result['thread']['items'] = self.itemtree
        result['thread']['start_path'] = self.start_path

        return result


class ThreadGet(Service):

    def reply(self):
        service_factory = Thread(self.context, self.request)
        return service_factory(expand=True)['thread']
