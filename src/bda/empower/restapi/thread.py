# -*- coding: utf-8 -*-
from bda.empower import discourse
from plone.restapi.services import Service
from plone.restapi.types.utils import get_jsonschema_for_portal_type
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class ThreadGet(Service):

    @property
    def itemtree(self):
        items = discourse.get_current_workspace_tree(self.context)
        tree = discourse.build_tree(items)
        for key, items in tree.items():
            tree[key] = map(
                lambda item: {
                    '@id': item['url'],
                    'uid': item['uid'],
                    'title': item['title'],
                    'review_state': item['review_state'],
                },
                items
            )
        return tree

    @property
    def start_path(self):
        start_path = "/".join(
            discourse.get_root_of_workspace(self.context).getPhysicalPath()[
                :-1
            ]  # noqa start a level above the start context. itemtree structure works that way.
        )
        return start_path

    def reply(self):
        """Reply to REST/JSON requests.
        """
        return {
            'itemtree': self.itemtree,
            'start_path': self.start_path
        }
