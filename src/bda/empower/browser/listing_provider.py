# -*- coding: utf-8 -*-
from bda.empower import discourse
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.contentprovider.provider import ContentProviderBase


class ListingProvider(ContentProviderBase):

    template = ViewPageTemplateFile("listing_provider.pt")

    @property
    def current_def(self):
        return self.__parent__.current_def

    def update(self):
        pass

    def render(self):
        return self.template()
