# -*- coding: utf-8 -*-
from bda.empower import discourse
from plone.indexer import indexer
from zope.interface import Interface


@indexer(Interface)
def workspace_path_indexer(obj, **kw):
    """a path of workspace UUIDS.
    - skip obejcts in between with same workspace
    - if it is not a workspace, its treated as a normal path
      this is needed, because otherwise EPI falls back to physical path
    """
    base_path = obj.getPhysicalPath()
    root = discourse.get_initial_root(obj)
    if root is None:
        return base_path
    base_path = base_path[:-1]
    return tuple(base_path) + tuple(discourse.get_workspace_path(obj))
