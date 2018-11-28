# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.contentprovider.interfaces import ITALNamespaceData
from zope.contentprovider.provider import ContentProviderBase
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider

import zope.schema


@provider(ITALNamespaceData)
class ITALContributionValue(Interface):

    contribution = zope.schema.Dict(
        title=u"contribution item dict data"
    )


@implementer(ITALContributionValue)
class ContributionProvider(ContentProviderBase):
    template = ViewPageTemplateFile("contribution_provider.pt")

    def update(self):
        ctx = self.contribution['ob']
        self.record = {
            "title": ctx.title,
            "description": getattr(ctx, "description", None),
            "text": ctx.text.output_relative_to(ctx)
            if getattr(ctx, "text", None) and ctx.text.raw
            else None,
            "modified": ctx.modification_date.ISO(),
            "created": ctx.creation_date.ISO(),
        }

    def render(self):
        return self.template()
