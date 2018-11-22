# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from bda.empower import discourse
from plone.indexer import indexer
from zope.interface import Interface

import logging


logger = logging.getLogger(__name__)


@indexer(Interface)
def workspace_path_indexer(obj, **kw):
    """a path of workspace UUIDS.
    - skip obejcts in between with same workspace
    - if it is not a workspace, its treated as a normal path
      this is needed, because otherwise EPI falls back to physical path
    """
    return discourse.get_workspace_path(obj)


@indexer(Interface)
def workspace_depth_indexer(obj, **kw):
    ws_depth = len(discourse.get_workspace_path(obj)) - 1
    if not ws_depth:
        raise AttributeError("n/a")
    return ws_depth


@indexer(Interface)
def workspace_root_indexer(obj, **kw):
    if obj.portal_type not in discourse.NODE_TYPES:
        raise AttributeError("n/a")
    return discourse.is_workspace_root(obj)
