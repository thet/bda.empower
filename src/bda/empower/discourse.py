# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from bda.empower.interfaces import IWorkspaceAware
from bda.empower.workspacedefinition import WORKSPACE_DEFINITION
from plone import api
from Products.CMFPlone.interfaces import IPloneSiteRoot


ROOT_TYPES = ["Case"]
CHILD_TYPES = ["Contribution"]
NODE_TYPES = ROOT_TYPES + CHILD_TYPES
WORKSPACE_ATTRIBUTE = "workspace"


def get_workspace_definitions():
    """the definition of the workspaces/workflows as an ordered dict.

    - the key is the identifier of the node
    - the first node is the initial workflow state.
    - the value is dict with keys:
      - title: a string or i18n message id used for display
      - next: a list of node identifiers of allowed transitions
      - no-parent: the node is allowed to be directlty created as a child node
        of the root node.
    """
    # Todo: Read this from registry...
    return WORKSPACE_DEFINITION


def get_workspace_definition(identifier):
    """return one workspace defintion by identifier

    - the value is dict with keys:
      - title: a string or i18n message id used for display
      - next: a list of node identifiers of allowed transitions
      - no-parent: the node is allowed to be directlty created as a child node
        of the root node.
    """
    return get_workspace_definitions()[identifier]


def get_allowed_workspaces(node):
    """context specific vocabulary of a node.

    - list of tuples with (id, title)
    - first item is alway the current workspace
    - following items are the next workspaces
    - root item can pnly have initial workspace
    """
    workspace_definitions = get_workspace_definitions()
    if node.portal_type not in NODE_TYPES:
        raise ValueError(
            "workspace_next_vocabulary_factory called in wrong context"
        )
    if node.portal_type in ROOT_TYPES:
        first_id, first_record = workspace_definitions.items()[0]
        yield first_id, first_record["title"]
    else:
        parent = aq_parent(node)
        parent_ws = getattr(parent, WORKSPACE_ATTRIBUTE)
        parent_ws_def = workspace_definitions[parent_ws]
        yield parent_ws, parent_ws_def["title"]
        for workspace_id in parent_ws_def["next"]:
            yield workspace_id, workspace_definitions[workspace_id]["title"]


def is_initial_root(node):
    """wether node is the initial root or not"""
    return node.portal_type in ROOT_TYPES


def is_workspace_root(node):
    """wether node is a workspace root or not"""
    return is_initial_root(node) or (
        node.portal_type in CHILD_TYPES
        and node.workspace != aq_parent(node).workspace
    )


def get_initial_root(node):
    """wether node is the initial root or not"""
    if node.portal_type not in NODE_TYPES:
        return None
    while True:
        if is_initial_root(node):
            return node
        node = aq_parent(node)


def get_root_of_workspace(current):
    """the next root with a different previous workspace

    - iterates in direction of the node and return the first with a different
      workspace.
    """
    while True:
        if IPloneSiteRoot.providedBy(current):
            return None
        parent = aq_parent(current)
        if not IWorkspaceAware.providedBy(current):
            current = parent
            continue
        current_ws = getattr(current, WORKSPACE_ATTRIBUTE)
        parent_ws = getattr(parent, WORKSPACE_ATTRIBUTE, None)
        if current_ws != parent_ws:
            return current
        current = parent


def get_workspace_path(current):
    """a list of workspace root UIDs starting with the initial root.

    - all none-workspace roots in between are omitted
    - all nodes
    - at the end we get something like:
      "/Plone/cases/9c92a34469086440a841d5a532e/c53d93aa4f68442296482f7fa46"
    """
    last_ws = None
    path = []
    while True:
        ws_root = get_root_of_workspace(current)
        if ws_root is None:
            break
        path.insert(0, ws_root.getId())
        last_ws = ws_root
        current = aq_parent(ws_root)
    # last ws_root before leaving workspace tree is used to create a path
    # to the workspace
    if last_ws is None:
        return current.getPhysicalPath()
    return tuple(list(last_ws.getPhysicalPath()[:-1]) + path)


def get_next_workspaces(
    node,
    root=True,
    context_aware=False,
    sort_on="workspace_depth",
    sort_order="ascending",
):
    """catalog brains of next nodes in the tree with a different workspace.

    - node is the context to work on
    - root (bool) defined is only workspace roots are to be returned
    - context_aware (bool): normal all next workspace of the root of the given
      workspace are returned. filter them to show only under given context
      physical path
    - sort_on (like catalog)
    - sort_order (like catalog)
    """
    current_path = "/".join(get_workspace_path(node))
    cat = api.portal.get_tool("portal_catalog")
    query = dict(workspace_path={})
    query["workspace_path"]["query"] = current_path
    query["workspace_path"]["depth"] = 1
    if root:
        query["workspace_root"] = True
    query["sort_on"] = sort_on
    query["sort_order"] = sort_order
    if context_aware:
        query["path"] = '/'.join(node.getPhysicalPath())
    brains = cat(**query)
    return brains
