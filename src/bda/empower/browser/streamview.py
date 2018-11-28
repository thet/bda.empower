# -*- coding: utf-8 -*-
from plone.batching import Batch
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.contentprovider.interfaces import IContentProvider


class StreamView(BrowserView):
    def items(self):
        # batch paging
        b_start = int(self.request.form.get("b_start", 0))
        b_size = int(self.request.form.get("b_size", 30))

        query = {}

        query["portal_type"] = "Contribution"
        query["sort_on"] = "created"
        query["sort_order"] = "reverse"
        query["path"] = {"query": "/".join(self.context.getPhysicalPath())}

        cat = getToolByName(self.context, "portal_catalog")
        result = cat(batch=True, **query)
        return Batch(result, size=b_size, start=b_start)

    def contribution_provider(self, context):
        provider = getMultiAdapter(
            (context, self.request, self),
            IContentProvider,
            name=u"contribution_provider",
        )
        return provider.render()
