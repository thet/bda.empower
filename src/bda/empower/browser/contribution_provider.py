# -*- coding: utf-8 -*-
from bda.empower import discourse
from plone.protect.utils import addTokenToUrl
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.contentprovider.interfaces import ITALNamespaceData
from zope.contentprovider.provider import ContentProviderBase
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider

import zope.schema


@provider(ITALNamespaceData)
class ITALContributionValue(Interface):

    contribution = zope.schema.Dict(title=u"contribution item dict data")


@implementer(ITALContributionValue)
class ContributionProvider(ContentProviderBase):
    template = ViewPageTemplateFile("contribution_provider.pt")

    def update(self):
        self.record = {
            "id": self.contribution.getId(),
            "title": self.contribution.title,
            "workspace": self.contribution.workspace,
            "workspace_title": discourse.get_workspace_definition(
                self.contribution.workspace
            )["title"],
            "text": self.contribution.text.output_relative_to(
                self.contribution
            )
            if getattr(self.contribution, "text", None)
            and self.contribution.text.raw
            else None,
            "modified": self.contribution.modification_date.ISO(),
            "created": self.contribution.creation_date.ISO(),
            "edit_url": addTokenToUrl(
                self.contribution.absolute_url() + "/edit"
            ),
            "reply_url": addTokenToUrl(
                self.contribution.absolute_url()
                + "/++add++Contribution"
            ),
        }

    def render(self):
        return self.template()
