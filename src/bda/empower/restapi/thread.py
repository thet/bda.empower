# -*- coding: utf-8 -*-
from bda.empower import discourse
from plone.restapi.services import Service
from plone.restapi.types.utils import get_jsonschema_for_portal_type


class ThreadGet(Service):

    @property
    def itemtree(self):
        items = discourse.get_current_workspace_tree(self.context)
        tree = discourse.build_tree(items)
        for key, items in tree.items():
            tree[key] = map(
                lambda item: {
                    "@id": item.getURL(),
                    "uid": item.uuid(),
                    "title": item.Title(),
                    "review_state": item.review_state(),
                },
                items,
            )
        return tree

    @property
    def start_path(self):
        root = discourse.get_root_of_workspace(self.context)
        start_path = None
        if root:
            start_path = "/".join(root.getPhysicalPath()[:-1])  # start a level above the start context. itemtree structure works that way.  # noqa
        return start_path

    def reply(self):
        """Reply to REST/JSON requests.
        """
        return {"itemtree": self.itemtree, "start_path": self.start_path}
