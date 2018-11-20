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
    return discourse.get_workspace_path(obj)
