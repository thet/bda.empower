# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Acquisition import aq_parent
from bda.empower.interfaces import IWorkspaceAware
from bda.empower.workspacedefinition import WORKSPACE_DEFINITION
from plone import api
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.app.uuid.utils import uuidToCatalogBrain
from plone.uuid.interfaces import IUUID
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component.hooks import getSite


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
    if not node:
        # Allow node-less access to return all workspaces.
        # plone.restapi otherwise breaks when validating the schema.
        for ws, title in workspace_definitions.items():
            yield ws, title
            return

    if node and node.portal_type not in NODE_TYPES + ['Cases']:
        raise ValueError(
            "workspace_next_vocabulary_factory called in wrong context"
        )
    if node.portal_type in ROOT_TYPES + ['Cases']:
        first_id, first_record = list(workspace_definitions.items())[0]
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
    return aq_base(node).portal_type in ROOT_TYPES


def is_workspace_root(node):
    """wether node is a workspace root or not"""
    node_base = aq_base(node)
    return is_initial_root(node) or (
        node_base.portal_type in CHILD_TYPES
        and (
            getattr(node_base, WORKSPACE_ATTRIBUTE, None) !=
            getattr(aq_base(aq_parent(node)), WORKSPACE_ATTRIBUTE, None)
        )
    )


def get_initial_root(node):
    """get the workspace root"""
    if not node or node.portal_type not in NODE_TYPES:
        return None
    return node if is_initial_root(node) else get_initial_root(aq_parent(node))


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
        current_ws = getattr(current, WORKSPACE_ATTRIBUTE, None)
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
    portal_type=NODE_TYPES,
    sort_on="created",
    sort_order="ascending",
):
    """catalog brains of next nodes in the tree with a different workspace.

    - node is the context to work on
    - root (bool): If true, only workspace roots are to be returned
    - context_aware (bool): normal all next workspace of the root of the given
      workspace are returned. filter them to show only under given context
      physical path
    - portal_type - usually nothing one wants to overide
    - sort_on (like catalog)
    - sort_order (like catalog)
    """
    current_path = "/".join(get_workspace_path(node))
    cat = api.portal.get_tool("portal_catalog")
    query = dict(workspace_path={})
    query["workspace_path"]["query"] = current_path
    query["workspace_path"]["depth"] = 1
    query["portal_type"] = portal_type
    if root:
        query["workspace_root"] = True
    query["sort_on"] = sort_on
    query["sort_order"] = sort_order
    if context_aware:
        query["path"] = "/".join(node.getPhysicalPath())
    brains = cat(**query)
    return brains


def get_current_workspace_tree(current, context_aware=False):
    """a tree of brains of the current workspace

    - current is the context to work on
    - context_aware (bool):
      False: full tree workspace,
      True: partial workspace from current
    """
    # XXX hack: since EPI is optimized to return exactly onne item for a depth
    # of 0, we use depth of 1 and query the parent path
    # and also the whole physical path
    base_node = get_root_of_workspace(current)
    if not base_node:
        return []
    current_path = "/".join(get_workspace_path(aq_parent(base_node)))
    cat = api.portal.get_tool("portal_catalog")
    query = dict(workspace_path={})
    query["workspace_path"]["query"] = current_path
    query["workspace_path"]["depth"] = 1
    if context_aware:
        query["path"] = "/".join(current.getPhysicalPath())
    else:
        query["path"] = "/".join(base_node.getPhysicalPath())
    query["sort_on"] = "path"
    brains = cat(**query)
    return brains


def get_all_workspace_roots(node, workspace):
    """get all workspace root brains

    - workspace (str) name of workspace
    """
    root_node = get_initial_root(node)
    cat = api.portal.get_tool("portal_catalog")
    query = dict()
    query["workspace_root"] = True
    query["workspace"] = workspace
    query["path"] = "/".join(root_node.getPhysicalPath())
    query["portal_type"] = NODE_TYPES
    query["sort_on"] = "created"
    brains = cat(**query)
    return brains


def get_cases():
    """Get all cases.
    """
    cat = api.portal.get_tool("portal_catalog")
    query = dict()
    query["portal_type"] = ROOT_TYPES
    query["sort_on"] = "created"
    brains = cat(**query)
    return brains


def get_tree(node, workspace=None):
    """A tree of brains.
    :paran node: A context to start with.
    :type node: OFS content object.
    :param workspace: A workspace to limit search results (Optional).
    :type workspace: String

    :returns: key/value structure of path/items.
    :rtype: dict
    """

    query = {
        'sort_on': 'path',
        'path': '/'.join(node.getPhysicalPath())
    }

    if workspace:
        query['workspace'] = workspace

    cat = api.portal.get_tool("portal_catalog")
    brains = cat(**query)

    ret = {
        make_relative_path(it.getPath()): make_item(it)
        for it in brains
    }
    return ret


def make_relative_path(path):
    """Return a path relative to the portal object.
    :param path: The path to convert to a relative path.
    :type path: String
    :returns: Converted path, relative to the portal object.
    :rtype: String
    """
    site_path = getSite().getPhysicalPath()
    relative_path = [''] + path.split('/')[len(site_path):]
    return '/'.join(relative_path)


def make_item_overview(item, next_prev=True):
    """Make an item for REST API as expected by the frontend client.
    This one is used for overviews, where we do not want the direct
    next/previous workspace but the next/previous down/up the tree.
    """

    if next_prev:
        ob = item.getObject()

        _prev = get_root_of_workspace(aq_parent(ob))
        _prev = uuidToCatalogBrain(IUUID(_prev)) if _prev else None
        data_previous = make_item_overview(_prev, next_prev=False) if _prev else None  # noqa

        _next = get_next_workspaces(ob, context_aware=True) or []
        data_next = [make_item_overview(it, next_prev=False) for it in _next]

    item = IContentListingObject(item)

    ret = {
        "@id": item.getURL(),
        "@type": item.PortalType(),
        "UID": item.uuid(),
        "title": item.Title(),
        "review_state": item.review_state(),
        "workspace": getattr(item, WORKSPACE_ATTRIBUTE, None) or None,  # at least not Missing.Value  # noqa
        "is_workspace_root": item.workspace_root,
        "created": item.CreationDate(),
        "modified": item.ModificationDate()
    }
    if next_prev:
        ret["previous_workspace"] = data_previous
        ret["next_workspaces"] = data_next

    return ret


def make_item(item, next_prev=True):
    """Make an item for REST API as expected by the frontend client.
    """

    ws = getattr(item, WORKSPACE_ATTRIBUTE, None) or None  # at least not Missing.Value  # noqa
    if next_prev:
        ob = item.getObject()
        parent = aq_parent(ob)

        data_previous = None
        if (
            parent.portal_type in NODE_TYPES and
            getattr(aq_base(parent), WORKSPACE_ATTRIBUTE, ws) != ws
        ):
            # If the parent's ws != current ws it's OK to not reach this branch because:
            # 1) not a Contribution or Case.
            # 2) or hasn't set it's ``workspace`` attribute and not a different ws for sure.
            _prev = uuidToCatalogBrain(IUUID(parent)) if parent else None
            data_previous = make_item(_prev, next_prev=False) if _prev else None

        data_next = []
        for child in ob.contentValues():
            if getattr(aq_base(child), WORKSPACE_ATTRIBUTE, ws) != ws:
                # If child hasn't set it's ws attribute its not a different WS for sure.
                _next = uuidToCatalogBrain(IUUID(child))
                data_next.append(
                    make_item(_next, next_prev=False)
                )

    item = IContentListingObject(item)

    ret = {
        "@id": item.getURL(),
        "@type": item.PortalType(),
        "UID": item.uuid(),
        "title": item.Title(),
        "review_state": item.review_state(),
        "workspace": ws,
        "is_workspace_root": item.workspace_root,
        "created": item.CreationDate(),
        "modified": item.ModificationDate()
    }
    if next_prev:
        ret["previous_workspace"] = data_previous
        ret["next_workspaces"] = data_next

    return ret

#
