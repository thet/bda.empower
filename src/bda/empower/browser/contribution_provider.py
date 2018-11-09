from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import adapter
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import implementer
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IBrowserView


@implementer(IContentProvider)
@adapter(Interface, IBrowserRequest, IBrowserView)
class ContributionProvider(BrowserView):
    template = ViewPageTemplateFile(u'contribution_provider.pt')

    def __init__(self, context, request, view):
        self.view = view
        self.context = context
        self.request = request

    @property
    def data(self):
        return {
            'title': self.context.title
        }

    def render(self):
        return self.template(self)
