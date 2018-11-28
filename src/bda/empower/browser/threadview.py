from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.contentprovider.interfaces import IContentProvider
from bda.empower import discourse


BOTTOMLEVEL = 6


class ThreadView(BrowserView):

    _itemtree = None

    @property
    def itemtree(self):
        if self._itemtree is not None:
            return self._itemtree
        items = discourse.get_current_workspace_tree(self.context)
        tree = discourse.build_tree(items)
        self._itemtree = tree
        return tree

    @property
    def start_path(self):
        start_path = None
        ctx = discourse.get_root_of_workspace(self.context)
        if ctx:
            # start a level above the start context.
            # itemtree structure works that way.
            start_path = "/".join(ctx.getPhysicalPath()[:-1]
        )
        return start_path

    def contribution_provider(self, context):
        provider = getMultiAdapter(
            (context, self.request, self),
            IContentProvider,
            name=u"contribution_provider",
        )
        return provider.render()

    bottomlevel = BOTTOMLEVEL
    recurse = ViewPageTemplateFile("threadview_recurse.pt")
