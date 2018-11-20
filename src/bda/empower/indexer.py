# -*- coding: utf-8 -*-
from bda.empower import discourse
from bda.empower.behaviors.contribution import IContributionBehavior
from plone.indexer import indexer


@indexer(IContributionBehavior)
def workspace_path_indexer(obj, **kw):
    return tuple(discourse.get_workspace_path(obj))
