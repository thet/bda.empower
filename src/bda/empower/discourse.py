# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from bda.empower.workspacedefinition import WORKSPACE_DEFINITION
from plone import api


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


def get_root_of_workspace(current):
    """the next root with a different previous workspace

    - iterates in direction of the node and return the first with a different
      workspace.
    """
    while True:
        parent = aq_parent(current)
        current_ws = getattr(current, WORKSPACE_ATTRIBUTE)
        parent_ws = getattr(parent, WORKSPACE_ATTRIBUTE, None)
        if current_ws != parent_ws:
            break
        current = parent
    return current


def get_workspace_path(node):
    """a list of workspace root UIDs starting with the initial root.

    all none-workspace roots are omitted
    """
    ws_root = get_root_of_workspace(node)
    path = [api.content.get_uuid(ws_root)]
    while not is_initial_root(ws_root):
        ws_root = get_root_of_workspace(aq_parent(ws_root))
        path.insert(0, api.content.get_uuid(ws_root))
    return path


def get_next_workspace_nodes(node):
    """the next nodes in the tree with a different workspace.different
    """
    brains = api.content.find()
