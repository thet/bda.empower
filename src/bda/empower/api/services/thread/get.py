# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Acquisition import aq_parent
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
        ob = item.getObject()
        ob_base = aq_base(ob)

        previous = None
        parent = aq_parent(ob)
        if parent.portal_type in discourse.NODE_TYPES and\
            aq_base(parent).workspace != ob_base.workspace:

            previous = '/'.join(parent.getPhysicalPath())

        next = []
        for child in ob.contentValues():
            if aq_base(child).workspace != ob_base.workspace:
                next.append('/'.join(child.getPhysicalPath()))

        ret = {
            "@id": item.getURL(),
            "@type": item.PortalType(),
            "uid": item.uuid(),
            "title": item.Title(),
            "review_state": item.review_state(),
            "creator": item.Creator(),
            "created": item.CreationDate(),
            "modified": item.ModificationDate(),
            "workspace": getattr(ob_base, 'workspace', None),
            "client": getattr(ob_base, 'client', None),
            "coordinators": getattr(ob_base, 'coordinators', None),
            "expert_pool": getattr(ob_base, 'expert_pool', None),
            "experts_assigned": getattr(ob_base, 'experts_assigned', None),
            "previous_workspace": previous,
            "next_workspace": next,
        }

        text = getattr(ob_base, 'text', None)
        # TODO: check if output_relative_to(workspace) is better..?
        ret["text"] = text.output_relative_to(ob) if text else None

        return ret

    @property
    def itemtree(self):
        items = discourse.get_workspace_tree(self.context)
        tree = discourse.build_tree(items)

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
