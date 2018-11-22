from plone.app.layout.navigation.navtree import buildFolderTree
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.contentprovider.interfaces import IContentProvider


BOTTOMLEVEL = 6


class ThreadView(BrowserView):

    def itemtree(self):
        context = self.context
        query = {}
        query["portal_type"] = "Contribution"
        query["path"] = {"query": "/".join(context.getPhysicalPath())}
        query["sort_on"] = "created"
        tree = buildFolderTree(context, obj=context, query=query)


        from bda.empower.discourse import get_current_workspace_tree
        li = get_current_workspace_tree(self.context)
        from pprint import pprint
        pprint([
            it.getURL() for it in li
        ])
        return tree

    def start_recurse(self):
        return self.recurse(
            children=self.itemtree().get("children", []),
            level=0,
            bottomLevel=self.bottomlevel,
        )

    def contribution_provider(self, context):
        provider = getMultiAdapter(
            (context, self.request, self),
            IContentProvider,
            name=u"contribution_provider",
        )
        return provider.render()

    bottomlevel = BOTTOMLEVEL
    recurse = ViewPageTemplateFile("threadview_recurse.pt")
