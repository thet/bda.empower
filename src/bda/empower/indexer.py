# -*- coding: utf-8 -*-
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
    logger.info(discourse.get_workspace_path(obj))
    return discourse.get_workspace_path(obj)


@indexer(Interface)
def workspace_depth(obj, **kw):
    ws_depth = len(discourse.get_workspace_path(obj)) - 1
    if not ws_depth:
        raise AttributeError
    return ws_depth
