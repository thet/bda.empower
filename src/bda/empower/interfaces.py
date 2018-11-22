# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Attribute
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IBdaEmpowerLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IWorkspaceAware(Interface):

    workspace = Attribute("identifier of a workspace (Bytes)")
